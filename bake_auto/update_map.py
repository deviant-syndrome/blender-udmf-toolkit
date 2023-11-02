from io import StringIO

import bpy

from .utils import (
    generate_texture_name,
    generate_floor_texture_name,
    generate_ceiling_texture_name,
)
from ..libs import load_udmf_map


def update_udmf_sidedef_texture(
    udmf_map, sidedef_index, new_texture_name, texture_type
):
    """Update the texturemiddle property of a sidedef in a UDMF map."""
    if texture_type == "M":
        udmf_map.sidedefs[sidedef_index].texturemiddle = new_texture_name
        udmf_map.sidedefs[sidedef_index].offsetx_mid = 0
        udmf_map.sidedefs[sidedef_index].offsety_mid = 0
    elif texture_type == "U":
        udmf_map.sidedefs[sidedef_index].textureupper = new_texture_name
        udmf_map.sidedefs[sidedef_index].offsetx_top = 0
        udmf_map.sidedefs[sidedef_index].offsety_top = 0
    elif texture_type == "L":
        udmf_map.sidedefs[sidedef_index].texturebottom = new_texture_name
        udmf_map.sidedefs[sidedef_index].offsetx_bottom = 0
        udmf_map.sidedefs[sidedef_index].offsety_bottom = 0


def update_udmf_flat_texture(
    udmf_map, sector_index, texture_type, new_texture_name, panning_x, panning_y
):
    """
    Update the texture property of a sector in a UDMF map.
    texture_type: either 'floor' or 'ceiling'
    """
    if texture_type not in ["floor", "ceiling"]:
        raise ValueError("texture_type must be either 'floor' or 'ceiling'")

    setattr(udmf_map.sectors[sector_index], f"texture{texture_type}", new_texture_name)
    setattr(udmf_map.sectors[sector_index], f"xpanning{texture_type}", panning_x)
    setattr(udmf_map.sectors[sector_index], f"ypanning{texture_type}", panning_y)


def update_udmf_walls(obj, udmf_map):
    for material in obj.data.materials:
        if material.name.endswith("_fallback"):
            continue
        sidedef = material["sidedef_index"]
        texture_type = material["texture_type"].decode("utf-8")
        texture_filename = generate_texture_name(sidedef, texture_type)
        update_udmf_sidedef_texture(udmf_map, sidedef, texture_filename, texture_type)


def update_udmf_sector_flats(obj, udmf_map, floor_ceil_type, name_func):
    for material in obj.data.materials:
        if material.name.endswith("_fallback"):
            continue
        sector_index = material["sector_index"]
        panning_x = material["offset_x"]
        panning_y = material["offset_y"]
        update_udmf_flat_texture(
            udmf_map,
            sector_index,
            floor_ceil_type,
            name_func(sector_index),
            panning_x,
            panning_y,
        )


def update_udmf(obj, udmf_map):
    if obj["udmf_type"] == "walls":
        update_udmf_walls(obj, udmf_map)
    elif obj["udmf_type"] == "floors":
        update_udmf_sector_flats(obj, udmf_map, "floor", generate_floor_texture_name)
    elif obj["udmf_type"] == "ceilings":
        update_udmf_sector_flats(
            obj, udmf_map, "ceiling", generate_ceiling_texture_name
        )


def create_updated_map(obj):
    # Get the UDMF map
    udmf_map = load_udmf_map(StringIO(bpy.data.texts["EmbeddedUDMF"].as_string()))
    # Update the UDMF map
    update_udmf(obj, udmf_map)

    return udmf_map
