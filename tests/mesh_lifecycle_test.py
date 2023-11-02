import bpy
import unittest
from udmf_blender_addon.scene.mesh_lifecycle import MeshObjectLifecycle


class TestMeshObjectLifecycle(unittest.TestCase):

    def setUp(self):
        # Ensure we're in OBJECT mode
        if bpy.context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

    def test_mesh_scaling(self):
        # Set the map scale
        expected_scale = 2.0
        bpy.context.scene.map_scale = expected_scale

        object_name = "TestObject"

        with MeshObjectLifecycle(object_name) as (bm, mesh):
            # Create a simple polygon (triangle) using BMesh
            bm.verts.new((0, 0, 1))
            bm.verts.new((1, 0, 0))
            bm.verts.new((0, 1, 0))
            bm.faces.new(bm.verts)

        # After exiting the block, the object is created and linked to the scene
        obj = bpy.data.objects[object_name]

        # Assert that the dimensions of the object's mesh are properly scaled
        for dimension in obj.dimensions:
            self.assertAlmostEqual(dimension, expected_scale, places=6)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
