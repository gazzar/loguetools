import xml.etree.ElementTree as ET
from xml.dom import minidom
import struct
from types import SimpleNamespace
import fnmatch
from loguetools import og, xd, prologue, monologue
from loguetools import version
import hashlib
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
    'og1': '9d2fd7e2e97edc87306d8360eb881534',
    'og2': '3c2611b06c1fbb118269a0d9ca764b34',
    'xd': 'fd6940f683f8b69966fc3fd08bbb5ee3',
    'prologue': 'a4fa5be24cb09c35a91e81ef2bbf71af',
    'monologue1': 'c5594cd3363607bdfbf0803e0ae05b98', #factory preset
    'monologue2': '7863e5bf4a351456155b549c24eca178',
    'kk': 'c2f4605587c157c52c41c9fac56fc5d3',
}
def is_init_patch(flavour, hash):
    """True iff the hash matches the Init Program md5 checksum for the corresponding flavour

    Args:
        flavour (str): "xd", "og", "prologue"
        hash (bool): md5 checksum string

    Returns:
        bool: True iff Init Program matched

    """
    assert flavour in valid_flavours

    if flavour == "og":
        return hash in {init_program_hashes["og1"], init_program_hashes["og2"]}
    elif flavour == "monologue":
        return hash in {init_program_hashes["monologue1"], init_program_hashes["monologue2"]}
    else:
        return init_program_hashes[flavour] == hash


def is_init_program_name(name):
    return name.replace(' ', '').strip() == "InitProgram"


valid_flavours = {"xd", "og", "prologue", "monologue", "kk"}
flavour_to_product = {
        "xd": "xd",
        "og": "minilogue",
        "prologue": "prologue",
        "monologue": "monologue",
        "kk": "KingKORG",
    }


def prog_info_template_xml(flavour, programmer=None, comment=None, copyright=None):
    """xml template for Prog_nnn.prog_info xml patch elements

    Args:
        flavour: "xd", "og", "prologue", "monologue", "kk"
        programmer (str), default=None :  programmer field text
        comment (str), default=None : comment field text
        copyright (str), default=None : copyright field text

    Returns:
        str: formatted xml

    """
    assert flavour in valid_flavours

    # create the file structure
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


def fileinfo_xml(flavour, non_init_patch_ids, force_preset):
    """Build FileInformation.xml metadata file.

    Args:
        flavour: "xd", "og", "prologue", "monologue", "kk"
        non_init_patch_ids (list of ints): 0-based list of non-Init-Program patches
        force_preset: preset file output

    Returns:
        str: formatted xml

    """
    assert flavour in valid_flavours

    # create the file structure
    root = ET.Element("KorgMSLibrarian_Data")
    product = ET.SubElement(root, "Product")
    product.text = {
        "monologue":"monologue",
        "xd":"minilogue xd",
        "og":"minilogue",
        "prologue":"prologue",
        "monologue":"monologue",
        "kk":"KingKORG",
    }[flavour]
    contents = ET.SubElement(root, "Contents")

    contents.set("NumProgramData", str(len(non_init_patch_ids)))
    if force_preset:
        contents.set("NumPresetInformation", "1")
        ET.SubElement(ET.SubElement(contents, "PresetInformation"), "File").text = "PresetInformation.xml"
    else:
        contents.set("NumPresetInformation", "0")
    contents.set("NumTuneScaleData", "0")
    contents.set("NumTuneOctData", "0")

    if len(non_init_patch_ids) <= 1 or force_preset:
        if flavour == "prologue":
            contents.set("NumLivesetData", "0")
        elif flavour != "monologue":
            contents.set("NumFavoriteData", "0")
    else:
        if flavour == "prologue":
            contents.set("NumLivesetData", "1")
            fave = ET.SubElement(contents, "LivesetData")
            fave_info = ET.SubElement(fave, "File")
            fave_info.text = "LivesetData.lvs_data"
        elif flavour != "monologue":
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


def presetinfo_xml(flavour, dataid, name, author, version, numofprog, date, prefix, copyright):
    """Build PresetInformation.xml metadata file.

    Args:
        flavour:
        force_preset: preset file output

    Returns:
        str: formatted xml

    """
    # create the file structure
    root = ET.Element(flavour_to_product[flavour] + "_Preset")
    ET.SubElement(root, "DataID").text = dataid
    ET.SubElement(root, "Name").text = name
    ET.SubElement(root, "Author").text = author
    ET.SubElement(root, "Version").text = version
    ET.SubElement(root, "NumOfProg").text = numofprog
    ET.SubElement(root, "Date").text = date
    ET.SubElement(root, "Prefix").text = prefix
    ET.SubElement(root, "Copyright").text = copyright

    # https://stackoverflow.com/a/3095723
    formatted_xml = minidom.parseString(
        ET.tostring(root, encoding="utf-8", method="xml")
    ).toprettyxml(indent="  ")

    return formatted_xml


presuffixes = [".mnlgxd", ".mnlg", ".prlg", ".molg", ".kk"]
patch_suffixes = {i + "prog" for i in presuffixes}
lib_suffixes = {i + "lib" for i in presuffixes}
preset_suffixes = {i + "preset" for i in presuffixes}
collection_suffixes = lib_suffixes | preset_suffixes
all_suffixes = collection_suffixes | patch_suffixes

postsuffixes = ["prog", "lib", "preset"]
xd_suffixes = {".mnlgxd" + i for i in postsuffixes}
og_suffixes = {".mnlg" + i for i in postsuffixes}
prologue_suffixes = {".prlg" + i for i in postsuffixes}
monologue_suffixes = {".molg" + i for i in postsuffixes}
kk_suffixes = {".kk" + i for i in postsuffixes}
suffixes_dict = {
        "xd":xd_suffixes,
        "og":og_suffixes,
        "prologue":prologue_suffixes,
        "monologue":monologue_suffixes,
        "kk":kk_suffixes,
    }

def file_type(suffix):
    """Identify file data as being a minilogue xd, minilogue og, or prologue patch by
    suffix and whether it is a single patch or collection.

    Args:
        suffix (str): e.g. ".mnlgxdprog", ".mnlgprog", ".prlgpreset", ".molglib"
    Returns:
        str: One of {"xd", "og", "prologue", "monologue", "kk"}
        bool: True iff suffix is a collection

    """
    assert suffix in all_suffixes
    logue_type = None
    for i in suffixes_dict:
        if suffix in suffixes_dict[i]:
            logue_type = i

    if suffix in collection_suffixes:
        collection = True
    else:
        collection = False
    return logue_type, collection


def patch_type(data):
    """Identify patch data flavour.
    Attempts to distinguish by using a combination of approaches:
    1. Read from locations valid only for some synth flavours.
       xd, og, monologue, prologue, and kingkorg patches are respectively
       1024, 448, 448, 336, 320 bytes long.
    2. Init Program patches are incorrectly initialised on the monologue and contain
       SEQD at 96~99. Check for this case based on hash.
    3. To distinguish between og and monologue, look for the SEQD string at the
       following locations; og: 96~99, monologue: 48~51

    Args:
        data (packed binary string): patch data

    Returns:
        str: One of {"xd", "og", "monologue", "prologue", "kk"}

    """
    try:
        struct.unpack_from("B", data, offset=1023)
        return "xd"
    except struct.error:
        pass

    try:
        struct.unpack_from("B", data, offset=447)
        if struct.unpack_from("4s", data, offset=0x30)[0].decode('ansi') == 'SEQD':
            return "monologue"
        else:
            return "og"
    except struct.error:
        pass

    try:
        struct.unpack_from("B", data, offset=447)
        # if we didn't raise an exception by this point, it's an og or monologue
        hash = hashlib.md5(data).hexdigest()
        if is_init_patch("monologue", hash):
            # An incorrectly initialised monologue Init Program patch
            return "monologue"
        if struct.unpack_from("4s", data, offset=48)[0] == b"SEQD":
            return "monologue"
        if struct.unpack_from("4s", data, offset=96)[0] == b"SEQD":
            return "og"
    except struct.error:
        pass

    try:
        struct.unpack_from("B", data, offset=335)
        return "prologue"
    except struct.error:
        pass

    try:
        struct.unpack_from("B", data, offset=319)
        return "kk"
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
        flavour = patch_type(patchdata)
        prgname = program_name(patchdata, flavour)
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

def all_from_presetinformation_xml(zipobj):
    """Parses a PresetInformation.xml file block from a preset pack and returns all
    fields

    Args:
        zipobj (zipfile object): patch file or library zipfile object

    Returns:
        (str) : dataid
        (str) : name
        (str) : author
        (str) : version
        (str) : numofprog
        (str) : date
        (str) : prefix
        (str) : copyright

    """
    xml = zipobj.read("PresetInformation.xml").decode()
    tree = ET.fromstring(xml)
    dataid = tree.find("DataID").text
    name = tree.find("Name").text
    author = tree.find("Author").text
    version = tree.find("Version").text
    numofprog = tree.find("NumOfProg").text
    date = tree.find("Date").text
    prefix = tree.find("Prefix").text
    copyright = tree.find("Copyright").text
    return dataid, name, author, version, numofprog, date, prefix, copyright


def program_name(data, flavour):
    """Returns the patch name

    Args:
        data (packed binary string): patch data
        flavour: "xd", "og", "prologue", "monologue", "kk"

    Returns:
        str: name

    """
    assert flavour in valid_flavours

    if flavour == "kk":
        offset = 0
    else:
        offset = 4
    name = struct.unpack_from("12s", data, offset)[0].decode("utf-8").partition("\x00")[0].strip("\x00")
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
    elif patch.minilogue_type == "prologue":
        patch_struct = prologue.patch_struct
        tuple_decoder = prologue.patch_value
    elif patch.minilogue_type == "monologue":
        patch_struct = monologue.patch_struct
        tuple_decoder = monologue.patch_value
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
