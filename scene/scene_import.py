import bpy

from .props import set_props_on_import
from .scene_floors import FloorOperations, CeilingOperations
from .scene_walls import wall_operations
from .traversal import create_graph
from ..utils import embed_udmf_map


def clean_resources():
    # Remove all images
    for img in bpy.data.images:
        bpy.data.images.remove(img)

    # Remove all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


def create_udmf_scene(udmf_map, options):
    clean_resources()
    graph = create_graph(udmf_map)

    FloorOperations(graph, udmf_map).execute()
    CeilingOperations(graph, udmf_map).execute()

    wall_operations(graph, udmf_map)

    embed_udmf_map(udmf_map)
    set_props_on_import(options)
