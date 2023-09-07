import bpy


def get_addon_package():
    """Warning: This function is not safe to use in all cases. It is only safe to use if the current package is one
    level down from the root package. Blender addon-preferences API requires the key to be the root package name"""
    current_package = __package__
    parent_package = ".".join(current_package.split(".")[:-1])
    return parent_package


def get_texture_path(texture_name):
    preferences = bpy.context.preferences.addons[get_addon_package()].preferences
    base_texture_folder_path = preferences.base_texture_folder_path
    return base_texture_folder_path + texture_name + ".png"


def set_simple_uv_on_mesh(mesh, face_index, texture_image):
    # Ensure there's a UV map
    if not mesh.uv_layers:
        mesh.uv_layers.new()

    uv_layer = mesh.uv_layers.active.data

    # Get face and its loops
    face = mesh.polygons[face_index]
    loops = face.loop_indices

    # Get the vertex coordinates of the face
    co1 = mesh.vertices[mesh.loops[loops[0]].vertex_index].co
    co2 = mesh.vertices[mesh.loops[loops[1]].vertex_index].co
    co3 = mesh.vertices[mesh.loops[loops[2]].vertex_index].co
    co4 = mesh.vertices[mesh.loops[loops[3]].vertex_index].co

    # Calculate the lengths of all sides
    len1 = (co2 - co1).length
    len2 = (co3 - co2).length
    len3 = (co4 - co3).length
    len4 = (co1 - co4).length

    # Arbitrarily assign width and height based on the two longest lengths
    # This may or may not be suitable for your specific mesh geometry.
    width = max(len1, len2, len3, len4) * 100
    height = min(len1, len2, len3, len4) * 100

    print("Wall dimensions: ", width, height)
    print("Texture dimensions: ", texture_image.size[0], texture_image.size[1])
    # Calculate tiling factors based on the texture size
    tile_x = width / texture_image.size[0]
    tile_y = height / texture_image.size[1]

    print("Tiling: ", (int(tile_x), int(tile_y)))
    uv_layer[loops[0]].uv = (0, 0)
    uv_layer[loops[1]].uv = (tile_x, 0)
    uv_layer[loops[2]].uv = (tile_x, tile_y)
    uv_layer[loops[3]].uv = (0, tile_y)
    return width, height


def create_checker_material(scale_value=50.0):  # Default scale set to 10
    checker_material = bpy.data.materials.new(name="CheckerFallback")
    checker_material.use_nodes = True
    nodes = checker_material.node_tree.nodes
    links = checker_material.node_tree.links

    bsdf = nodes["Principled BSDF"]
    checker_node = nodes.new(type="ShaderNodeTexChecker")

    # Adjust the scale of the checker pattern
    checker_node.inputs["Scale"].default_value = scale_value

    links.new(bsdf.inputs["Base Color"], checker_node.outputs["Color"])

    return checker_material


def assign_texture_to_face(face, texture_name, obj, face_index, mesh):
    try:
        # Try loading the image texture
        texture_image = bpy.data.images.load(get_texture_path(texture_name))
    except:
        # Use the fallback checker material
        material = create_checker_material()
    else:
        # If the texture loads successfully, create a material for it
        material_name = f"{texture_name}_face_{face_index}"

        material = bpy.data.materials.new(name=material_name)
        material.use_nodes = True
        nodes = material.node_tree.nodes

        for node in nodes:
            nodes.remove(node)

        bsdf = nodes.new(type='ShaderNodeBsdfDiffuse')
        bsdf.location = (0, 0)

        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        material_output.location = (400, 0)
        material.node_tree.links.new(material_output.inputs["Surface"], bsdf.outputs["BSDF"])

        if texture_image:  # assuming texture_image is loaded if it exists
            tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_image.image = texture_image
            tex_image.location = (-300, 0)
            material.node_tree.links.new(bsdf.inputs["Color"], tex_image.outputs["Color"])

        # Create a new image for baking based on the wall dimensions
        width, height = set_simple_uv_on_mesh(mesh, face_index, texture_image)
        baking_image_name = f"Bake_{face_index}"
        if baking_image_name not in bpy.data.images:
            baking_image = bpy.data.images.new(baking_image_name, width=int(width), height=int(height))
        else:
            baking_image = bpy.data.images[baking_image_name]

        # Add a new ImageTexture node for this image
        for node in material.node_tree.nodes:
            node.select = False

        # Select and activate the original texture node
        # tex_image.select = True
        # material.node_tree.nodes.active = tex_image
        # Redraw the Node Editor
        for area in bpy.context.screen.areas:
            if area.type == 'NODE_EDITOR':
                area.tag_redraw()

        bake_node = material.node_tree.nodes.new('ShaderNodeTexImage')
        bake_node.location = (-600, 0)
        bake_node.image = baking_image
        bake_node.select = True
        material.node_tree.nodes.active = bake_node

    # Assign the material to the Blender mesh object
    obj.data.materials.append(material)
    face.material_index = obj.data.materials.find(material.name)
