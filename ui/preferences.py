import bpy


def get_addon_package():
    """Warning: This function is not safe to use in all cases. It is only safe to use if the current package is one
    level down from the root package. Blender addon-preferencies API requires the key to be the root package name"""
    current_package = __package__
    parent_package = ".".join(current_package.split(".")[:-1])
    return parent_package


class UDMFToolkitAddonPreferences(bpy.types.AddonPreferences):
    """Preferences for the UDMF Toolkit Addon. This class has to be placed here, because the package name is used as the
    bl_idname for the addon. This class is used to store the preferences for the addon"""

    bl_idname = get_addon_package()  # This should match the name of your add-on

    base_texture_folder_path: bpy.props.StringProperty(
        name="Base texture directory",
        description="Directory with textures from base IWAD and your mod",
        subtype='FILE_PATH',
    )

    some_boolean: bpy.props.BoolProperty(
        name="Some Boolean",
        default=True,
    )

    def draw(self, context):
        layout = self.layout

        layout.label(text="Path to External Tool:")
        layout.prop(self, "base_texture_folder_path")

        layout.label(text="Some Boolean Preference:")
        layout.prop(self, "some_boolean")


def register():
    bpy.utils.register_class(UDMFToolkitAddonPreferences)


def unregister():
    bpy.utils.unregister_class(UDMFToolkitAddonPreferences)
