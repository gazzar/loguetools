import os
import sys
import click
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
import re
from loguetools import og, xd, common


XD_PATCH_LENGTH = 1024


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--match_name", "-n", help="Dump the patch with name NAME")
@click.option("--match_ident", "-i", type=int, help="Dump the patch with ident ID")
def explode(filename, match_name, match_ident):
    """Explode a minilogue og or xd program bank or extract a program.

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
    if input_path.suffix == ".mnlgpreset":
        suffix = ".mnlgprog"
        prog_info_template = og.prog_info_template
        fileinfo_xml = og.fileinfo_xml
    elif input_path.suffix == ".mnlgxdlib":
        suffix = ".mnlgxdprog"
        prog_info_template = xd.prog_info_template
        fileinfo_xml = xd.fileinfo_xml

    sanitise = common.sanitise_patchname()
    for i, p in enumerate(proglist):
        patchdata = zipobj.read(p)
        prgname = common.program_name(patchdata)
        if prgname == "Init Program":
            continue
        output_path = (dir_path / (sanitise(prgname) + suffix))
        with ZipFile(output_path, "w") as zip:
            binary = zipobj.read(p)

            # .prog_bin record/file
            zip.writestr(f"Prog_000.prog_bin", binary)

            # .prog_info record/file
            zip.writestr(f"Prog_000.prog_info", prog_info_template)

            # FileInformation.xml record/file
            zip.writestr(f"FileInformation.xml", fileinfo_xml([0]))

        print(f"{int(p[5:8])+1:03d}: {prgname:<12s}  ->  {output_path}")


if __name__ == "__main__":
    explode()
