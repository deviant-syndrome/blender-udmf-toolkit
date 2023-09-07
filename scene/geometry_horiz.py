from .sector_polygon import create_sector_polygon


def draw_floors(bm, graph, udmf_map):
    for sector in graph:
        create_sector_polygon(sector, graph, udmf_map, bm, udmf_map.vertexes)
