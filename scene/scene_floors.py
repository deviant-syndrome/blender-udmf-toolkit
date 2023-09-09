from collections import defaultdict

import bmesh
import bpy

from .geometry_horiz import draw_floors, draw_ceilings
from .materials_floors import create_material_for_sector_floor, create_material_for_sector_ceiling
from .mesh_lifecycle import MeshObjectLifecycle
from .metadata import assign_custom_attributes
from .tiling_uv_layer import uv_map_sector_by_bounding_box


class FloorOperations:
    def __init__(self, graph, udmf_map):
        self.graph = graph
        self.udmf_map = udmf_map

    def draw(self, bm):
        return draw_floors(bm, self.graph, self.udmf_map)

    def create_material(self, bm, texture_name, obj, layers):
        create_material_for_sector_floor(bm, texture_name, obj, layers)

    def create_name(self):
        return "UDMF_Floors"

    def create_type(self):
        return "floors"

    def create_geometry(self):
        with MeshObjectLifecycle(self.create_name()) as (bm, mesh):
            floors_metadata = self.draw(bm)
            floors_mesh = mesh
            bmesh.ops.scale(bm, vec=(0.01, 0.01, 0.01), verts=bm.verts)
        return floors_metadata, floors_mesh, bpy.data.objects[self.create_name()]

    def add_metadata(self, floors_obj, floor_metadata):
        sector_faces_dict = defaultdict(list)

        for face_index, data in floor_metadata.items():
            sector_specific_data = {
                "sector_index": data["sector_index"],
            }
            sector_faces_dict[data["sector_index"]].append(face_index)
            assign_custom_attributes(floors_obj, face_index, sector_specific_data)
        return sector_faces_dict

    def texture(self, texture_names, floors_mesh, floors_obj):
        bm = bmesh.new()
        bm.from_mesh(floors_obj.data)

        sector_index_layer = bm.faces.layers.int.get("sector_index")
        if not sector_index_layer:
            raise ValueError("sector_index attribute not found!")

        layers = {
            "width": bm.faces.layers.int.get("bbox_width"),
            'height': bm.faces.layers.int.get("bbox_height"),
            "offset_x": bm.faces.layers.int.get("offset_x"),
            "offset_y": bm.faces.layers.int.get("offset_y"),
            "sector_index": sector_index_layer
        }
        sector_faces = defaultdict(list)
        sector_texture_names = {}
        for idx, face in enumerate(bm.faces):
            sector_idx = face[sector_index_layer]
            sector_texture_names[sector_idx] = texture_names[idx]
            sector_faces[sector_idx].append(face)

        # Create materials for each sector's faces
        for idx, faces in enumerate(sector_faces.values()):
            self.create_material(faces, sector_texture_names[idx], floors_obj, layers)

        bm.to_mesh(floors_obj.data)
        bm.free()

    def execute(self):
        floor_metadata, floors_mesh, floors_obj = self.create_geometry()
        floors_obj["udmf_type"] = self.create_type()
        sector_faces_dict = self.add_metadata(floors_obj, floor_metadata)
        uv_map_sector_by_bounding_box(floors_obj, sector_faces_dict)
        self.texture({face_index: data["flat_texture"] for face_index, data in floor_metadata.items()}, floors_mesh,
                     floors_obj)


class CeilingOperations(FloorOperations):
    def create_material(self, bm, texture_name, obj, layers):
        create_material_for_sector_ceiling(bm, texture_name, obj, layers)

    def create_name(self):
        return "UDMF_Ceilings"

    def create_type(self):
        return "ceilings"

    def draw(self, bm):
        return draw_ceilings(bm, self.graph, self.udmf_map)
