# -*- coding: utf-8 -*-

"""
HomeWork Task 7
"""

import argparse
import collections

import numpy as np
import matplotlib.pyplot as plt


def theoretical_probabilities() -> dict[int, float]:
    """
    Theoretical probabilities of sums for two fair dice (1...6).

    :return: Probabilities for sums {2..12} (Dictionary)
    """
    ways = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    return {s: ways[s] / 36.0 for s in range(2, 13)}


def print_table(counts: dict[int, int], probabilities: dict[int, float]) -> None:
    """
    Table of results + theoretical values and error.

    :param counts: frequencies for sums {2..12} (Dictionary, mandatory)
    :param probabilities: probabilities for sums {2..12} (Dictionary, mandatory)
    """
    theory = theoretical_probabilities()
    simulation_numbers = sum(counts.values())

    print(f"\nResults of the two-dice roll Monte Carlo simulation (n_rolls = {simulation_numbers:,}):")
    print(" Sum |  Quantity  | Probability MC | Probability Theory | Δ = Probability(MC - Theory)")
    print("-----+------------+----------------+--------------------+------------------------------")
    for s in range(2, 13):
        p_mc = probabilities[s]
        p_theory = theory[s]
        print(f"{s:>4} | {counts[s]:>10} | {p_mc:>14.2%} | {p_theory:>18.2%} | {p_mc - p_theory:>= .6f}")


def plot_probabilities(probabilities: dict[int, float]) -> None:
    """
    Probability chart: Monte Carlo (bars) + theory (line).

    :param probabilities: probabilities for sums {2..12} (Dictionary, mandatory)
    """
    s_vals = np.arange(2, 13, dtype=np.int16)
    p_mc = np.array([probabilities[int(s)] for s in s_vals])
    p_th = np.array([theoretical_probabilities()[int(s)] for s in s_vals])

    plt.figure(figsize=(10, 6))
    plt.bar(s_vals, p_mc, width=0.3, label="MC", color="#5B8FF9")
    plt.plot(s_vals, p_th, "o-", label="Теорія", color="#EE6666")
    plt.xticks(s_vals)
    plt.xlabel("Sum on two dice")
    plt.ylabel("Probability")
    plt.title("Probabilities of sums (Monte Carlo vs Theory)")
    plt.grid(alpha=0.3, linestyle="--")
    plt.legend()
    plt.tight_layout()
    plt.show()


def dice_simulation(simulation_numbers: int, seed: int = 42) -> tuple[dict[int, int], dict[int, float]]:
    """
    Simulation of rolling two fair dice and estimating the probabilities of the sums.

    :param simulation_numbers: Number of rolls (large for stable estimates) (Integer, mandatory)
    :param seed: Initialization of the random number generator for reproducibility (Integer, optional)
    :return: Frequencies and probabilities for sums {2..12} (Tuple of DefaultDictionaries)
    """

    if simulation_numbers <= 0:
        raise ValueError("The number of rolls must be greater than zero")

    counts = collections.defaultdict(int)
    rng = np.random.default_rng(seed)
    dices = rng.integers(1, 7, size=(simulation_numbers, 2), dtype=np.int16)
    for idx in range(simulation_numbers):
        dice_1, dice_2 = dices[idx]
        counts[int(dice_1 + dice_2)] += 1
    # Sorting the counts by the sum of the dice values
    counts = dict(sorted(counts.items()))
    probabilities = {amount: count / simulation_numbers for amount, count in counts.items()}

    return counts, probabilities


def cli() -> None:
    try:
        parser = argparse.ArgumentParser(
            description="Simulation of rolling two fair dice and estimating the probabilities of the sums",
            epilog="Good bye!",
        )
        parser.add_argument("-r", "--rolls", type=int, default=1_000_000, help="Number of rolls (default 1000000)")

        args = parser.parse_args()

        counts, probabilities = dice_simulation(args.rolls)
        print_table(counts, probabilities)
        plot_probabilities(probabilities)
    except Exception as e:
        print(e)

    exit(0)
