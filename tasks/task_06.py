# -*- coding: utf-8 -*-

"""
HomeWork Task 6
"""

import argparse
import collections


def greedy_algorithm(
        items: dict[str, dict[str, int]],
        budget: int,
        repeatable: bool = False,
) -> dict[str, int | collections.Counter]:
    """
    Selecting the combination of foods with the highest total calories within a limited budget (Greedy algorithm).

    :param items: A catalog of dishes with their cost and calorie content (Dictionary, mandatory)
    :param budget: Specified budget (Integer, mandatory)
    :param repeatable: Indicator of whether repeated selection of dishes is allowed (Boolean, optional)
    :return: Selected dishes, total calories, and budget spent (Dictionary)
    """

    def _non_repeatable_(_items_: list[tuple[str, dict[str, int]]]) -> tuple[int, int, list[str]]:
        _total_cost_: int = 0
        _total_calories_: int = 0
        _chosen_items_: list[str] = []
        for _name_, _info_ in _items_:
            if _total_cost_ + int(_info_.get("cost", 0)) <= budget:
                _total_cost_ += int(_info_.get("cost", 0))
                _total_calories_ += int(_info_.get("calories", 0))
                _chosen_items_.append(_name_)
        return _total_cost_, _total_calories_, _chosen_items_

    def _repeatable_(_items_: list[tuple[str, dict[str, int]]]) -> tuple[int, int, list[str]]:
        _total_cost_: int = 0
        _total_calories_: int = 0
        _chosen_items_: list[str] = []
        for _name_, _info_ in _items_:
            while _total_cost_ + int(_info_.get("cost", 0)) <= budget:
                _total_cost_ += int(_info_.get("cost", 0))
                _total_calories_ += int(_info_.get("calories", 0))
                _chosen_items_.append(_name_)
        return _total_cost_, _total_calories_, _chosen_items_

    # Розрахунок співвідношення калорій до вартості
    items_sorted: list[tuple[str, dict[str, int]]] = sorted(
        items.items(),
        key=lambda x: (
            x[1].get("calories") / x[1].get("cost") if len(x) >= 2 and x[1].get("calories") and x[1].get("cost") else 0
        ),
        reverse=True
    )

    selector = _repeatable_ if repeatable else _non_repeatable_
    total_cost, total_calories, chosen_items = selector(items_sorted)

    return dict(total_calories=total_calories, total_cost=total_cost, items=collections.Counter(chosen_items))


def dynamic_programming(
        items: dict[str, dict[str, int]],
        budget: int,
        repeatable: bool = False,
) ->dict[str, int | collections.Counter]:
    """
    Selecting the combination of foods with the highest total calories within a limited budget (Dynamic programming).

    :param items: A catalog of dishes with their cost and calorie content (Dictionary, mandatory)
    :param budget: Specified budget (Integer, mandatory)
    :param repeatable: Indicator of whether repeated selection of dishes is allowed (Boolean, optional)
    :return: Selected dishes, total calories, and budget spent (Dictionary)
    """

    def _non_repeatable_(_names_: list[str]) -> tuple[list[int], list[str]]:
        _items_number_ = len(_names_)

        # amount_calories_matrix[i][a] = Maximum calories from the first i items with a budget of a
        _amount_calories_matrix_: list[list[int]] = [[0] * (budget + 1) for _ in range(_items_number_ + 1)]

        for _i_ in range(1, _items_number_ + 1):
            item = items[_names_[_i_ - 1]]
            for _a_ in range(budget + 1):
                if item.get("cost", 0) > _a_:
                    _amount_calories_matrix_[_i_][_a_] = _amount_calories_matrix_[_i_ - 1][_a_]
                else:
                    _amount_calories_matrix_[_i_][_a_] = max(
                        # Do not take the item
                        _amount_calories_matrix_[_i_ - 1][_a_],
                        # Take the item
                        _amount_calories_matrix_[_i_ - 1][_a_ - item.get("cost", 0)] + item.get("calories", 0),
                    )

        # Restore the chosen items
        _a_: int = budget
        _chosen_items_: list[str] = []
        for _i_ in range(_items_number_, 0, -1):
            if _amount_calories_matrix_[_i_][_a_] != _amount_calories_matrix_[_i_ - 1][_a_]:
                _item_name_ = _names_[_i_ - 1]
                _chosen_items_.append(_item_name_)
                _a_ -= items[_item_name_].get("cost", 0)

        return _amount_calories_matrix_[_items_number_], _chosen_items_

    def _repeatable_(_names_: list[str]) -> tuple[list[int], list[str]]:

        # amount_calories_matrix[a] = Maximum calories with a budget of a
        _amount_calories_matrix_: list[int] = [0] * (budget + 1)
        _item_choice_: list[str|None] = [None] * (budget + 1)

        for _a_ in range(1, budget + 1):
            for _name_ in _names_:
                _cost_ = items[_name_].get("cost", 0)
                _calories_ = items[_name_].get("calories", 0)
                if _cost_ <= _a_ and _amount_calories_matrix_[_a_ - _cost_] + _calories_ > _amount_calories_matrix_[_a_]:
                    _amount_calories_matrix_[_a_] = _amount_calories_matrix_[_a_ - _cost_] + _calories_
                    _item_choice_[_a_] = _name_

        # Restore the chosen items
        _a_: int = budget
        _chosen_items_: list[str] = []
        while _a_ > 0 and _item_choice_[_a_] is not None:
            _name_ = _item_choice_[_a_]
            _chosen_items_.append(_name_)
            _a_ -= items[_name_].get("cost", 0)

        return _amount_calories_matrix_, _chosen_items_

    selector = _repeatable_ if repeatable else _non_repeatable_
    matrix, chosen_items = selector(list(items.keys()))

    return dict(
        total_calories=matrix[budget],
        total_cost=sum(items[i].get("cost", 0) for i in chosen_items),
        items=collections.Counter(chosen_items),
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
        print()
        print("Selected items by Greedy algorithm (non-repeatable):")
        print(greedy_algorithm(items, budget))
        print()
        print("Selected items by Dynamic programming (non-repeatable):")
        print(dynamic_programming(items, budget))
        print()
        print("Selected items by Greedy algorithm (repeatable):")
        print(greedy_algorithm(items, budget, repeatable=True))
        print()
        print("Selected items by Dynamic programming (repeatable):")
        print(dynamic_programming(items, budget, repeatable=True))
        print()

    except Exception as e:
        print(e)

    exit(0)
