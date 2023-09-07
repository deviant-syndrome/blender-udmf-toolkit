from .visual_sector import VisualSector
from .wall import add_wall


def draw_walls(graph, map, bm):
    face_metadata = {}
    vertices = map.vertexes
    for sector_id, linedefs in graph.items():
        current_sector = VisualSector(map.sectors[sector_id])

        for linedef_data in linedefs:
            v1_coords = (vertices[linedef_data['linedef'][0]].x, vertices[linedef_data['linedef'][0]].y)
            v2_coords = (vertices[linedef_data['linedef'][1]].x, vertices[linedef_data['linedef'][1]].y)

            if not linedef_data['twosided']:
                add_wall(v1_coords, v2_coords, current_sector.heightfloor, current_sector.heightceiling, bm,
                         face_metadata, linedef_data['front_sidedef'], walltype="MIDDLE")
            else:
                # For two-sided walls
                other_sector = VisualSector(map.sectors[linedef_data['back_sector']])

                # Check upper mismatch
                if current_sector.heightceiling != other_sector.heightceiling:
                    upper_start = min(current_sector.heightceiling, other_sector.heightceiling)
                    upper_end = max(current_sector.heightceiling, other_sector.heightceiling)
                    add_wall(v1_coords, v2_coords, upper_start, upper_end, bm, face_metadata,
                             linedef_data['front_sidedef'], walltype="UPPER")

                # Check lower mismatch
                if current_sector.heightfloor != other_sector.heightfloor:
                    lower_start = min(current_sector.heightfloor, other_sector.heightfloor)
                    lower_end = max(current_sector.heightfloor, other_sector.heightfloor)
                    add_wall(v1_coords, v2_coords, lower_start, lower_end, bm, face_metadata,
                             linedef_data['front_sidedef'], walltype="LOWER")
    return face_metadata
