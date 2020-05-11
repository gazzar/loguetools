import os
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

filenames = {}

def sanitise_patchname(filepath):
    """Generate a sensible patch filename stem.
    Replaces whitespace with underscores and ensures all names are unique.
    If a patch name has already been encountered during bank export, if encountered
    again, the new name is munged by appending a hyphen and unique number.

    Args:
        filepath (Path object): A Path object with a stem element

    Returns:
        Path: Sanitised path

    """
    stem = re.sub(r"[^\w\-+]", "_", filepath.stem)
    if filepath.stem in filenames:
        filenames[filepath.stem] = filenames[filepath.stem] + 1
        stem = f"{stem}-{filenames[filepath.stem]}"
        filenames[stem] = 0
    else:
        filenames[filepath.stem] = 0
    output_path = filepath.with_name(stem).with_suffix(filepath.suffix)
    return output_path


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--match_name", "-n", help="Dump the patch with name NAME")
@click.option("--match_ident", "-i", type=int, help="Dump the patch with ident ID")
def explode(filename, match_name, match_ident):
    """Explode a minilogue xd program bank or extract a program.

    \b
    Examples
    --------
    explode xd_program_bank.mnlgxdlib
    explode -n XDProgName xd_program_bank.mnlgxdlib

    """
    zipobj = ZipFile(filename, "r", compression=ZIP_DEFLATED, compresslevel=9)
    proglist = common.zip_progbins(zipobj)

    if match_name is not None:
        match_ident = common.id_from_name(zipobj, match_name)

    if match_ident is not None:
        proglist = [proglist[match_ident - 1]]

    # Create directory based on the filename stem
    input_path = pathlib.Path(filename)
    dir_path = input_path.with_suffix("")
    dir_path.mkdir(exist_ok=True)

    for i, p in enumerate(proglist):
        patchdata = zipobj.read(p)
        prgname = common.program_name(patchdata)
        if prgname == "Init Program":
            continue
        output_path = (dir_path / (prgname + ".mnlgxdprog"))
        output_path = sanitise_patchname(output_path)
        with ZipFile(output_path, "w") as xdzip:
            binary_xd = zipobj.read(p)

            # .prog_bin record/file
            xdzip.writestr(f"Prog_000.prog_bin", binary_xd)

            # .prog_info record/file
            xdzip.writestr(f"Prog_000.prog_info", xd.prog_info_template)

            # FileInformation.xml record/file
            xdzip.writestr(f"FileInformation.xml", xd.fileinfo_xml([0]))

        print(f"{int(p[5:8])+1:03d}: {prgname:<12s}  ->  {output_path}")


if __name__ == "__main__":
    explode()
