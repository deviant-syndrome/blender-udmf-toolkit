import bpy

from .material_nodes import create_material_node_tree, MaterialNodeParameters
from .texture_utils import create_checker_material, get_texture_path


def create_material_for_face_new(
    obj, face, face_index, wall_material_params: MaterialNodeParameters
):
    texture_name = wall_material_params.texture_data["texture_name"]
    try:
        # Try loading the image texture
        texture_image = bpy.data.images.load(get_texture_path(texture_name))
    except:  # noqa E722
        # Use the fallback checker material
        fallback_material = create_checker_material(
            wall_material_params.get_material_name(obj, face_index, face) + "_fallback"
        )
        obj.data.materials.append(fallback_material)
        return fallback_material
    else:
        material_name = wall_material_params.get_material_name(obj, face_index, face)
        material = bpy.data.materials.new(name=material_name)
        tiling = wall_material_params.get_face_tiling(
            obj, face, face_index, texture_image
        )
        wall_material_params.preprocess_mesh_uv(obj, face_index)
        create_material_node_tree(
            material, texture_image, tiling, wall_material_params.texture_data
        )
        wall_material_params.set_custom_properties(material, obj, face)
        obj.data.materials.append(material)
        return material
