def get_texture_metadata(sidedef, walltype):
    """Get texture metadata for a given sidedef and walltype."""

    walltype_to_attr_suffix = {"UPPER": "top", "MIDDLE": "middle", "LOWER": "bottom"}

    walltype_to_attr_abbrev = {"UPPER": "top", "MIDDLE": "mid", "LOWER": "bottom"}

    suffix = walltype_to_attr_suffix.get(walltype)
    abbrev_suffix = walltype_to_attr_abbrev.get(walltype)
    abbr_suffix = suffix[:3]
    if not suffix:
        raise ValueError(f"Invalid walltype: {walltype}")

    # Using getattr to fetch attributes dynamically based on the walltype
    texture = getattr(sidedef, f"texture{suffix}")
    scalex = getattr(sidedef, f"scalex_{suffix}", 1.0) or 1.0
    scaley = getattr(sidedef, f"scaley_{suffix}", 1.0) or 1.0
    offsetx = (
        getattr(sidedef, f"offsetx_{abbr_suffix}", getattr(sidedef, "offsetx", 0.0))
        or 0.0
    )
    offsety = (
        getattr(sidedef, f"offsety_{abbrev_suffix}", getattr(sidedef, "offsety", 0.0))
        or 0.0
    )

    return {
        "texture_name": texture,
        "scale_x": scalex,
        "scale_y": scaley,
        "offset_x": offsetx / 100.0,
        "offset_y": offsety / 100.0,
    }


def add_wall(
    v1, v2, start_height, end_height, bm, face_metadata, sidedef=None, walltype="MIDDLE"
):
    """Add a wall using the bottom vertices and the heights."""
    # Get bottom vertices
    bottom_1 = bm.verts.new((v1[0], v1[1], start_height))
    bottom_2 = bm.verts.new((v2[0], v2[1], start_height))

    # Calculate top vertices based on height
    top_1 = bm.verts.new((v1[0], v1[1], end_height))
    top_2 = bm.verts.new((v2[0], v2[1], end_height))

    # Create the wall face
    bm.faces.new([bottom_1, bottom_2, top_2, top_1])

    # Assign texture and sidedef index
    face_index = len(bm.faces) - 1

    texture_type_abbreviations = {"UPPER": "U", "MIDDLE": "M", "LOWER": "L"}

    if sidedef:
        face_metadata[face_index] = {
            "texture_data": get_texture_metadata(sidedef, walltype),
            "sidedef_index": sidedef.index,
            "wall_type": texture_type_abbreviations[walltype],
        }
    else:
        face_metadata[face_index] = {
            "texture_data": None,
            "sidedef_index": -1,
            "wall_type": texture_type_abbreviations[walltype],
        }
