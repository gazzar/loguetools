import sys
import click
import zipfile
import struct
from pprint import pprint
import hashlib
from loguetools import og, common


def print_patch(patchdata):
    patch = common.parse_patchdata(patchdata)
    if common.patch_type(patchdata) == "og":
        patch = og.normalise_og_patch(patch)
    pprint(vars(patch))


def dump(filename, match_name, match_ident, verbose, md5):
    """Dump contents of FILENAME to stdout. Supports minilogue og and xd patch files.

    \b
    Examples
    --------
    dump og_program_bank.mnlgpreset
    dump xd_program_bank.mnlgxdlib
    dump OGProgName.mnlgprog
    dump XDProgName.mnlgxdprog
    dump -n OGProgName og_program_bank.mnlgpreset
    dump -n "OG Prog Name" og_program_bank.mnlgpreset
    dump -i 10 og_program_bank.mnlgpreset
    dump -i 10 -m og_program_bank.mnlgpreset

    """
    zipobj = zipfile.ZipFile(filename, "r")
    proglist = common.zipread_progbins(zipobj)

    if match_name is not None:
        match_ident = common.id_from_name(zipobj, match_name)

    if match_ident is not None:
        proglist = [proglist[match_ident - 1]]

    for p in proglist:
        patchdata = zipobj.read(p)
        prgname = common.program_name(patchdata)
        if prgname == "Init Program":
            continue
        checksum = ""
        if md5:
            checksum = hashlib.md5(patchdata).hexdigest()
        print(f"{int(p[5:8])+1:03d}: {prgname:12s} {checksum}")
        if verbose:
            print_patch(patchdata)
            print()


@click.command()
@click.argument("filename", type=click.File("rb"))
@click.option("--match_name", "-n", help="Dump the patch with name NAME")
@click.option("--match_ident", "-i", type=int, help="Dump the patch with ident ID")
@click.option("--verbose", "-v", is_flag=True, help="List the patch contents")
@click.option("--md5", "-m", is_flag=True, help="List patch checksums")
def click_dump(filename, match_name, match_ident, verbose, md5):
    dump(filename, match_name, match_ident, verbose, md5)



if __name__ == "__main__":
    click_dump()
