import sys
import click
from zipfile import ZipFile, ZIP_DEFLATED
from types import LambdaType, FunctionType
import struct
from pprint import pprint
import pathlib
import re
from loguetools import common
import glob
from os.path import join, split, splitext

def collapse(filename, unskip_init, force_preset):
    proglist = []
    for p in common.patch_suffixes:
        proglist.extend(glob.glob(join(filename, "*" + p)))

    (flavor, lib_ext, preset_ext) = {
        ".molgprog": ("monologue", ".molglib", ".molgpreset"),
        ".mnlgxdprog": ("xd", ".mnlgxdlib", ".mnlgxdpreset"),
        ".mnlgprog": ("og", ".mnlglib", ".mnlgpreset"),
        ".prlgprog": ("prologue", ".prlglib", ".prlgpreset")
    }[splitext(proglist[0])[1]]

    if force_preset:
        output_file = filename + preset_ext
    else:
        output_file = filename + lib_ext

    name = split(filename)[1]
    dataid = name
    version = None
    date = None
    prefix = None
    copyright = None
    author = None
    comment = None

    non_init_patch_ids = []
    numofprog = 0
    with ZipFile(output_file, "w") as xdzip:
        for i, p in enumerate(proglist):
            zipobj = ZipFile(p, "r", compression=ZIP_DEFLATED, compresslevel=9)
            patchdata = zipobj.read(common.zipread_progbins(zipobj)[0])
            prgname = common.program_name(patchdata)
            flavour = common.patch_type(patchdata)
            if flavor != flavour:
                # actual patch type did not match with the first one
                continue
            if common.is_init_patch(flavour, hash):
                # Init Program identified based on hash; i.e. a "True" Init Program
                continue
            if common.is_init_program_name(prgname) and not unskip_init:
                # Init Program found and option not to skip is unchecked
                continue
            non_init_patch_ids.append(i)
            print(f"{i+1:03d}: {prgname}")

            # .prog_bin record/file
            xdzip.writestr(f"Prog_{i:03d}.prog_bin", patchdata)

            # .prog_info record/file
            prog_info = common.prog_info_template_xml(flavor)
            xdzip.writestr(f"Prog_{i:03d}.prog_info", prog_info)

            numofprog += 1

        if force_preset:
            xdzip.writestr(f"PresetInformation.xml", common.presetinfo_xml(flavor, dataid, name, author, version, str(numofprog), date, prefix, copyright))
        elif flavor == "prologue":
            xdzip.writestr(f"LivesetData.lvs_data", getattr(globals()[flavor], "favorite_template"))
        else:
            # FavoriteData.fav_data record/file
            try:
                xdzip.writestr(f"FavoriteData.fav_data", getattr(globals()[flavor], "favorite_template"))
            except:
                pass

        # FileInformation.xml record/file
        xdzip.writestr(f"FileInformation.xml", common.fileinfo_xml(flavor, non_init_patch_ids, force_preset))

        print("Wrote", output_file)


@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False))
@click.option("--unskip_init", "-u", is_flag=True, help="Don't skip patches named Init Program")
@click.option("--force_preset", "-p", is_flag=True, help="Collapse to preset file")
def click_collapse(path, unskip_init, force_preset):
    collapse(path, unskip_init, force_preset)


if __name__ == "__main__":
    click_collapse()
