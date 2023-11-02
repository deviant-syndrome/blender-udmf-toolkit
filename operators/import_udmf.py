import bpy

from ..libs import load_udmf_map
from ..scene import create_udmf_scene
from ..utils import load_map_from_pwad


def popup_error_message(error_message):
    bpy.ops.wm.centered_popup(
        "INVOKE_DEFAULT", message="Error importing file:\n {}".format(error_message)
    )


class IMPORT_OT_udmf(bpy.types.Operator):
    bl_idname = "import_scene.udmf"
    bl_label = "Import UDMF"
    bl_options = {"REGISTER", "UNDO"}

    scale: bpy.props.FloatProperty(name="Scale", default=0.01)

    # Define the filepath property for the file browser
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def get_options(self):
        return {"scale": self.scale, "original_pwad": self.filepath}

    def execute(self, context):
        # Your import logic goes here, use self.filepath for the file path
        # For demonstration:
        print(f"Importing UDMF map from: {self.filepath}")
        try:
            options = self.get_options()
            udmf_map = load_udmf_map(self.filepath)
            create_udmf_scene(udmf_map, options)
        except Exception as e:
            # TODO: clean the scene
            popup_error_message(e)
            raise e

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class IMPORT_OT_pwad(IMPORT_OT_udmf):
    bl_idname = "import_scene.pwad"
    bl_label = "Import PWAD"
    bl_options = {"REGISTER", "UNDO"}

    # Define the filepath property for the file browser
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Your import logic goes here, use self.filepath for the file path
        # For demonstration:
        print(f"Importing PWAD map from: {self.filepath}")
        try:
            options = self.get_options()
            udmf_map = load_map_from_pwad(self.filepath)
            create_udmf_scene(udmf_map, options)
        except Exception as e:
            popup_error_message(e)
            raise e

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


def menu_func_udmf_import(self, context):
    self.layout.operator(IMPORT_OT_udmf.bl_idname, text="UDMF Map (.udmf)")


def menu_func_pwad_import(self, context):
    self.layout.operator(IMPORT_OT_pwad.bl_idname, text="PWAD Map (.wad)")


def register():
    bpy.utils.register_class(IMPORT_OT_udmf)
    bpy.utils.register_class(IMPORT_OT_pwad)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_udmf_import)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_pwad_import)


def unregister():
    bpy.utils.unregister_class(IMPORT_OT_udmf)
    bpy.utils.unregister_class(IMPORT_OT_pwad)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_udmf_import)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_pwad_import)
