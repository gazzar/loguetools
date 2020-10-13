import sys
import click
from zipfile import ZipFile, ZIP_DEFLATED
from types import LambdaType, FunctionType
import struct
from pprint import pprint
import pathlib
import re
from loguetools import og, xd, common


XD_PATCH_LENGTH = 1024


def convert_og_to_xd(patch):
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
    for m in xd.minilogue_xd_patch_struct:
        f = xd.patch_translation_value(*m)
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
    zipobj = ZipFile(filename, "r", compression=ZIP_DEFLATED, compresslevel=9)
    proglist = common.zipread_progbins(zipobj)

    input_file = pathlib.Path(filename)
    assert input_file.suffix in {".mnlgprog", ".mnlgpreset", ".mnlglib"}
    if input_file.suffix == ".mnlgprog":
        # single patch/program
        match_name = input_file
        match_ident = 1
    elif match_name is not None:
        # patch library/program pack
        match_ident = common.id_from_name(zipobj, match_name)

    if match_ident is not None:
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
    numofprog = str(len(proglist))
    date = None
    prefix = None
    copyright = None
    author = None
    comment = None
    if input_file.suffix == ".mnlgpreset":
        dataid, name, author, version, numofprog, date, prefix, copyright = common.all_from_presetinformation_xml(zipobj)
        if dataid is None:
          dataid = name

    non_init_patch_ids = []
    with ZipFile(output_file, "w") as xdzip:
        for i, p in enumerate(proglist):
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

            raw_og_patch = common.parse_patchdata(patchdata)
            patch = og.normalise_og_patch(raw_og_patch)
            patch_xd, binary_xd = convert_og_to_xd(patch)

            # .prog_bin record/file
            xdzip.writestr(f"Prog_{i:03d}.prog_bin", binary_xd)

            # .prog_info record/file
            prog_info_xd = common.prog_info_template_xml("xd")
            xdzip.writestr(f"Prog_{i:03d}.prog_info", prog_info_xd)

            if verbose:
                pprint(vars(patch))
                print()

        if len(proglist) > 1 and not force_preset:
            # FavoriteData.fav_data record/file
            xdzip.writestr(f"FavoriteData.fav_data", xd.favorite_template)

        # FileInformation.xml record/file
        xdzip.writestr(f"FileInformation.xml", common.fileinfo_xml("xd", non_init_patch_ids, force_preset))

        if force_preset:
            xdzip.writestr(f"PresetInformation.xml", common.presetinfo_xml("xd", dataid, name, author, version, numofprog, date, prefix, copyright))

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
