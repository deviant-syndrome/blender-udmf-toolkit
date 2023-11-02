import bpy
import unittest

from udmf_blender_addon.scene.props import set_props_on_import


class TestImportProps(unittest.TestCase):
    def setUp(self):
        # Create a new scene so we don't change properties on the default one
        self.test_scene = bpy.data.scenes.new("TestScene")
        bpy.context.window.scene = self.test_scene

    def tearDown(self):
        # Clean up after tests by removing the test scene
        bpy.data.scenes.remove(self.test_scene)

    def test_set_props_with_values(self):
        options = {"scale": 0.05, "original_pwad": "path/to/pwad"}
        set_props_on_import(options)
        self.assertAlmostEqual(self.test_scene.map_scale, 0.05, places=6)
        self.assertEqual(self.test_scene.original_pwad, "path/to/pwad")

    def test_set_props_with_defaults(self):
        options = {}
        set_props_on_import(options)
        self.assertAlmostEqual(self.test_scene.map_scale, 0.01, places=6)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=True)
