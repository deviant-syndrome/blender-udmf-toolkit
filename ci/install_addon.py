import bpy

# The name of your addon
addon_name = "udmf_blender_addon"

# Now enable the addon
# Make sure the addon directory is correct and contains '__init__.py'
try:
    bpy.ops.preferences.addon_enable(module=addon_name)
    # Save the preferences
    bpy.ops.wm.save_userpref()
    print(f"Enabled addon: {addon_name}")
except Exception as e:
    print(f"Failed to enable addon: {addon_name}")
    raise e
