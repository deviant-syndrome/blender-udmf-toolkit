import bpy

from ..bake_auto import save_all_baked_images
from ..bake_auto import prepare_for_baking


class ObjectPrepareBakeOperator(bpy.types.Operator):
    bl_idname = "object.preparebake_operator"
    bl_label = "Prepare Bake"
    bl_description = "Do something when clicked"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Your code here. For example, just print a message:
        result = prepare_for_baking(context.active_object)
        if result:
            removed, added = result
            self.report({'INFO'}, "Bake preparation done. Removed " + str(removed) + " materials and added " + str(added) + " blank bake images.")
        else:
            self.report({'WARNING'}, "Bake preparation skipped. Not a UDMF object.")
        return {'FINISHED'}


class ObjectExportBakedTexturesOperator(bpy.types.Operator):
    bl_idname = "object.exportbakedtextures_operator"
    bl_label = "Export baked textures"
    bl_description = "Do something when clicked"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Your code here. For example, just print a message:
        print("Bake textures export started...")
        num_saved = save_all_baked_images(context.active_object)
        self.report({'INFO'}, "Bake textures export done. Saved " + str(num_saved) + " images.")
        return {'FINISHED'}


# Step 2: Define the Panel
class SimpleObjectPanel(bpy.types.Panel):
    bl_label = "Simple Panel"
    bl_idname = "OBJECT_PT_simple"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        # Add the button (operator) to the panel
        layout.operator("object.preparebake_operator")
        layout.operator("object.exportbakedtextures_operator")


# Registration
def register():
    bpy.utils.register_class(ObjectPrepareBakeOperator)
    bpy.utils.register_class(ObjectExportBakedTexturesOperator)
    bpy.utils.register_class(SimpleObjectPanel)


def unregister():
    bpy.utils.unregister_class(SimpleObjectPanel)
    bpy.utils.unregister_class(ObjectExportBakedTexturesOperator)
    bpy.utils.unregister_class(ObjectPrepareBakeOperator)


if __name__ == "__main__":
    register()
