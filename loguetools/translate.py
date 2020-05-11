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


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--match_name", "-n", help="Dump the patch with name NAME")
@click.option("--match_ident", "-i", type=int, help="Dump the patch with ident ID")
@click.option("--verbose", "-v", is_flag=True, help="List the patch contents")
def translate(filename, match_name, match_ident, verbose):
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
    proglist = common.zip_progbins(zipobj)

    input_file = pathlib.Path(filename)
    assert input_file.suffix in {".mnlgprog", ".mnlgpreset"}
    if input_file.suffix == ".mnlgprog":
        match_name = input_file
        match_ident = 1
    elif match_name is not None:
        match_ident = common.id_from_name(zipobj, match_name)

    if match_ident is not None:
        proglist = [proglist[match_ident - 1]]
        # https://stackoverflow.com/a/13593932
        stem = re.sub(r"[^\w\-_\.]", "_", match_name.stem)
        patch_ext = ".mnlgxdprog"
    else:
        stem = input_file.stem
        patch_ext = ".mnlgxdlib"
    output_file = input_file.with_name(stem).with_suffix(patch_ext)

    non_init_patch_ids = []
    with ZipFile(output_file, "w") as xdzip:
        for i, p in enumerate(proglist):
            patchdata = zipobj.read(p)
            prgname = common.program_name(patchdata)
            if prgname == "Init Program":
                continue
            non_init_patch_ids.append(i)
            print(f"{int(p[5:8])+1:03d}: {prgname}")

            raw_og_patch = common.parse_patchdata(patchdata)
            patch = og.normalise_og_patch(raw_og_patch)
            patch_xd, binary_xd = convert_og_to_xd(patch)

            # .prog_bin record/file
            xdzip.writestr(f"Prog_{i:03d}.prog_bin", binary_xd)

            # .prog_info record/file
            xdzip.writestr(f"Prog_{i:03d}.prog_info", xd.prog_info_template)

            if verbose:
                pprint(vars(patch))
                print()

        if len(proglist) > 1:
            # FavoriteData.fav_data record/file
            xdzip.writestr(f"FavoriteData.fav_data", xd.favorite_template)

        # FileInformation.xml record/file
        xdzip.writestr(f"FileInformation.xml", xd.fileinfo_xml(non_init_patch_ids))

        print("Wrote", output_file)


if __name__ == "__main__":
    translate()
