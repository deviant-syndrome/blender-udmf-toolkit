import bmesh


def assign_custom_attributes(obj, face_index, attributes):
    """
    Assign custom attributes to a face in an object's mesh.
    :param obj: Target object
    :param face_index: Index of the face to assign attributes to
    :param attributes: Dictionary of attribute names and their values
    """

    # Create a BMesh instance from the object mesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Ensure lookup table is up-to-date
    bm.faces.ensure_lookup_table()

    for attr_name, attr_value in attributes.items():
        # Determine the type of the attribute and assign it to the appropriate layer
        if isinstance(attr_value, int) or isinstance(attr_value, float):
            attr_layer = bm.faces.layers.int.get(attr_name) or bm.faces.layers.int.new(attr_name)
            bm.faces[face_index][attr_layer] = int(attr_value)  # Access face by index inside loop
        elif isinstance(attr_value, str):
            attr_layer = bm.faces.layers.string.get(attr_name) or bm.faces.layers.string.new(attr_name)
            bm.faces[face_index][attr_layer] = attr_value.encode()

    # Update the mesh
    bm.to_mesh(obj.data)
    bm.free()


def get_custom_attributes(obj, face_index, attr_names):
    """
    Retrieve the custom attributes from the specified face.
    :param obj: Source object
    :param face_index: Index of the face to retrieve attributes from
    :param attr_names: List of attribute names to retrieve
    :return: Dictionary of attribute names and their values
    """

    # Create a BMesh instance from the object mesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Ensure lookup table is up-to-date
    bm.faces.ensure_lookup_table()

    face = bm.faces[face_index]

    attributes = {}

    for attr_name in attr_names:
        # Check if the attribute layer exists and fetch the value
        attr_layer_int = bm.faces.layers.int.get(attr_name)
        attr_layer_string = bm.faces.layers.string.get(attr_name)

        if attr_layer_int is not None:
            attributes[attr_name] = face[attr_layer_int]
        elif attr_layer_string is not None:
            attributes[attr_name] = face[attr_layer_string].decode()

    # Clean up
    bm.free()

    return attributes
