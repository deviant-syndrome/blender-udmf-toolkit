import bpy
from mathutils import Vector


# noinspection DuplicatedCode
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


def get_simple_tiling_on_mesh(mesh, face_index, texture_image):
    # Get face and its loops
    face = mesh.polygons[face_index]
    loops = face.loop_indices

    # Extract vertex coordinates of the face
    coordinates = [mesh.vertices[mesh.loops[i].vertex_index].co for i in loops]

    # Sort vertices based on Z to determine top and bottom
    sorted_coordinates = sorted(coordinates, key=lambda co: co.z, reverse=True)

    # top_left, top_right, bottom_left, bottom_right = sorted_coordinates

    topmost1 = sorted_coordinates[0]
    topmost2 = sorted_coordinates[1]
    width = (topmost1 - topmost2).length * 100

    highest_z = max(coord.z for coord in coordinates)
    lowest_z = min(coord.z for coord in coordinates)

    height = (highest_z - lowest_z) * 100

    print("Face #", face_index, "width: ", round(width, 2), "height: ", round(height, 2))
    print("Texture dimensions: ", texture_image.size[0], texture_image.size[1])

    # Calculate tiling factors based on the texture size
    tile_x = width / texture_image.size[0]
    tile_y = height / texture_image.size[1]

    # print("Tiling: ", round(tile_x, 2), round(tile_y, 2))

    return tile_x, tile_y, width, height


def set_default_uv_on_mesh(mesh, face_index):
    # Ensure there's a UV map
    if not mesh.uv_layers:
        mesh.uv_layers.new()

    uv_layer = mesh.uv_layers.active.data

    # Get face and its loops
    face = mesh.polygons[face_index]
    loops = face.loop_indices

    # Assign UVs
    uv_layer[loops[0]].uv = (0, 0)
    uv_layer[loops[1]].uv = (1, 0)
    uv_layer[loops[2]].uv = (1, 1)
    uv_layer[loops[3]].uv = (0, 1)


def create_checker_material(name, scale_value=50.0):  # Default scale set to 10
    checker_material = bpy.data.materials.new(name=name)
    checker_material.use_nodes = True
    nodes = checker_material.node_tree.nodes
    links = checker_material.node_tree.links

    bsdf = nodes["Principled BSDF"]
    checker_node = nodes.new(type="ShaderNodeTexChecker")

    # Adjust the scale of the checker pattern
    checker_node.inputs["Scale"].default_value = scale_value

    links.new(bsdf.inputs["Base Color"], checker_node.outputs["Color"])

    return checker_material
