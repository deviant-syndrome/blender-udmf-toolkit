import bpy
import unittest

from udmf_blender_addon.utils.helpers import load_map_from_pwad

from udmf_blender_addon.scene import create_udmf_scene


class TestLoadBasicWad(unittest.TestCase):
    def setUp(self):
        # Create a new scene so we don't change properties on the default one
        self.test_scene = bpy.data.scenes.new("TestScene")
        bpy.context.window.scene = self.test_scene

    def tearDown(self):
        # Clean up after tests by removing the test scene
        bpy.data.scenes.remove(self.test_scene)

    def test_load_wad(self):
        udmf_map = load_map_from_pwad("testdata/basic.wad")
        create_udmf_scene(udmf_map, {})
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=True)
