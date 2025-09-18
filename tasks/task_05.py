# -*- coding: utf-8 -*-

"""
HomeWork Task 5
"""

import argparse
import colorsys
from collections import deque
from typing import Optional

from .tree import Node, tree_draw, heap_to_tree


def tree_create(nodes_number: int = 15) -> Optional[Node]:
    """
    Creation of a binary tree from a min-heap with the specified number of vertices.

    :param nodes_number: Number of vertices (Integer, optional)
    :return: Root of the tree or None, if the node is absent (Node, optional)
    """

    # Min-heap as an array
    heap_array = [2 * n + 1 for n in range(nodes_number)]
    return heap_to_tree(heap_array)


def bfs(root: Optional[Node], colors: Optional[list[str]] = None) -> list[Node]:
    """
    Breadth-first traversal of the tree (BFS).

    :param root: Root node of the tree (Node, mandatory)
    :param colors: List of colors (List of String, optional)
    :return: List of vertices in traversal order (List of Node)
    """
    if root is None:
        return []

    result: list[Node] = []
    q: deque[Node] = deque([root])

    while q:
        node = q.popleft()
        if colors:
            node.color = colors[len(result)]
        result.append(node)

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    return result


def dfs_preorder(root: Optional[Node], colors: Optional[list[str]] = None) -> list[Node]:
    """
    Depth-first traversal of the tree (DFS, preorder).

    :param root: Root node of the tree (Node, mandatory)
    :param colors: List of colors (List of String, optional)
    :return: List of vertices in traversal order (List of Node)
    """
    if root is None:
        return []

    result: list[Node] = []
    stack: list[Node] = [root]

    while stack:
        # Take a node from the stack
        node = stack.pop()
        if node is None:
            continue

        # Add node to the path
        if colors:
            node.color = colors[len(result)]
        result.append(node)

        # First add the right child, then the left → so that the left one is processed first.
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


def dfs_inorder(root: Optional[Node], colors: Optional[list[str]] = None) -> list[Node]:
    """
    Depth-first traversal of the tree (DFS, inorder).

    :param root: Root node of the tree (Node, mandatory)
    :param colors: List of colors (List of String, optional)
    :return: List of vertices in traversal order (List of Node)
    """
    result: list[Node] = []
    stack: list[Node] = []
    current = root

    while current or stack:
        # Go as far left as possible
        while current:
            stack.append(current)
            current = current.left

        # Take a node from the stack
        current = stack.pop()
        if current is None:
            continue

        # Add node to the path
        if colors:
            current.color = colors[len(result)]
        result.append(current)

        # Move to the right
        current = current.right

    return result


def dfs_postorder(root: Optional[Node], colors: Optional[list[str]] = None) -> list[Node]:
    """
    Depth-first traversal of the tree (DFS, postorder).

    :param root: Root node of the tree (Node, mandatory)
    :param colors: List of colors (List of String, optional)
    :return: List of vertices in traversal order (List of Node)
    """
    if root is None:
        return []

    result: list[Node] = []
    # Tuple (node, flag indicating whether it has been visited)
    stack: list[tuple[Node, bool]] = [(root, False)]

    while stack:
        # Take a node from the stack
        node, visited = stack.pop()
        if node is None:
            continue

        if visited:
            # Add node to the path
            if colors:
                node.color = colors[len(result)]
            result.append(node)
        else:
            # Push onto the stack in the order: root (marked) → right → left
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))

    return result


def generate_colors(colors_number: int = 15) -> list[str]:
    """
    Generate colors_number colors in HEX (#RRGGBB), from dark to light, using shades of blue.

    :param colors_number: Number of colors (Integer, optional)
    :return: List of colors (List of String)
    """
    colors = []
    for i in range(colors_number):
        # Shade of blue
        h = 210 / 360.0
        # Saturation
        s = 0.8
        # Brightness from 0.1 to 1.0
        v = 0.1 + 0.9 * (i / max(1, colors_number - 1))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        colors.append(f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}")
    return colors


def cli() -> None:
    try:
        parser = argparse.ArgumentParser(description="Builds and visualizes a tree", epilog="Good bye!")
        parser.add_argument("-n", "--nodes", type=int, default=15, help="Number of nodes (default 15)")

        args = parser.parse_args()

        root = tree_create(nodes_number=args.nodes)
        colors: list[str] = generate_colors(args.nodes)

        # Make BFS and visualize the result
        print("BFS path:", " -> ".join(str(n) for n in bfs(root, colors=colors)))
        tree_draw(root, title="BFS Traversal")

        # Make DFS preorder and visualize the result
        print("DFS preorder path:", " -> ".join(str(n) for n in dfs_preorder(root, colors=colors)))
        tree_draw(root, title="DFS PREORDER Traversal")

        # Make DFS inorder and visualize the result
        print("DFS inorder path:", " -> ".join(str(n) for n in dfs_inorder(root, colors=colors)))
        tree_draw(root, title="DFS INORDER Traversal")

        # Make DFS postorder and visualize the result
        print("DFS postorder path:", " -> ".join(str(n) for n in dfs_postorder(root, colors=colors)))
        tree_draw(root, title="DFS POSTORDER Traversal")

    except Exception as e:
        print(e)

    exit(0)
