from ..utils.helpers import export_map_to_pwad
from ..bake_auto.update_map import create_updated_map
import bpy


def popup_error_message(error_message):
    bpy.ops.wm.centered_popup('INVOKE_DEFAULT', message="Error exporting file:\n {}".format(error_message))


class EXPORT_OT_udmf(bpy.types.Operator):
    bl_idname = "export_scene.pwad"
    bl_label = "Export PWAD"
    bl_options = {'REGISTER', 'UNDO'}

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

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_udmf.bl_idname, text="Export PWAD")


def register():
    bpy.utils.register_class(EXPORT_OT_udmf)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(EXPORT_OT_udmf)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
