import xml.etree.ElementTree as ET
from xml.dom import minidom
import struct
from types import SimpleNamespace
import fnmatch
from loguetools import og, xd
import version
import re
import textwrap


class Patch(SimpleNamespace):
    """A simple container class for patch data."""

    pass


class sanitise_patchname():
    """Generate a sensible patch filename stem.
    Replaces whitespace with underscores and ensures all names are unique.
    If a patch name has already been encountered during bank export, if encountered
    again, the new name is munged by appending a hyphen and unique number.

    Args:
        filename (str): A filename

    Returns:
        Path: Sanitised name

    """
    def __init__(self):
        self.filenames = {}

    def __call__(self, filename):
        filename = str(filename)
        output_name = re.sub(r"[^\w\-+]", "_", filename)
        if filename in self.filenames:
            self.filenames[filename] = self.filenames[filename] + 1
            output_name = f"{output_name}-{self.filenames[filename]}"
            self.filenames[output_name] = 0
        else:
            self.filenames[filename] = 0
        return output_name


init_program_hashes = {
    'og': '9d2fd7e2e97edc87306d8360eb881534',
    'xd': 'fd6940f683f8b69966fc3fd08bbb5ee3',
    'prologue': 'a4fa5be24cb09c35a91e81ef2bbf71af',
}
def is_init_patch(flavour, hash):
    """True iff the hash matches the Init Program md5 checksum for the corresponding flavour

    Args:
        flavour (str): "xd", "og", "prologue"
        hash (bool): md5 checksum string

    Returns:
        bool: True iff Init Program matched

    """
    return init_program_hashes[flavour] == hash


def prog_info_template_xml(flavour, programmer=None, comment=None, copyright=None):
    """xml template for Prog_nnn.prog_info xml patch elements

    Args:
        flavour: "xd", "og", "prologue"
            choose "xd", "minilogue", "prologue"
        programmer (str), default=None :  programmer field text
        comment (str), default=None : comment field text
        copyright (str), default=None : copyright field text

    Returns:
        str: formatted xml

    """
    # create the file structure
    flavour_to_product = {
        "xd":"xd",
        "og":"minilogue",
        "prologue":"prologue"
    }
    root = ET.Element(flavour_to_product[flavour] + "_ProgramInformation")
    programmer_elem = ET.SubElement(root, "Programmer")
    programmer_elem.text = programmer
    comment_elem = ET.SubElement(root, "Comment")
    comment_elem.text = comment
    loguetools_version_elem = ET.SubElement(root, "loguetoolsVersion")
    loguetools_version_elem.text = version.__version__
    if copyright is not None:
        copyright_elem = ET.SubElement(root, "Copyright")
        copyright_elem.text = copyright

    # https://stackoverflow.com/a/3095723
    formatted_xml = minidom.parseString(
        ET.tostring(root, encoding="utf-8", method="xml")
    ).toprettyxml(indent="  ")

    return formatted_xml


def fileinfo_xml(flavour, non_init_patch_ids):
    """Build FileInformation.xml metadata file.

    Args:
        flavour: 
        non_init_patch_ids (list of ints): 0-based list of non-Init-Program patches

    Returns:
        str: formatted xml

    """
    # create the file structure
    root = ET.Element("KorgMSLibrarian_Data")
    product = ET.SubElement(root, "Product")
    product.text = {
        "xd":"minilogue xd",
        "og":"minilogue",
        "prologue":"prologue"
    }[flavour]
    contents = ET.SubElement(root, "Contents")

    contents.set("NumProgramData", str(len(non_init_patch_ids)))
    contents.set("NumPresetInformation", "0")
    contents.set("NumTuneScaleData", "0")
    contents.set("NumTuneOctData", "0")

    if len(non_init_patch_ids) <= 1:
        contents.set("NumFavoriteData", "0")
    else:
        contents.set("NumFavoriteData", "1")
        fave = ET.SubElement(contents, "FavoriteData")
        fave_info = ET.SubElement(fave, "File")
        fave_info.text = "FavoriteData.fav_data"

    for i in non_init_patch_ids:
        prog = ET.SubElement(contents, "ProgramData")
        prog_info = ET.SubElement(prog, "Information")
        prog_info.text = f"Prog_{i:03d}.prog_info"
        prog_bin = ET.SubElement(prog, "ProgramBinary")
        prog_bin.text = f"Prog_{i:03d}.prog_bin"

    # https://stackoverflow.com/a/3095723
    formatted_xml = minidom.parseString(
        ET.tostring(root, encoding="utf-8", method="xml")
    ).toprettyxml(indent="  ")

    return formatted_xml


patch_suffixes = {
    ".mnlgxdprog", ".mnlgprog", ".prlgprog"
}
lib_suffixes = {
    ".mnlgxdpreset", ".mnlgpreset", ".prlgpreset",
    ".mnlgxdlib", ".mnlglib", ".prlglib"
}


def file_type(suffix):
    """Identify file data as being a minilogue xd, minilogue og, or prologue patch by
    suffix and whether it is a single patch or collection.

    Args:
        suffix (str): One of
            ".mnlgxdprog", ".mnlgprog", ".prlgprog"
            ".mnlgxdpreset", ".mnlgpreset", ".prlgpreset",
            ".mnlgxdlib", ".mnlglib", ".prlglib"
    Returns:
        str: One of {"xd", "og", "prologue"}
        bool: True iff suffix is a collection

    """
    assert suffix in lib_suffixes | patch_suffixes
    logue_type = None
    if suffix in {".mnlgxdpreset", ".mnlgxdlib", ".mnlgxdprog"}:
        logue_type = "xd"
    if suffix in {".mnlgpreset", ".mnlglib", ".mnlgprog"}:
        logue_type = "og"
    if suffix in {".prlgpreset", ".prlglib", ".prlgprog"}:
        logue_type = "prologue"
    if suffix in lib_suffixes:
        collection = True
    else:
        collection = False
    return logue_type, collection


def patch_type(data):
    """Identify patch data as being a minilogue xd, minilogue og, or prologue patch by
    attempting to read from locations valid only for the prologue, then if that fails,
    the xd. xd, og, and Prologue patches are 1780, 448, and 336 bytes long

    Args:
        data (packed binary string): patch data

    Returns:
        str: One of {"xd", "og", "prologue"}

    """
    try:
        struct.unpack_from("B", data, offset=1023)
        return "xd"
    except struct.error:
        pass

    try:
        struct.unpack_from("B", data, offset=447)
        return "og"
    except struct.error:
        pass

    try:
        struct.unpack_from("B", data, offset=335)
        return "prologue"
    except struct.error:
        pass


def id_from_name(zipobj, name):
    """Searches patches contained in the zipped object finding the 0-based index of the
    matching named patch.

    Args:
        zipobj (ZipFile instance): zipped patches object
        name (str): patch name to match

    Returns:
        int: 0-based matched index

    Raises:
        ValueError: If name is not found

    """
    for i, p in enumerate(zipread_progbins(zipobj)):
        patchdata = zipobj.read(p)
        prgname = program_name(patchdata)
        if prgname != name:
            continue
        ident = i + 1
        break
    else:
        raise ValueError("No patch named " + name)
    return ident


def zipread_all_prog_info(zipobj):
    """Returns an ordered list of all the contained file block data as a dictionary,
    keyed by the .bin_info name

    Args:
        zipobj (zipfile object): patch file or library zipfile object

    Returns:
        dict: described above

    """
    names = zipobj.namelist()
    bin_names = sorted(fnmatch.filter(names, "*.prog_bin"))
    info_names = sorted(fnmatch.filter(names, "*.prog_info"))
    all_prog_info = {}
    for bin_name, info_name in zip(bin_names, info_names):
        xml = zipobj.read(info_name).decode()
        tree = ET.fromstring(xml)
        prog_text_dict = {i.tag:i.text for i in tree.iter()}
        all_prog_info[bin_name] = prog_text_dict
    return all_prog_info


def zipread_progbins(zipobj):
    """Returns an ordered list of all the contained .prog_bin patch block names

    Args:
        zipobj (zipfile object): patch file or library zipfile object

    Returns:
        list: ordered list

    """
    names = zipobj.namelist()
    names = sorted(fnmatch.filter(names, "*.prog_bin"))
    return names


def author_copyright_from_presetinformation_xml(zipobj):
    """Parses a PresetInformation.xml file block from a preset pack and returns the
    Author and Copyright fields

    <minilogue_Preset>
      <DataID></DataID>
      <Name>Patches</Name>
      <Author>Anne Author</Author>
      <Date></Date>
      <Prefix></Prefix>
      <Copyright>Anne Author</Copyright>
    </minilogue_Preset>

    Args:
        zipobj (zipfile object): patch file or library zipfile object

    Returns:
        (str) : author
        (str) : copyright

    """
    xml = zipobj.read("PresetInformation.xml").decode()
    tree = ET.fromstring(xml)
    author = tree.find("Author").text
    copyright = tree.find("Copyright").text
    return author, copyright


def program_name(data):
    """Returns the patch name

    Args:
        data (packed binary string): patch data

    Returns:
        str: name

    """
    name = struct.unpack_from("12s", data, offset=4)[0].decode("utf-8").strip("\x00")
    return name


def signed_shift(val, shift):
    """Bit shifts the value val. +ve values shift left and -ve shift right.

    Args:
        val (int): Value to be shifted
        shift (int): Number of bits to shift by

    Returns:
        int: Shifted result

    """
    return val << shift if shift >= 0 else val >> -shift


def parse_patchdata(data):
    """Decodes a minilogue og or xd format packed binary patch

    Args:
        data (packed binary): minilogue og patch

    Returns:
        Patch: normalised/decoded patch

    """
    patch = Patch()
    patch.minilogue_type = patch_type(data)

    if patch.minilogue_type == "xd":
        patch_struct = xd.minilogue_xd_patch_struct
        tuple_decoder = xd.patch_translation_value
    else:
        patch_struct = og.minilogue_og_patch_struct
        tuple_decoder = og.patch_value

    offset = 0
    for m in patch_struct:
        f = tuple_decoder(*m)
        value = struct.unpack_from(f.type, data, offset=offset)[0]
        setattr(patch, f.name, value)
        offset += struct.calcsize(f.type)

    return patch
