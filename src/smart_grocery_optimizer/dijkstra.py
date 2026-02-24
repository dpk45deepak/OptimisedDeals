import heapq


def dijkstra(graph):
    pq = []
    distances = {}

    for node in graph:
        distances[node] = float("inf")

    for node, weight in graph.items():
        heapq.heappush(pq, (weight, node))

    while pq:
        dist, node = heapq.heappop(pq)
        distances[node] = dist

    return distances