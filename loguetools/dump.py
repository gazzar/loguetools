import click
import zipfile
from pprint import pprint
from loguetools import og, common


def print_patch(patchdata):
    import copy

    patch = common.parse_patchdata(patchdata)
    if common.patch_ident(patchdata)[0] == "og":
        patch = og.normalise_og_patch(patch)

    patchcopy = copy.deepcopy(vars(patch))
    for key in patchcopy:
        val = patchcopy[key]
        if isinstance(val, (bytes, bytearray)) and len(val) > 12:
            patchcopy[key] = val.hex()
    pprint(patchcopy)



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
        flavour, hash = common.patch_ident(patchdata)
        prgname = common.program_name(patchdata, flavour)
        if common.is_init_program_name(prgname):
            continue
        if md5:
            print(f"{int(p[5:8])+1:03d}: {prgname:12s} {hash}")
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
