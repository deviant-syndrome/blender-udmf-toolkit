import bpy
from .materials import make_faces_transparent_except, restore_original_materials
from .utils import get_baked_texture_path
from ..scene.metadata import get_face_custom_attribute


def adjust_render_settings_for_wall(obj, face_index):
    wall = obj.data.polygons[face_index]

    # Calculate the dimensions of the wall in world space
    # Assuming the wall is a quadrilateral
    v0 = obj.data.vertices[wall.vertices[0]].co
    v1 = obj.data.vertices[wall.vertices[1]].co
    v3 = obj.data.vertices[wall.vertices[3]].co

    width = (obj.matrix_world @ v1 - obj.matrix_world @ v0).length
    height = (obj.matrix_world @ v3 - obj.matrix_world @ v0).length

    # Set the render resolution
    bpy.context.scene.render.resolution_x = int(width * 100)  # Scaling factor can be adjusted
    bpy.context.scene.render.resolution_y = int(height * 100)  # Scaling factor can be adjusted


def render_wall_face(obj, face_index):
    """
    Renders a specific face by making other faces transparent.
    """
    # Make all faces transparent except the face_index
    original_materials = make_faces_transparent_except(obj, face_index)

    # Setup camera and render the image
    cam_obj = bpy.data.objects["WallBakeCam"]
    bpy.context.scene.camera = cam_obj

    adjust_render_settings_for_wall(obj, face_index)

    sidedef, texture_type = get_face_custom_attribute(obj, face_index)
    tex_name = generate_texture_name(sidedef, texture_type.upper())
    bpy.context.scene.render.filepath = get_baked_texture_path(tex_name)
    bpy.ops.render.render(write_still=True)

    # Revert materials to their original state
    restore_original_materials(obj, original_materials)
