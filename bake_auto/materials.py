import bpy


def remove_unused_materials(obj):
    # Check if the object has material slots
    if not obj.material_slots:
        return

    # Get a set of material indices used by the object's faces
    used_material_indices = set(face.material_index for face in obj.data.polygons)
    num_removed = 0
    # Iterate through material slots in reverse (so we don't mess up the indices when removing)
    for i in reversed(range(len(obj.material_slots))):
        if i not in used_material_indices:
            num_removed += 1
            obj.active_material_index = i
            bpy.ops.object.material_slot_remove()
    return num_removed


def assign_bake_textures_to_obj(obj):
    num_assigned = 0
    for material in obj.data.materials:
        if material.name.endswith("_fallback"):
            continue
        if assign_bake_texture_to_material(material):
            num_assigned += 1
    return num_assigned


def assign_bake_texture_to_material(material):
    nodes = material.node_tree.nodes
    width = material["width"]
    height = material["height"]

    for node in nodes:
        if node.name == "Tiled Texture":
            baking_node = nodes.new(type="ShaderNodeTexImage")
            baking_node.name = "Bake_Node"
            baking_image_name = "Bake_{}".format(material.name)
            baking_node.location = (1200, 400)
            if baking_image_name not in bpy.data.images:
                baking_image = bpy.data.images.new(
                    baking_image_name, width=int(width), height=int(height)
                )
            else:
                baking_image = bpy.data.images[baking_image_name]
            baking_node.image = baking_image
            for nodek in material.node_tree.nodes:
                nodek.select = False

            # Select and activate the baking texture node
            # Redraw the Node Editor
            for area in bpy.context.screen.areas:
                if area.type == "NODE_EDITOR":
                    area.tag_redraw()

            baking_node.select = True
            material.node_tree.nodes.active = baking_node
            return 1
    return 0


def prepare_for_baking(obj):
    if not obj.name.startswith("UDMF_"):
        return None
    num_removed = remove_unused_materials(obj)
    num_assigned = assign_bake_textures_to_obj(obj)
    return num_removed, num_assigned
