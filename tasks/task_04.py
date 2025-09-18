# -*- coding: utf-8 -*-

"""
HomeWork Task 4
"""

import argparse

from .tree import tree_draw, heap_to_tree


def heap_visualization(nodes_number: int = 15) -> None:
    """
    Creation and visualization of a binary tree from a min-heap with the specified number of vertices.

    :param nodes_number: Number of vertices (Integer, optional)
    """

    # Min-heap as an array
    heap_array = [2 * n + 1 for n in range(nodes_number)]

    root = heap_to_tree(heap_array)

    tree_draw(root)


def cli() -> None:
    try:
        parser = argparse.ArgumentParser(description="Builds and visualizes a tree", epilog="Good bye!")
        parser.add_argument("-n", "--nodes", type=int, default=15, help="Number of nodes (default 15)")

        args = parser.parse_args()

        heap_visualization(nodes_number=args.nodes)
    except Exception as e:
        print(e)

    exit(0)
