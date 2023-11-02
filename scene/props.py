import bpy


def init_props():
    bpy.types.Scene.map_scale = bpy.props.FloatProperty(name="Map scale", default=0.01)
    bpy.types.Scene.original_pwad = bpy.props.StringProperty(name="Original PWAD", default="")


def clear_props():
    del bpy.types.Scene.map_scale
    del bpy.types.Scene.original_pwad


def set_props_on_import(options):
    bpy.context.scene.map_scale = options.get("scale", 0.01)
    bpy.context.scene.original_pwad = options.get("original_pwad", "")
