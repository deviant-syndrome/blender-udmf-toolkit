from mathutils.geometry import delaunay_2d_cdt
from mathutils import Vector

from .visual_sector import VisualSector


def create_sector_polygon(sector, graph, map, bm, vertices):
    vertex_coords = []
    visual_sector = VisualSector(map.sectors[sector])
    # Iterate over each linedef associated with this sector
    for linedef_data in graph[sector]:
        v1, v2 = linedef_data['linedef']

        # Add the vertices of this linedef to the vertex_coords list
        vertex_coords.append((vertices[v1].x, vertices[v1].y, 0))
        vertex_coords.append((vertices[v2].x, vertices[v2].y, 0))

    # Note: At this point, vertex_coords will have duplicates as each linedef
    # might share a vertex with another linedef. If you wish to remove duplicates:
    vertex_coords = list(dict.fromkeys(vertex_coords))

    # Convert your vertex_coords to 2D mathutils.Vector
    vector_coords_2d = [Vector((v[0], v[1])) for v in vertex_coords]

    # Perform Delaunay triangulation
    output = delaunay_2d_cdt(vector_coords_2d, [], [], 0, 0.0001)

    new_vertex_coords_2d, out_edges, out_faces, orig_verts, orig_edges, orig_faces = output

    # Convert the 2D coords back to 3D for use in Blender
    new_vertex_coords_3d = [(v.x, v.y, visual_sector.heightfloor) for v in new_vertex_coords_2d]
    print("total new verts: ", len(new_vertex_coords_3d))
    print(out_faces)
    vert_map = [bm.verts.new(v) for v in new_vertex_coords_3d]

    # Add the new faces to the BMesh
    for face_indices in out_faces:
        bm.faces.new([vert_map[i] for i in face_indices])
