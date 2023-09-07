import bpy
import bmesh


def assign_custom_attribute(obj, face_index, sidedef, texture_type):
    # Ensure object is in object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a BMesh instance from the object mesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Ensure lookup table is up-to-date
    bm.faces.ensure_lookup_table()

    # Create custom layers
    sidedef_layer = bm.faces.layers.int.get("sidedef") or bm.faces.layers.int.new("sidedef")
    texture_layer = bm.faces.layers.string.get("texture_type") or bm.faces.layers.string.new("texture_type")

    # Assign values to custom layers for the specified face
    face = bm.faces[face_index]
    face[sidedef_layer] = sidedef
    face[texture_layer] = texture_type.encode()  # Store string as bytes

    # Update the mesh
    bm.to_mesh(obj.data)
    bm.free()


def get_face_custom_attribute(obj, face_index):
    """Retrieve the custom attributes sidedef and texture_type from the specified face."""

    # Create a BMesh instance from the object mesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Ensure lookup table is up-to-date
    bm.faces.ensure_lookup_table()

    # Get custom layers
    sidedef_layer = bm.faces.layers.int.get("sidedef")
    texture_layer = bm.faces.layers.string.get("texture_type")

    if sidedef_layer is None or texture_layer is None:
        raise ValueError("Custom layers not found on the mesh!")

    # Fetch values from custom layers for the specified face
    face = bm.faces[face_index]
    sidedef = face[sidedef_layer]
    texture_type = face[texture_layer].decode()  # Convert bytes back to string

    # Clean up
    bm.free()

    return sidedef, texture_type
