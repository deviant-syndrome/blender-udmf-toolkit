from .sector_polygon import create_sector_polygon


def draw_horizontals(bm, graph, udmf_map, height_func, texture_func):
    sector_metadata = {}
    for sector in graph:
        create_sector_polygon(sector, graph, udmf_map, bm, udmf_map.vertexes, sector_metadata, height_func,
                              texture_func)
    return sector_metadata


def draw_floors(bm, graph, udmf_map):
    return draw_horizontals(bm, graph, udmf_map, lambda s: s.heightfloor, lambda s: s.texturefloor)


def draw_ceilings(bm, graph, udmf_map):
    return draw_horizontals(bm, graph, udmf_map, lambda s: s.heightceiling, lambda s: s.textureceiling)
