import bpy


def get_addon_package():
    """Warning: This function is not safe to use in all cases. It is only safe to use if the current package is one
    level down from the root package. Blender addon-preferences API requires the key to be the root package name"""
    current_package = __package__
    parent_package = ".".join(current_package.split(".")[:-1])
    return parent_package


def get_baked_texture_path(texture_name):
    preferences = bpy.context.preferences.addons[get_addon_package()].preferences
    baked_texture_folder_path = preferences.baked_texture_folder_path

    return baked_texture_folder_path + texture_name + ".png"


def generate_texture_name(sidedef, texture_type):
    """Generate the texture filename based on sidedef and texture_type."""
    return f"M01{sidedef}{texture_type}"


def generate_floor_texture_name(sector):
    """Generate the texture filename based on sector."""
    return f"M01{sector}F"


def generate_ceiling_texture_name(sector):
    """Generate the texture filename based on sector."""
    return f"M01{sector}C"


def save_baked_image(image, name):
    """
    Saves the given image to the given path.
    """
    path = get_baked_texture_path(name)
    image.filepath_raw = path
    print("Saving image to " + path)
    image.file_format = "PNG"
    image.save()


def find_baked_image_node(material):
    for node in material.node_tree.nodes:
        if node.type == "TEX_IMAGE" and node.name.startswith("Bake"):
            return node
    return None


def save_baked_image_from_material(obj, material):
    node = find_baked_image_node(material)
    if node is None:
        return 0
    image = node.image
    if obj["udmf_type"] == "walls":
        texture_type = material["texture_type"].decode("utf-8")
        sidedef = material["sidedef_index"]
        save_baked_image(image, generate_texture_name(sidedef, texture_type))
        return 1
    elif obj["udmf_type"] == "floors":
        sector = material["sector_index"]
        save_baked_image(image, generate_floor_texture_name(sector))
        return 1
    elif obj["udmf_type"] == "ceilings":
        sector = material["sector_index"]
        save_baked_image(image, generate_ceiling_texture_name(sector))
        return 1
    else:
        return 0


def save_all_baked_images(obj):
    num_saved = 0
    for material in obj.data.materials:
        num_saved += save_baked_image_from_material(obj, material)
    return num_saved
