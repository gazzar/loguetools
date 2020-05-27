import os
import sys
import click
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
import hashlib
import re
from loguetools import og, xd, common
import version


XD_PATCH_LENGTH = 1024


def explode(filename, match_name, match_ident, append_md5_4, append_version, unskip_init):
    """Explode a minilogue og or xd or prologue program bank or extract a program.

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
    if input_path.suffix == ".mnlgxdlib":
        suffix = ".mnlgxdprog"
        prog_info_template = common.prog_info_template("xd")
        fileinfo_xml = common.fileinfo_xml("xd", [0])
    elif input_path.suffix == ".mnlgpreset":
        suffix = ".mnlgprog"
        prog_info_template = common.prog_info_template("og")
        fileinfo_xml = common.fileinfo_xml("og", [0])
    elif input_path.suffix == ".prlglib":
        suffix = ".prlgprog"
        prog_info_template = common.prog_info_template("prologue")
        fileinfo_xml = common.fileinfo_xml("prologue", [0])

    sanitise = common.sanitise_patchname()
    for i, p in enumerate(proglist):
        patchdata = zipobj.read(p)
        prgname = common.program_name(patchdata)
        if (prgname == "Init Program") and (not unskip_init):
            continue
        if append_md5_4:
            hash = hashlib.md5(patchdata).hexdigest()
            prgname = f"{prgname}-{hash[:4]}"
        if append_version:
            ver = version.__version__.replace(".", "")
            prgname = f"{prgname}-v{ver}"
        output_path = (dir_path / (sanitise(prgname) + suffix))
        with ZipFile(output_path, "w") as zip:
            binary = zipobj.read(p)

            # .prog_bin record/file
            zip.writestr(f"Prog_000.prog_bin", binary)

            # .prog_info record/file
            zip.writestr(f"Prog_000.prog_info", prog_info_template)

            # FileInformation.xml record/file
            zip.writestr(f"FileInformation.xml", fileinfo_xml)

        print(f"{int(p[5:8])+1:03d}: {prgname:<12s}  ->  {output_path}")


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--match_name", "-n", help="Dump the patch with name NAME")
@click.option("--match_ident", "-i", type=int, help="Dump the patch with ident ID")
@click.option("--append_md5_4", "-m", is_flag=True, help="Append 4 digits of an md5 checksum to the filename")
@click.option("--append_version", "-v", is_flag=True, help="Append loguetools version to the filename")
@click.option("--unskip_init", "-u", is_flag=True, help="Don't skip patches named Init Program")
def click_explode(filename, match_name, match_ident, append_md5_4, append_version, unskip_init):
    explode(filename, match_name, match_ident, append_md5_4, append_version, unskip_init)


if __name__ == "__main__":
    click_explode()
