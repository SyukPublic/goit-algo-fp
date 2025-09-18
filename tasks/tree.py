# -*- coding: utf-8 -*-

"""
Knuth-Morris-Pratt algorithm implementation
"""

import heapq
import uuid
from typing import Optional, Any, Union

import networkx as nx
import matplotlib.pyplot as plt


class Node:

    def __init__(self, value: Any, color: str = "#1C548C"):
        self.left = None
        self.right = None
        self.value = value
        self.color = color
        self.key = uuid.uuid4()

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


def edges_add(
        graph: Union[nx.Graph, nx.DiGraph],
        node: Node,
        pos: dict[uuid.UUID, tuple[int, int]],
        x: int = 0,
        y: int = 0,
        layer: int = 1,
) -> Union[nx.Graph, nx.DiGraph]:
    """
    Recursively builds a tree by adding an edge to the graph.

    :param graph: A graph representing a tree (nx.Graph | nx.DiGraph, mandatory)
    :param node: Tree node, graph vertex (Node, mandatory)
    :param pos: A dictionary with nodes as keys and positions as values (Dictionary of tuple)
    :param x: X-axis coordinate (Integer, optional)
    :param y: Y-axis coordinate (Integer, optional)
    :param layer: Hierarchy level (Integer, optional)
    :return: A graph representing a tree (nx.Graph | nx.DiGraph)
    """
    if node is not None:
        graph.add_node(node.key, color=node.color, label=node.value)
        if node.left:
            graph.add_edge(node.key, node.left.key)
            l = x -1 / 2 ** layer
            pos[node.left.key] = (l, y - 1)
            l = edges_add(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.key, node.right.key)
            r = x + 1 / 2 ** layer
            pos[node.right.key] = (r, y - 1)
            r = edges_add(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def tree_draw(root: Node, title: Optional[str] = None, last: bool = True) -> None:
    """
    Tree visualization.

    :param root: Root node of the tree (Node, mandatory)
    :param title: Figure/chart title (String, optional)
    :param last: Flag of whether it is the last figure/chart in the set or not (Boolean, optional)
    """
    tree = nx.DiGraph()
    pos = {root.key: (0, 0)}
    tree = edges_add(tree, root, pos)

    colors = [color for node_id, color in nx.get_node_attributes(tree, "color").items()]
    labels = nx.get_node_attributes(tree, "label")

    plt.figure(figsize=(15, 8))
    ax = plt.gca()
    nx.draw(
        tree,
        ax=ax,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        font_color='white',
        font_weight='bold',
        node_color=colors,
    )
    if title:
        ax.set_title(title, fontweight="bold", fontsize="20")
    plt.show(block=last)


def heap_to_tree(heap: list[Any], i: int = 0) -> Optional[Node]:
    """
    Builds a tree from a heap array (complete binary heap).

    :param heap: Heap list (List of any values)
    :param i: Index of the current node (Integer, optional)
    :return: Root of the tree or None, if the node is absent (Node, optional)
    """
    if i >= len(heap):
        return None

    heapq.heapify(heap)

    root = Node(heap[i])
    root.left = heap_to_tree(heap, 2 * i + 1)
    root.right = heap_to_tree(heap, 2 * i + 2)
    return root
