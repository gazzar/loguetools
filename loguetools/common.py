import struct
from types import SimpleNamespace
import fnmatch
from loguetools import og, xd


class Patch(SimpleNamespace):
    """A simple container class for patch data."""

    pass


def patch_type(data):
    """Identify patch data as being a minilogue xd or og patch by attempting to read
    from a location that is only valid for the xd.

    Args:
        data (packed binary string): patch data

    Returns:
        str: One of {"xd", "og"}

    """
    try:
        struct.unpack_from("B", data, offset=1000)
        minilogue_type = "xd"
    except struct.error:
        minilogue_type = "og"
    return minilogue_type


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
    for i, p in enumerate(zip_progbins(zipobj)):
        patchdata = zipobj.read(p)
        prgname = program_name(patchdata)
        if prgname != name:
            continue
        ident = i + 1
        break
    else:
        raise ValueError("No patch named " + name)
    return ident


def zip_progbins(zipobj):
    """Returns an ordered list of all the contained .prog_bin patch block names

    Args:
        zipobj (zipfile object): patch file or library zipfile object

    Returns:
        list: ordered list

    """
    names = zipobj.namelist()
    names = sorted(fnmatch.filter(names, "*.prog_bin"))
    return names


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
