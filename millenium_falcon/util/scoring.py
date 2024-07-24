"""
This module provides functions to compute the odds of being captured by a bounty hunter.
"""

import math

from ..domain.bounty_hunter import BountyHunter, Hunt
from ..domain.route import Trip


def count_bounty_hunter_days(trip: Trip, hunt: Hunt) -> int:
    """Count the number of days spent on a planet when a bounty hunter is present."""
    n = 0
    for day, planet in trip.items():
        for hunter in hunt:
            if hunter.planet == planet and hunter.day == day:
                n += 1
    return n


def probability_captured(n: int) -> int:
    """Compute the probability of being captured after visiting n times a planet with a bounty hunter."""
    if n < 0:
        raise ValueError("n should be positive")
    # Han Solo has 1/10 change of being captured when a bounty hunter is on the same planet.
    # So it has 0.9 chance of not being captured.
    # After n planets, the probability of not being captured is `(0.9)^n`.
    # So, the probability of being captured, after visiting n planets where there was a bounty hunter is `1 - (0.9)^n`.
    # This can be written in Python as:
    p_captured = 1 - 0.9**n

    # We round the result to 3 decimals:
    return math.ceil(p_captured * 1000) / 1000
