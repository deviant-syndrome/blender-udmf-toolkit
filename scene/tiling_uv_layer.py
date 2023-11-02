import bmesh
import bpy


def uv_map_sector_by_bounding_box(obj, sector_faces_dict):
    map_scale_reciprocal = 1 / bpy.context.scene.map_scale
    # Ensure object is in object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a BMesh instance from the object mesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Ensure lookup table is up-to-date
    bm.faces.ensure_lookup_table()
    width_layer = bm.faces.layers.int.get("bbox_width") or bm.faces.layers.int.new("bbox_width")
    height_layer = bm.faces.layers.int.get("bbox_height") or bm.faces.layers.int.new("bbox_height")

    offset_x_layer = bm.faces.layers.int.get("offset_x") or bm.faces.layers.int.new("offset_x")
    offset_y_layer = bm.faces.layers.int.get("offset_y") or bm.faces.layers.int.new("offset_y")

    # Get the sector_index custom layer
    sector_index_layer = bm.faces.layers.int.get("sector_index")
    if not sector_index_layer:
        raise ValueError("sector_index attribute not found!")

    # Create or get the UV layer
    uv_layer = bm.loops.layers.uv.verify()

    for sector_idx, face_indexes in sector_faces_dict.items():
        faces = [bm.faces[idx] for idx in face_indexes]

        # Calculate 2D bounding box
        min_x = min([v.co.x for f in faces for v in f.verts])
        max_x = max([v.co.x for f in faces for v in f.verts])
        min_y = min([v.co.y for f in faces for v in f.verts])
        max_y = max([v.co.y for f in faces for v in f.verts])

        # Identify the vertices that lie on the top and bottom edges of the bounding box
        top_vertices_x = [v.co.x for f in faces for v in f.verts if v.co.y == max_y]
        bottom_vertices_x = [v.co.x for f in faces for v in f.verts if v.co.y == min_y]

        # Calculate the widths using the leftmost and rightmost vertices on the top and bottom edges
        top_edge_width = (max(top_vertices_x) - min(top_vertices_x)) * map_scale_reciprocal
        bottom_edge_width = (max(bottom_vertices_x) - min(bottom_vertices_x)) * map_scale_reciprocal

        # Set bbox_width to the longer of the top and bottom edge widths
        bbox_width = max(top_edge_width, bottom_edge_width)
        # Calculate the height as the difference between the y-coordinates of the bounding box
        bbox_height = (max_y - min_y) * map_scale_reciprocal

        # Scale and offset factors for UV mapping
        scale_x = 1.0 / (max_x - min_x)
        scale_y = 1.0 / (max_y - min_y)
        offset_x = -min_x
        offset_y = -min_y

        # Assign UVs based on bounding box
        for face in faces:
            face[width_layer] = int(bbox_width)  # Access face by index inside loop
            face[height_layer] = int(bbox_height)  # Access face by index inside loop
            # todo: align to the nearest multiple of 64
            face[offset_x_layer] = int(min_x * map_scale_reciprocal)  # Access face by index inside loop
            face[offset_y_layer] = int(min_y * map_scale_reciprocal)  # Access face by index inside loop

            for loop in face.loops:
                u = (loop.vert.co.x + offset_x) * scale_x
                v = (loop.vert.co.y + offset_y) * scale_y
                loop[uv_layer].uv = (u, v)

    # Update the mesh from bmesh
    bm.to_mesh(obj.data)
    bm.free()
