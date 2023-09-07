def add_wall(v1, v2, start_height, end_height, bm, face_metadata, sidedef=None, walltype="MIDDLE"):
    """Add a wall using the bottom vertices and the heights."""
    # Get bottom vertices
    bottom_1 = bm.verts.new((v1[0], v1[1], start_height))
    bottom_2 = bm.verts.new((v2[0], v2[1], start_height))

    # Calculate top vertices based on height
    top_1 = bm.verts.new((v1[0], v1[1], end_height))
    top_2 = bm.verts.new((v2[0], v2[1], end_height))

    # Create the wall face
    face = bm.faces.new([bottom_1, bottom_2, top_2, top_1])

    # Assign texture and sidedef index
    face_index = len(bm.faces) - 1

    if sidedef:
        if walltype == "MIDDLE" and hasattr(sidedef, 'texturemiddle'):
            texture_name = sidedef.texturemiddle
        elif walltype == "LOWER" and hasattr(sidedef, 'texturebottom'):
            texture_name = sidedef.texturebottom
        elif walltype == "UPPER" and hasattr(sidedef, 'texturetop'):
            texture_name = sidedef.texturetop
        else:
            texture_name = "heck666"  # default

        face_metadata[face_index] = {
            "texture_name": texture_name,
            "sidedef_index": sidedef.index,
            "wall_type": walltype
        }
    else:
        face_metadata[face_index] = {
            "texture_name": "heck666",
            "sidedef_index": -1,
            "wall_type": walltype
        }