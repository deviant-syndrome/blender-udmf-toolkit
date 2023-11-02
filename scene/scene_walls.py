import bmesh
import bpy

from .geometry_vert import draw_walls
from .material_nodes import WallMaterialNodeParameters
from .mesh_lifecycle import MeshObjectLifecycle
from .metadata import assign_custom_attributes
from .materials_walls import create_material_for_face_new
from .texture_utils import set_default_uv_on_mesh


def create_walls(graph, udmf_map):
    with MeshObjectLifecycle("UDMF_Walls") as (bm, mesh):
        face_metadata = draw_walls(graph, udmf_map, bm)
        walls_mesh = mesh

    return face_metadata, walls_mesh, bpy.data.objects["UDMF_Walls"]


def texture_walls(textures_data, walls_mesh, walls_obj):
    for face_index, _ in enumerate(walls_mesh.polygons):
        set_default_uv_on_mesh(walls_mesh, face_index)

    bm = bmesh.new()
    bm.from_mesh(walls_obj.data)
    bm.faces.ensure_lookup_table()

    data_layers = {
        "sidedef_index": bm.faces.layers.int.get("sidedef_index"),
        "texture_type": bm.faces.layers.string.get("texture_type"),
    }

    for face_index, texture_data in textures_data.items():
        face = bm.faces[face_index]
        material = create_material_for_face_new(
            walls_obj,
            face,
            face_index,
            WallMaterialNodeParameters(texture_data, data_layers),
        )
        face.material_index = walls_obj.data.materials.find(material.name)

    bm.to_mesh(walls_obj.data)
    bm.free()


def add_walls_metadata(obj, face_metadata):
    for face_index, data in face_metadata.items():
        face_specific_data = {
            "sidedef_index": data["sidedef_index"],
            "texture_type": data["wall_type"],
        }
        assign_custom_attributes(obj, face_index, face_specific_data)


def wall_operations(graph, udmf_map):
    walls_metadata, walls_mesh, walls_obj = create_walls(graph, udmf_map)

    walls_obj["udmf_type"] = "walls"
    add_walls_metadata(walls_obj, walls_metadata)
    texture_walls(
        {
            face_index: data["texture_data"]
            for face_index, data in walls_metadata.items()
        },
        walls_mesh,
        walls_obj,
    )
