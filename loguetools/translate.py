import sys
import click
from zipfile import ZipFile, ZIP_DEFLATED
from types import LambdaType, FunctionType
import struct
from pprint import pprint
import pathlib
import re
from loguetools import og, xd, prlg as prologue, molg, common


XD_PATCH_LENGTH = 1024


def convert_to_xd(patch, flavour):
    """Converts a minilogue og patch to a minilogue xd patch.

    Args:
        patch (Patch instance): minilogue og patch to translate

    Returns:
        Patch: minilogue xd patch object
        Binary Struct: minilogue xd patch binary

    """
    patch_xd = common.Patch()
    binary_xd = bytearray(XD_PATCH_LENGTH)

    offset = 0
    for m in xd.patch_struct[flavour]:
        f = xd.patch_translation_value[flavour](*m)
        if isinstance(f.source, str):
            value = getattr(patch, f.source)
        elif isinstance(f.source, (int, bytes)):
            value = f.source
        elif callable(f.source):
            value = f.source(patch)
        else:
            raise (Exception("Unknown patch field type"))

        setattr(patch_xd, f.name, value)
        if isinstance(value, str):
            value = bytes(value, "utf-8")
        struct.pack_into(f.type, binary_xd, offset, value)
        offset += struct.calcsize(f.type)
	
    return patch_xd, binary_xd


def convert_from_syx(filename):
    with open(filename, "rb") as f:
        f.seek(5)
        flavor = {
            0x44:"molg",
            0x51:"xd",
            0x2C:"og",
            0x4B:"prologue"
        }[ord(f.read(1))]
        if ord(f.read(1)) == 0x4C:
          f.seek(9)
        b = 0
        h = 0
        patch_data = bytearray()
        while b != 0xF7 and h != 0xF7:
            h = ord(f.read(1))
            i = 0
            while i < 7 and b != 0xF7 and h != 0xF7:
                i += 1
                b = ord(f.read(1))
                if b != 0xF7:
                    patch_data.append((b | (h << 7)) & 0xFF);
                    h >>= 1;
        f.close()
        return (flavor, patch_data)


def translate(filename, match_name, match_ident, verbose, unskip_init, force_preset):
    """Translate a minilogue program or program bank to the minilogue xd.

    \b
    Examples
    --------
    translate og_program_bank.mnlgpreset
    translate -n OGProgName og_program_bank.mnlgpreset
    translate -n "OG Prog Name" og_program_bank.mnlgpreset
    translate OGProgName.mnlgprog

    """
    input_file = pathlib.Path(filename)
    assert input_file.suffix in {".mnlgprog", ".mnlgpreset", ".mnlglib", ".prlgprog", ".prlgpreset", ".prlglib", ".molgprog", ".molgpreset", ".molglib", ".syx"}

    if input_file.suffix != ".syx":
        flavor = "xd"
        zipobj = ZipFile(filename, "r", compression=ZIP_DEFLATED, compresslevel=9)
        proglist = common.zipread_progbins(zipobj)

    if input_file.suffix == ".mnlgprog":
        # single patch/program
        match_name = input_file
        match_ident = 1
    elif match_name is not None:
        # patch library/program pack
        match_ident = common.id_from_name(zipobj, match_name)

    if input_file.suffix == ".syx":
        stem = input_file.stem
        proglist = ["Prog_000.prog_bin"]
        (flavor, patchdata) = convert_from_syx(input_file)
        patch_ext = {
            "molg":".molgprog",
            "xd":".mnlgxdprog",
            "og":".mnlgprog",
            "prologue":".prlgprog"
        }[flavor]

    elif match_ident is not None:
        proglist = [proglist[match_ident - 1]]
        # https://stackoverflow.com/a/13593932
        stem = re.sub(r"[^\w\-_\.]", "_", match_name.stem)
        patch_ext = ".mnlgxdprog"
    else:
        stem = input_file.stem
        patch_ext = ".mnlgxdlib"

    if force_preset:
        patch_ext = ".mnlgxdpreset"

    output_file = input_file.with_name(stem).with_suffix(patch_ext)

    # Read any information from preset if available
    dataid = stem
    name = stem
    version = None
    date = None
    prefix = None
    copyright = None
    author = None
    comment = None
    if input_file.suffix in {".mnlgxdpreset", ".mnlgpreset", ".prlgpreset", ".molgpreset"}:
        dataid, name, author, version, numofprog, date, prefix, copyright = common.all_from_presetinformation_xml(zipobj)
        if dataid is None:
          dataid = name

    non_init_patch_ids = []
    numofprog = 0
    with ZipFile(output_file, "w") as xdzip:
        for i, p in enumerate(proglist):
            if input_file.suffix != ".syx":
                patchdata = zipobj.read(p)
            prgname = common.program_name(patchdata)
            flavour = common.patch_type(patchdata)
            if common.is_init_patch(flavour, hash):
                # Init Program identified based on hash; i.e. a "True" Init Program
                continue
            if common.is_init_program_name(prgname) and not unskip_init:
                # Init Program found and option not to skip is unchecked
                continue
            non_init_patch_ids.append(i)
            print(f"{int(p[5:8])+1:03d}: {prgname}")

            if input_file.suffix != ".syx":
                if flavour == 'og': 
                    raw_og_patch = common.parse_patchdata(patchdata)
                    patch = og.normalise_og_patch(raw_og_patch)
                    patch_xd, patchdata = convert_to_xd(patch, flavour)
                elif flavour == 'prologue':
                    raw_og_patch = common.parse_patchdata(patchdata)
                    patch = prologue.normalise_patch(raw_og_patch)
                    patch_xd, patchdata = convert_to_xd(patch, flavour)
                elif flavour == 'molg':
                    raw_og_patch = common.parse_patchdata(patchdata)
                    patch = molg.normalise_patch(raw_og_patch)
                    patch_xd, patchdata = convert_to_xd(patch, flavour)

            # .prog_bin record/file
            xdzip.writestr(f"Prog_{i:03d}.prog_bin", patchdata)

            # .prog_info record/file
            prog_info_xd = common.prog_info_template_xml(flavor)
            xdzip.writestr(f"Prog_{i:03d}.prog_info", prog_info_xd)

            numofprog += 1

            if verbose:
                pprint(vars(patch))
                print()

        if len(proglist) > 1 and not force_preset:
            if flavor == "prologue":
                xdzip.writestr(f"LivesetData.lvs_data", getattr(globals()[flavor], "favorite_template"))
            else:
                # FavoriteData.fav_data record/file
                try:
                    xdzip.writestr(f"FavoriteData.fav_data", getattr(globals()[flavor], "favorite_template"))
                except:
                    pass

        if force_preset:
            xdzip.writestr(f"PresetInformation.xml", common.presetinfo_xml(flavor, dataid, name, author, version, str(numofprog), date, prefix, copyright))


        # FileInformation.xml record/file
        xdzip.writestr(f"FileInformation.xml", common.fileinfo_xml(flavor, non_init_patch_ids, force_preset))

        print("Wrote", output_file)


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--match_name", "-n", help="Dump the patch with name NAME")
@click.option("--match_ident", "-i", type=int, help="Dump the patch with ident ID")
@click.option("--verbose", "-v", is_flag=True, help="List the patch contents")
@click.option("--unskip_init", "-u", is_flag=True, help="Don't skip patches named Init Program")
@click.option("--force_preset", "-p", is_flag=True, help="Translate to preset file")
def click_translate(filename, match_name, match_ident, verbose, unskip_init, force_preset):
    translate(filename, match_name, match_ident, verbose, unskip_init, force_preset)


if __name__ == "__main__":
    click_translate()
