from ..utils.helpers import export_map_to_pwad
from ..bake_auto.update_map import create_updated_map
import bpy
import os


def popup_error_message(error_message):
    bpy.ops.wm.centered_popup(
        "INVOKE_DEFAULT", message="Error exporting file:\n {}".format(error_message)
    )


def compute_label(cls, context):
    name = os.path.basename(context.scene.original_pwad)
    return f"Overwrite {name}"


class OVERWRITE_OT_udmf(bpy.types.Operator):
    bl_idname = "overwrite_scene.pwad"
    bl_label = "placeholder"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            obj = context.active_object
            map = create_updated_map(obj)
            filename = bpy.context.scene.original_pwad
            export_map_to_pwad(filename, map)
        except Exception as e:
            popup_error_message(e)
            raise e

        return {"FINISHED"}

    def invoke(self, context, event):
        pass


class EXPORT_OT_udmf(bpy.types.Operator):
    bl_idname = "export_scene.pwad"
    bl_label = "Export PWAD as..."
    bl_options = {"REGISTER", "UNDO"}

    # Define the filepath property for the file browser
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        print(f"Exporting bake-updated UDMF map to: {self.filepath}")
        try:
            obj = context.active_object
            map = create_updated_map(obj)
            export_map_to_pwad(self.filepath, map)
        except Exception as e:
            popup_error_message(e)
            raise e

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


def menu_func_export_to(self, context):
    self.layout.operator(EXPORT_OT_udmf.bl_idname, text=EXPORT_OT_udmf.bl_label)


def menu_func_overwrite(self, context):
    if bpy.context.scene.original_pwad:
        self.layout.operator(
            OVERWRITE_OT_udmf.bl_idname,
            text=compute_label(OVERWRITE_OT_udmf, bpy.context),
        )


def register():
    bpy.utils.register_class(EXPORT_OT_udmf)
    bpy.utils.register_class(OVERWRITE_OT_udmf)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_to)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_overwrite)


def unregister():
    bpy.utils.unregister_class(EXPORT_OT_udmf)
    bpy.utils.unregister_class(OVERWRITE_OT_udmf)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_to)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_overwrite)
