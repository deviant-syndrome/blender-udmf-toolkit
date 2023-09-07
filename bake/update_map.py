from .utils import generate_texture_name
from ..scene.metadata import get_face_custom_attribute
import bpy


def update_udmf_sidedef_texture(udmf_map, sidedef_index, new_texture_name):
    """Update the texturemiddle property of a sidedef in a UDMF map."""
    udmf_map.sidedefs[sidedef_index].texturemiddle = new_texture_name
    udmf_map.sidedefs[sidedef_index].offsetx = 0


def update_udmf(obj, udmf_map):
    for face_index in range(len(obj.data.polygons)):
        sidedef, texture_type = get_face_custom_attribute(bpy.context.object, face_index)
        if sidedef == -1:
            continue;
        # Generate the texture filename
        texture_filename = generate_texture_name(sidedef, texture_type)

        # Update the UDMF map
        update_udmf_sidedef_texture(udmf_map, sidedef, texture_filename)
