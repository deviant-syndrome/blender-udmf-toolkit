from .material_nodes import FloorMaterialNodeParameters, CeilingMaterialNodeParameters
from .materials_walls import create_material_for_face_new


def create_material_for_flat(faces, texture_name, obj, layers, params_func):
    first_face = faces[0]
    texture_data = {
        "texture_name": texture_name,
        "texture_type": "floor",
        "offset_x": 0,
        "offset_y": 0,
    }
    params = params_func(texture_data, layers)
    material = create_material_for_face_new(obj, first_face, 0, params)
    for face in faces:
        face.material_index = obj.data.materials.find(material.name)


def create_material_for_sector_floor(faces, texture_name, obj, layers):
    create_material_for_flat(
        faces, texture_name, obj, layers, FloorMaterialNodeParameters
    )


def create_material_for_sector_ceiling(faces, texture_name, obj, layers):
    create_material_for_flat(
        faces, texture_name, obj, layers, CeilingMaterialNodeParameters
    )
