# -*- coding: utf-8 -*-

"""
HomeWork Task 3
"""

import heapq
from typing import Any, Iterable

import networkx as nx
import matplotlib.pyplot as plt


def iter_neighbors(
        graph: nx.Graph | nx.DiGraph | nx.MultiGraph | nx.MultiDiGraph,
        node: Any
) -> Iterable[tuple[Any, float]]:
    """
    Iterator of (node, weight) for edges outgoing from the specified node
    For Multi* graphs, choose the minimum weight among parallel edges.
    """
    multigraph = graph.is_multigraph()
    for neighbor_node, edge_info in graph[node].items():
        if multigraph:
            # Select the minimal weight among the parallel edges node–neighbor_node
            weight = min(d.get("weight", 1.0) for d in edge_info.values())
        else:
            weight = edge_info.get("weight", 1.0)
        yield neighbor_node, float(weight)


def dijkstra(graph: nx.Graph | nx.DiGraph | nx.MultiGraph | nx.MultiDiGraph, start_node: Any) -> dict[Any, float]:
    """
    Heap-based Dijkstra’s algorithm for networkx graphs (edge attribute "weight").
    Implemented without decrease-key: uses "lazy" deletion of outdated records.

    :param graph: Graph, weights must be non-negative (nx.Graph, mandatory)
    :param start_node: Start vertex (Any value, mandatory)
    :return: Shortest paths to the other vertices (Dictionary of distances)
    """

    # Initialization
    distances = {nodes: float("inf") for nodes in graph.nodes}
    distances[start_node] = 0.0

    # Heap initialization
    heap: list[tuple[float, Any]] = [(0.0, start_node)]
    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if current_distance != distances[current_node]:
            # Outdated record
            continue

        for neighbor_node, weight in iter_neighbors(graph, current_node):
            if weight < 0:
                raise ValueError("A negative edge weight was found — Dijkstra’s algorithm is not valid")
            distance = current_distance + weight
            if distance < distances[neighbor_node]:
                distances[neighbor_node] = distance
                heapq.heappush(heap, (distance, neighbor_node))

    # Remove a start vertex from the shortest paths
    distances.pop(start_node, None)

    # Return the shortest paths to the vertices
    return distances


def test_dijkstra_heap() -> None:

    # Graph creation
    graph = nx.Graph()

    # Adding weighted edges (a cities and roads for example)
    graph.add_edge("A", "B", weight=5)
    graph.add_edge("A", "C", weight=10)
    graph.add_edge("B", "D", weight=3)
    graph.add_edge("C", "D", weight=2)
    graph.add_edge("D", "E", weight=4)

    # Graph visualization
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=15, width=2)
    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

    # Graph information
    print(f"Graph: {graph}")
    print(f"Graph nodes: {graph.nodes()}")
    print(f"Graph edges: {graph.edges()}")
    print()

    # Using Dijkstra’s algorithm
    print(f"Dijkstra shortest path: {dijkstra(graph, "A")}")
