import bpy


def make_faces_transparent_except(obj, face_index):
    """
    Makes all the faces of the object transparent except the given face_index.
    Returns a dictionary of the original materials per face.
    """
    original_materials = {}

    # Create a transparent material if not exists
    if 'Transparent_Material' not in bpy.data.materials:
        transparent_mat = bpy.data.materials.new(name="Transparent_Material")
        transparent_mat.use_nodes = True
        nodes = transparent_mat.node_tree.nodes
        for node in nodes:
            nodes.remove(node)

        transparent_bsdf = nodes.new(type="ShaderNodeBsdfTransparent")
        material_output = nodes.new(type="ShaderNodeOutputMaterial")

        transparent_mat.node_tree.links.new(
            transparent_bsdf.outputs["BSDF"],
            material_output.inputs["Surface"]
        )

        # Set Blend Mode to Alpha Blend
        transparent_mat.blend_method = 'BLEND'

    else:
        transparent_mat = bpy.data.materials["Transparent_Material"]

    # Assign transparent material to all faces except face_index
    for poly in obj.data.polygons:
        original_materials[poly.index] = poly.material_index
        if poly.index != face_index:
            if transparent_mat.name not in obj.material_slots:
                obj.data.materials.append(transparent_mat)
            poly.material_index = obj.data.materials.find(transparent_mat.name)

    return original_materials


def restore_original_materials(obj, original_materials):
    """
    Restores the materials of an object to their original states
    using a dictionary of original materials.
    """
    for face_index, mat_index in original_materials.items():
        obj.data.polygons[face_index].material_index = mat_index
    # Remove the transparent material slot if it's no longer used
    for slot in obj.material_slots:
        if slot.material == bpy.data.materials["Transparent_Material"]:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.material_slot_remove()
            break
