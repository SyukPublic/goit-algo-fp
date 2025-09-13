# -*- coding: utf-8 -*-

"""
HomeWork Task 2
"""

import argparse
import turtle
import math


def pythagoras_tree(t: turtle.Turtle, x: float, y: float, size: float, angle: float, depth: int) -> None:
    """Draw a single tree with the turtle

    :param t: Active turtle (Turtle, mandatory)
    :param x: X coordinate of the bottom point of the tree trunk in pixels (Float, mandatory)
    :param y: Y coordinate of the bottom point of the tree trunk in pixels (Float, mandatory)
    :param size: Tree trunk length in pixels (Float, mandatory)
    :param angle: Angle of tilt of the tree trunk (Float, mandatory)
    :param depth: Recursion depth (Integer, mandatory)
    """

    # Reduction factor
    factor = 0.7

    # Coordinates of the top point of the tree trunk in pixels
    x1 = x - size * math.cos(angle)
    y1 = y + size * math.sin(angle)

    # Draw the tree trunk
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x1, y1)
    t.penup()

    # End of draw
    if depth <= 1:
        return

    pythagoras_tree(t, x1, y1, factor * size, angle - math.pi / 4, depth - 1)
    pythagoras_tree(t, x1, y1, factor * size, angle + math.pi / 4, depth - 1)


def draw_pythagoras_tree(depth: int, size: float = 100) -> None:
    """Draw the Pythagoras tree

    :param depth: Recursion depth
    :param size: Size of tree trunk
    """

    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle(visible=False)
    t.speed(0)

    pythagoras_tree(t, 0, -size, size, math.pi / 2, depth)

    window.mainloop()


def cli() -> None:
    try:
        parser = argparse.ArgumentParser(description="Draw the Pythagoras tree", epilog="Good bye!")
        parser.add_argument("-d", "--depth", type=int, default=5, help="Recursion depth (default 5)")

        args = parser.parse_args()

        draw_pythagoras_tree(args.depth)
    except Exception as e:
        print(e)

    exit(0)
