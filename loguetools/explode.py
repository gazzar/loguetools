import click
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
from loguetools import common
from loguetools import version


XD_PATCH_LENGTH = 1024


def explode(filename, match_name, match_ident, prepend_id, append_md5_4, append_version, unskip_init, unskip_factory):
    """Explode a minilogue og or xd or prologue program bank or extract a program.

    \b
    Examples
    --------
    explode xd_program_bank.mnlgxdlib
    explode -n XDProgName xd_program_bank.mnlgxdlib

    """
    zipobj = ZipFile(filename, "r", compression=ZIP_DEFLATED, compresslevel=9)
    proglist = common.zipread_progbins(zipobj)
    proginfo_dict = common.zipread_all_prog_info(zipobj)

    if match_name is not None:
        match_ident = common.id_from_name(zipobj, match_name)

    if match_ident is not None:
        proglist = [proglist[match_ident - 1]]

    # Create directory based on the filename stem
    input_file = pathlib.Path(filename)
    dir_path = input_file.with_suffix("")
    dir_path.mkdir(exist_ok=True)
    if input_file.suffix in {".mnlgxdpreset", ".mnlgxdlib"}:
        suffix = ".mnlgxdprog"
        flavour = "xd"
    elif input_file.suffix in {".mnlgpreset", ".mnlglib"}:
        suffix = ".mnlgprog"
        flavour = "og"
    elif input_file.suffix in {".prlgpreset", ".prlglib"}:
        suffix = ".prlgprog"
        flavour = "prologue"
    elif input_file.suffix in {".molgpreset", ".molglib"}:
        suffix = ".molgprog"
        flavour = "monologue"
    elif input_file.suffix in {".kklib"}:
        suffix = ".kkprog"
        flavour = "kk"
    fileinfo_xml = common.fileinfo_xml(flavour, [0], False)

    # Read any copyright and author information if available
    copyright = None
    author = None
    comment = None
    if input_file.suffix in {".mnlgxdpreset", ".mnlgpreset", ".prlgpreset", ".molgpreset"}:
        author, copyright = common.author_copyright_from_presetinformation_xml(zipobj)

    sanitise = common.sanitise_patchname()
    for i, p in enumerate(proglist):
        patchdata = zipobj.read(p)
        flavour, hash = common.patch_ident(patchdata)
        if common.is_init_patch(flavour, hash):
            # Init Program identified based on hash; i.e. a "True" Init Program
            continue
        if common.is_factory_program(flavour, hash) and not unskip_factory:
            # Factory Program found and option to include is unchecked
            continue
        prgname = common.program_name(patchdata, flavour)
        print(hash, prgname)
        if common.is_init_program_name(prgname) and not unskip_init:
            # Init Program found and option not to skip is unchecked
            continue
        if prepend_id:
            prgname = f"{i+1:03d}_{prgname}"
        if append_md5_4:
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
            # Use any available presetinformation_xml author and copyright fields
            if author is not None:
                comment = f"Author: {author}"
            proginfo_comment = (proginfo_dict[p])['Comment']
            if proginfo_comment is not None:
                comment = f"{comment}, " + proginfo_comment
            prog_info_template = common.prog_info_template_xml(flavour, comment=comment, copyright=copyright)
            zip.writestr(f"Prog_000.prog_info", prog_info_template)

            # FileInformation.xml record/file
            zip.writestr(f"FileInformation.xml", fileinfo_xml, False)

        print(f"{int(p[5:8])+1:03d}: {prgname:<12s}  ->  {output_path}")


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--match_name", "-n", help="Dump the patch with name NAME")
@click.option("--match_ident", "-i", type=int, help="Dump the patch with ident ID")
@click.option("--prepend_id", "-p", is_flag=True, help="Prepend patch ID to the filename")
@click.option("--append_md5_4", "-m", is_flag=True, help="Append 4 digits of an md5 checksum to the filename")
@click.option("--append_version", "-v", is_flag=True, help="Append loguetools version to the filename")
@click.option("--unskip_init", "-u", is_flag=True, help="Don't skip patches named Init Program")
@click.option("--unskip_factory", "-f", is_flag=True, help="Don't skip factory patches")
def click_explode(filename, match_name, match_ident, prepend_id, append_md5_4, append_version, unskip_init, unskip_factory):
    explode(filename, match_name, match_ident, prepend_id, append_md5_4, append_version, unskip_init, unskip_factory)


if __name__ == "__main__":
    click_explode()
