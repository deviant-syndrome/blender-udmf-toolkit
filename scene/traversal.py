from .extended_linedef import ExtendedSidedef


def create_graph(udmf_map):
    graph = {sector_id: [] for sector_id, _ in enumerate(udmf_map.sectors)}

    # Iterate over linedefs to populate the graph
    for linedef in udmf_map.linedefs:
        front_sidedef = ExtendedSidedef(
            udmf_map.sidedefs[linedef.sidefront], linedef.sidefront
        )
        front_sector = front_sidedef.sector

        back_sidedef = None
        back_sector = None

        if linedef.twosided:
            back_sidedef = ExtendedSidedef(
                udmf_map.sidedefs[linedef.sideback], linedef.sideback
            )
            back_sector = back_sidedef.sector

        entry = {
            "linedef": (linedef.v1, linedef.v2),
            "front_sidedef": front_sidedef,
            "front_sector": front_sector,
            "back_sidedef": back_sidedef,
            "back_sector": back_sector,
            "twosided": bool(back_sidedef),
        }

        graph[front_sector].append(entry)

        if back_sector is not None:
            graph[back_sector].append(entry)

    return graph
