from .distance import haversine


def build_graph(family, shops):
    graph = {}

    for shop in shops:
        distance = haversine(family.lat, family.lon, shop.lat, shop.lon)
        graph[shop.id] = distance

    return graph