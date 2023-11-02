from .texture_utils import get_simple_tiling_on_mesh


class MaterialNodeParameters:
    def __init__(self, texture_data, data_layers):
        self.texture_data = texture_data
        self.data_layers = data_layers

    def get_material_name(self, obj, face_index, face):
        return "Material"

    def get_face_tiling(self, obj, face, face_index, image):
        return 1, 1, 1, 1

    def set_custom_properties(self, material, obj, face):
        pass

    def preprocess_mesh_uv(self, obj, face_index):
        pass


class WallMaterialNodeParameters(MaterialNodeParameters):
    def __init__(self, texture_data, data_layers):
        super().__init__(texture_data, data_layers)
        self.tiling = None

    def get_material_name(self, obj, face_index, face):
        return "Wall_{}".format(face_index)

    def get_face_tiling(self, obj, face, face_index, image):
        self.tiling = get_simple_tiling_on_mesh(obj.data, face_index, image)
        return self.tiling

    def set_custom_properties(self, material, obj, face):
        material["width"] = self.tiling[2]
        material["height"] = self.tiling[3]
        material["sidedef_index"] = face[self.data_layers["sidedef_index"]]
        material["texture_type"] = face[self.data_layers["texture_type"]]

    def preprocess_mesh_uv(self, obj, face_index):
        pass
        # set_default_uv_on_mesh(obj.data, face_index)


class FloorMaterialNodeParameters(MaterialNodeParameters):
    def __init__(self, texture_data, data_layers):
        super().__init__(texture_data, data_layers)
        self.material_name = None
        self.tiling = None

    def get_material_name(self, obj, face_index, face):
        sector_index = face[self.data_layers["sector_index"]]
        self.material_name = "Floor_{}".format(sector_index)
        return self.material_name

    def get_face_tiling(self, obj, face, face_index, image):
        width = face[self.data_layers["width"]]
        height = face[self.data_layers["height"]]
        tile_x = width / image.size[0]
        tile_y = height / image.size[1]

        self.tiling = (tile_x, tile_y, width, height)
        return self.tiling

    def set_custom_properties(self, material, obj, face):
        material["width"] = self.tiling[2]
        material["height"] = self.tiling[3]
        material["sector_index"] = face[self.data_layers["sector_index"]]
        material["offset_x"] = face[self.data_layers["offset_x"]]
        material["offset_y"] = face[self.data_layers["offset_y"]]
        material["texture_type"] = "floor"

    def preprocess_mesh_uv(self, obj, face_index):
        pass
        # set_default_uv_on_mesh(obj.data, face_index)


class CeilingMaterialNodeParameters(FloorMaterialNodeParameters):
    def __init__(self, texture_data, data_layers):
        super().__init__(texture_data, data_layers)

    def get_material_name(self, obj, face_index, face):
        sector_index = face[self.data_layers["sector_index"]]
        self.material_name = "Ceiling_{}".format(sector_index)
        return self.material_name

    def set_custom_properties(self, material, obj, face):
        super().set_custom_properties(material, obj, face)
        material["texture_type"] = "ceiling"

    def preprocess_mesh_uv(self, obj, face_index):
        pass
        # set_default_uv_on_mesh(obj.data, face_index)


def create_material_node_tree(material, texture_image, tiling, texture_data):
    tile_x, tile_y, _, _ = tiling

    material.use_nodes = True
    nodes = material.node_tree.nodes

    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)

    # Add BSDF shader
    bsdf = nodes.new(type='ShaderNodeBsdfDiffuse')
    bsdf.location = (0, 0)

    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (800, 0)

    # UV Map node
    uv_map_node = nodes.new(type="ShaderNodeUVMap")
    uv_map_node.location = (-1200, 0)

    # Separate XYZ node
    separate_xyz = nodes.new(type="ShaderNodeSeparateXYZ")
    separate_xyz.location = (-1000, 0)

    # Multiply nodes (equivalent to dividing by texture dimensions)
    multiply_node_x = nodes.new(type="ShaderNodeMath")
    multiply_node_x.operation = 'MULTIPLY'
    multiply_node_x.location = (-800, -200)

    # Multiply nodes (equivalent to dividing by texture dimensions)
    multiply_node_y = nodes.new(type="ShaderNodeMath")
    multiply_node_y.operation = 'MULTIPLY'
    multiply_node_y.location = (-800, -200)

    # Combine XYZ node
    combine_xyz = nodes.new(type="ShaderNodeCombineXYZ")
    combine_xyz.location = (-600, 0)

    # Value nodes for texture dimensions
    value_node_x = nodes.new(type="ShaderNodeValue")
    value_node_x.outputs[0].default_value = tile_x
    value_node_x.label = "Tile X"
    value_node_x.location = (-1000, -200)

    value_node_y = nodes.new(type="ShaderNodeValue")
    value_node_y.outputs[0].default_value = tile_y
    value_node_y.label = "Tile Y"
    value_node_y.location = (-1000, -400)

    # Mapping node
    mapping_node = nodes.new(type="ShaderNodeMapping")
    mapping_node.location = (-400, 0)

    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.image = texture_image
    tex_image.name = "Tiled Texture"
    tex_image.location = (200, 0)

    # offsets
    offset_node_x = nodes.new(type="ShaderNodeValue")
    offset_node_x.outputs[0].default_value = texture_data["offset_x"]
    offset_node_x.label = "Offset X"
    offset_node_x.location = (-1000, -600)

    offset_node_y = nodes.new(type="ShaderNodeValue")
    offset_node_y.outputs[0].default_value = texture_data["offset_y"]
    offset_node_y.label = "Offset Y"
    offset_node_y.location = (-1000, -800)

    offset_combine_xyz = nodes.new(type="ShaderNodeCombineXYZ")
    offset_combine_xyz.location = (-600, -600)

    material.node_tree.links.new(offset_node_x.outputs[0], offset_combine_xyz.inputs[0])
    material.node_tree.links.new(offset_node_y.outputs[0], offset_combine_xyz.inputs[1])
    material.node_tree.links.new(offset_combine_xyz.outputs[0], mapping_node.inputs["Location"])

    material.node_tree.links.new(uv_map_node.outputs["UV"], separate_xyz.inputs["Vector"])

    material.node_tree.links.new(separate_xyz.outputs["X"], multiply_node_x.inputs[0])
    material.node_tree.links.new(value_node_x.outputs[0], multiply_node_x.inputs[1])

    material.node_tree.links.new(separate_xyz.outputs["Y"], multiply_node_y.inputs[0])
    material.node_tree.links.new(value_node_y.outputs[0], multiply_node_y.inputs[1])

    material.node_tree.links.new(multiply_node_x.outputs[0], combine_xyz.inputs[0])
    material.node_tree.links.new(multiply_node_y.outputs[0], combine_xyz.inputs[1])

    material.node_tree.links.new(mapping_node.inputs["Vector"], combine_xyz.outputs["Vector"])
    material.node_tree.links.new(mapping_node.outputs["Vector"], tex_image.inputs["Vector"])
    material.node_tree.links.new(tex_image.outputs["Color"], bsdf.inputs["Color"])
    material.node_tree.links.new(bsdf.outputs["BSDF"], material_output.inputs["Surface"])
