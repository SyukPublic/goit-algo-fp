# -*- coding: utf-8 -*-

"""
HomeWork Task 6
"""

import argparse


def greedy_algorithm(items: dict[str, dict[str, int]], budget: int) -> dict[str, int]:
    """
    Selecting the combination of foods with the highest total calories within a limited budget (Greedy algorithm).

    :param items: A catalog of dishes with their cost and calorie content (Dictionary, mandatory)
    :param budget: Specified budget (Integer, mandatory)
    :return: Selected dishes, total calories, and budget spent (Dictionary)
    """

    # Розрахунок співвідношення калорій до вартості
    items_sorted: list[tuple[str, dict[str, int]]] = sorted(
        items.items(),
        key=lambda x: (
            x[1].get("calories") / x[1].get("cost") if len(x) >= 2 and x[1].get("calories") and x[1].get("cost") else 0
        ),
        reverse=True
    )

    total_cost: int = 0
    total_calories: int = 0
    chosen_items: list[str] = []

    for item_name, item_info in items_sorted:
        if total_cost + int(item_info.get("cost", 0)) <= budget:
            total_cost += int(item_info.get("cost", 0))
            total_calories += int(item_info.get("calories", 0))
            chosen_items.append(item_name)

    return dict(total_calories=total_calories, total_cost=total_cost, items=chosen_items)


def dynamic_programming(items: dict[str, dict[str, int]], budget: int) -> dict[str, int]:
    """
    Selecting the combination of foods with the highest total calories within a limited budget (Dynamic programming).

    :param items: A catalog of dishes with their cost and calorie content (Dictionary, mandatory)
    :param budget: Specified budget (Integer, mandatory)
    :return: Selected dishes, total calories, and budget spent (Dictionary)
    """

    names = list(items.keys())
    items_number = len(names)

    # dp[i][a] = Maximum calories from the first i items with a budget of a
    amount_calories_matrix = [[0] * (budget + 1) for _ in range(items_number + 1)]

    for i in range(1, items_number + 1):
        item = items[names[i - 1]]
        for a in range(budget + 1):
            if item.get("cost", 0) > a:
                amount_calories_matrix[i][a] = amount_calories_matrix[i - 1][a]
            else:
                amount_calories_matrix[i][a] = max(
                    amount_calories_matrix[i - 1][a],  # Do not take the item
                    amount_calories_matrix[i - 1][a - item.get("cost", 0)] + item.get("calories", 0)  # Take the item
                )

    # Restore the chosen items
    a = budget
    chosen_items = []
    for i in range(items_number, 0, -1):
        if amount_calories_matrix[i][a] != amount_calories_matrix[i - 1][a]:
            item_name = names[i - 1]
            chosen_items.append(item_name)
            a -= items[item_name].get("cost", 0)

    return dict(
        total_calories=amount_calories_matrix[items_number][budget],
        total_cost=sum(items[i].get("cost", 0) for i in chosen_items),
        items=list(reversed(chosen_items)),
    )


def cli() -> None:
    try:
        items: dict[str, dict[str, int]] = {
            "pizza": {"cost": 50, "calories": 300},
            "hamburger": {"cost": 40, "calories": 250},
            "hot-dog": {"cost": 30, "calories": 200},
            "pepsi": {"cost": 10, "calories": 100},
            "cola": {"cost": 15, "calories": 220},
            "potato": {"cost": 25, "calories": 350}
        }

        parser = argparse.ArgumentParser(
            description="Selecting the combination of foods with the highest total calories within a limited budget",
            epilog="Good bye!",
        )
        parser.add_argument("-b", "--budget", type=int, default=100, help="Budget (default 100)")

        args = parser.parse_args()

        budget = args.budget
        print("Selected items by Greedy algorithm:")
        print(greedy_algorithm(items, budget))
        print()
        print("Selected items by Dynamic programming:")
        print(dynamic_programming(items, budget))

    except Exception as e:
        print(e)

    exit(0)
