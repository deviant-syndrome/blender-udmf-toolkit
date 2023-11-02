import bpy
import bmesh
import unittest

from udmf_blender_addon.scene.tiling_uv_layer import uv_map_sector_by_bounding_box
from udmf_blender_addon.scene.metadata import assign_custom_attributes


class TestUVMapping(unittest.TestCase):
    def setUp(self):
        # Define the 5 vertices of the polygon
        vertices = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0.5, 1.5, 0)]

        # Define the three triangles using vertex indices
        faces = [(0, 1, 2), (0, 2, 3), (2, 3, 4)]

        # Create a new mesh
        mesh = bpy.data.meshes.new(name="TestMesh")

        # Create a new object using the mesh
        obj = bpy.data.objects.new("TestObject", mesh)

        # Link it to the scene
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Construct the bmesh and assign it to the mesh
        bm = bmesh.new()
        for v in vertices:
            bm.verts.new(v)
        bm.verts.ensure_lookup_table()
        for f in faces:
            bm.faces.new([bm.verts[i] for i in f])

        bm.to_mesh(mesh)
        bm.free()

        # Store the object for later use
        self.obj = obj

        assign_custom_attributes(obj, 0, {"sector_index": 0})

    def tearDown(self):
        # Deselect all objects
        bpy.ops.object.select_all(action="DESELECT")

        # Select the object
        self.obj.select_set(True)

        # Delete the object
        bpy.ops.object.delete()

        # Optionally, remove mesh data too
        mesh = bpy.data.meshes.get("TestMesh")
        if mesh is not None:
            bpy.data.meshes.remove(mesh)

        # Nullify the reference
        self.obj = None

    def test_offset_face_layers(self):
        expected_bbox = {0: (0, 0), 1: (2, 2), 2: (0, 0)}
        # Set map scale
        map_scale = 0.5
        bpy.context.scene.map_scale = map_scale

        sector_faces_dict = {0: [1]}
        uv_map_sector_by_bounding_box(self.obj, sector_faces_dict)

        bm = bmesh.new()
        bm.from_mesh(self.obj.data)

        width_layer = bm.faces.layers.int.get("bbox_width")
        height_layer = bm.faces.layers.int.get("bbox_height")

        for face in bm.faces:
            # Example assertions - replace with your own logic
            expected_w, expected_h = expected_bbox.get(face.index)

            assert (
                face[width_layer] == expected_w
            ), f"Face {face.index} has invalid width: {face[width_layer]}"
            assert (
                face[height_layer] == expected_h
            ), f"Face {face.index} has invalid height: {face[height_layer]}"

        # Clean up
        bm.free()

    def test_uv_map_sector_by_bounding_box(self):
        sector_faces_dict = {0: [1]}
        expected_uvs = {
            3: (0.0, 0.0),
            4: (1.0, 1.0),
            5: (0.0, 1.0),
        }
        # Set map scale
        map_scale = 2.0
        bpy.context.scene.map_scale = map_scale

        # Call the uv_map_sector_by_bounding_box function
        uv_map_sector_by_bounding_box(self.obj, sector_faces_dict)

        # Validate the UV coordinates
        # Retrieve the UV map
        uv_layer = self.obj.data.uv_layers.active.data

        # Loop over the sectors and faces and check the UVs
        for sector_idx, face_indexes in sector_faces_dict.items():
            for face_idx in face_indexes:
                # Retrieve the polygon (face)
                polygon = self.obj.data.polygons[face_idx]

                # For each vertex in the polygon, check the UV coordinates
                for li in range(polygon.loop_total):
                    loop_index = polygon.loop_start + li
                    uv = uv_layer[loop_index].uv

                    # Calculate the expected UVs based on your algorithm and map scale
                    expected_u = expected_uvs[loop_index][0]
                    expected_v = expected_uvs[loop_index][1]

                    self.assertAlmostEqual(uv.x, expected_u, places=6)
                    self.assertAlmostEqual(uv.y, expected_v, places=6)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
