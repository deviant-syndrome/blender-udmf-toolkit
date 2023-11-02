import bpy
import bmesh


def position_camera_for_wall(obj_name, face_index):
    # Get the object by name
    obj = bpy.data.objects[obj_name]

    # Ensure it's in object mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Get the face using BMesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    face = bm.faces[face_index]

    # Compute the face's center
    face_center = face.calc_center_median()

    # Create or get a camera
    if "WallBakeCam" not in bpy.data.objects:
        bpy.ops.object.camera_add(location=(0, 0, 0))
        cam = bpy.context.active_object
        cam.name = "WallBakeCam"
        cam.data.type = "ORTHO"
    else:
        cam = bpy.data.objects["WallBakeCam"]

    # Compute the direction from the face's normal
    direction = -face.normal

    # Calculate a good distance to place the camera. This is a rough estimate and can be tweaked.
    distance = max((v.co - face_center).length for v in face.verts) * 2

    # Position the camera
    cam.location = face_center - direction * distance

    # Point the camera to the face
    look_at = face_center
    loc_camera = cam.location

    direction = look_at - loc_camera
    rot_quat = direction.to_track_quat("-Z", "Y")
    cam.rotation_euler = rot_quat.to_euler()

    # Update the camera's orthographic scale
    # Assuming your face is more or less flat on the Z-axis,
    # this takes the X and Y dimensions to set the orthographic scale
    size_x = max((v.co.x - face_center.x) for v in face.verts)
    size_y = max((v.co.y - face_center.y) for v in face.verts)
    cam.data.ortho_scale = max(size_x, size_y) * 2

    # Clean up
    bm.free()
