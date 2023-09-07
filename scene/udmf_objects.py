import io

import bmesh
import bpy

from .geometry_horiz import draw_floors
from .geometry_vert import draw_walls
from .mesh_lifecycle import MeshObjectLifecycle
from .texture_utils import assign_texture_to_face
from .traversal import create_graph
from ..libs import write_udmf_map


def clean_resources():
    # Remove all images
    for img in bpy.data.images:
        bpy.data.images.remove(img)

    # Remove all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


def create_walls(graph, udmf_map):
    with MeshObjectLifecycle("UDMF_Walls") as (bm, mesh):
        face_metadata = draw_walls(graph, udmf_map, bm)
        bmesh.ops.scale(bm, vec=(0.01, 0.01, 0.01), verts=bm.verts)
        walls_mesh = mesh

    return face_metadata, walls_mesh, bpy.data.objects["UDMF_Walls"]


def texture_walls(texture_names, walls_mesh, walls_obj):
    for face_index, texture_name in texture_names.items():
        face = walls_mesh.polygons[face_index]
        assign_texture_to_face(face, texture_name, walls_obj, face_index, walls_mesh)


def add_walls_metadata():
    pass


def create_floors(graph, udmf_map):
    with MeshObjectLifecycle("UDMF_Floors") as (bm, mesh):
        draw_floors(bm, graph, udmf_map)
        floors_mesh = mesh
        bmesh.ops.scale(bm, vec=(0.01, 0.01, 0.01), verts=bm.verts)
    return floors_mesh, bpy.data.objects["UDMF_Floors"]


def texture_floors():
    pass


def add_sector_metadata():
    pass


def embed_udmf_map(udmf_map):
    with io.StringIO() as f:
        write_udmf_map(udmf_map, f)
        data = f.getvalue()
    udmf_text_block = bpy.data.texts.new(name="EmbeddedUDMF")
    udmf_text_block.from_string(data)


def create_udmf_scene(udmf_map):
    clean_resources()
    graph = create_graph(udmf_map)
    walls_metadata, walls_mesh, walls_obj = create_walls(graph, udmf_map)
    texture_walls({face_index: data["texture_name"] for face_index, data in walls_metadata.items()},
                  walls_mesh, walls_obj)

    create_floors(graph, udmf_map)

    embed_udmf_map(udmf_map)
