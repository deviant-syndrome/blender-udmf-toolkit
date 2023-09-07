import bpy


def get_addon_package():
    """Warning: This function is not safe to use in all cases. It is only safe to use if the current package is one
    level down from the root package. Blender addon-preferences API requires the key to be the root package name"""
    current_package = __package__
    parent_package = ".".join(current_package.split(".")[:-1])
    return parent_package


def get_baked_texture_path(texture_name):
    preferences = bpy.context.preferences.addons[get_addon_package()].preferences
    baked_texture_folder_path = preferences.baked_texture_folder_path
    return baked_texture_folder_path + texture_name + ".png"


def generate_texture_name(sidedef, texture_type):
    """Generate the texture filename based on sidedef and texture_type."""
    return f"M01{sidedef}{texture_type}"
