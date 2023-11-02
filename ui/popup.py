import bpy


class WM_OT_centered_popup(bpy.types.Operator):
    bl_idname = "wm.centered_popup"
    bl_label = "UDMF Toolkit"
    bl_options = {"REGISTER", "INTERNAL"}

    message: bpy.props.StringProperty(
        name="message",
        description="Text to display in the popup",
        default="",
    )

    def execute(self, context):
        # Your operator logic here...
        return {"FINISHED"}

    def invoke(self, context, event):
        # Save current mouse position
        original_mouse_position = (event.mouse_region_x, event.mouse_region_y)

        # Get the area and region sizes
        area_width = context.area.width
        # Cannot figure out how to get the height of the screen, for popup to be centered
        area_height = 1200  # context.area.height

        # Move the mouse cursor to the center
        context.window.cursor_warp(int(area_width / 2), area_height)

        # Show the dialog
        result = context.window_manager.invoke_props_dialog(self, width=400)

        # Restore the mouse position
        context.window.cursor_warp(*original_mouse_position)

        return result

    def draw(self, csontext):
        layout = self.layout
        lines = self.message.splitlines()
        for line in lines:
            row = layout.row()
            row.label(text=line)


def register():
    bpy.utils.register_class(WM_OT_centered_popup)


def unregister():
    bpy.utils.unregister_class(WM_OT_centered_popup)


if __name__ == "__main__":
    register()
