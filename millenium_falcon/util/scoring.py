"""
This module provides functions to compute the odds of being captured by a bounty hunter.
"""

import math
from typing import List, Tuple

from ..domain.route import Trip


def count_bounty_hunter_days(trip: Trip, bounty_hunters: List[Tuple[str, int]]) -> int:
    """Count the number of days spent on a planet when a bounty hunter is present."""
    n = 0
    for day, planet in trip.items():
        for hunter in bounty_hunters:
            if hunter[0] == planet and hunter[1] == day:
                n += 1
    return n


def probability_not_captured(n: int) -> int:
    """Compute the probability of being captured after visiting n times a planet with a bounty hunter."""
    if n < 0:
        raise ValueError("n should be positive")
    # Han Solo has 1/10 change of being captured when a bounty hunter is on the same planet.
    # So it has 0.9 chance of not being captured.
    # After n planets, the probability of not being captured is `(0.9)^n`.
    # This can be written in Python as:
    p_not_captured = 0.9**n
    # We return the probability as an integer percentage.
    return math.ceil(p_not_captured * 100)
