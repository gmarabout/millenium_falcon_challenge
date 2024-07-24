from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Route:
    """A route between two planets with travel time."""

    origin: str
    destination: str
    travel_time: int


# A trip is a dictionary where the key is the day and the value is the planet where the Falcon is.
# Example: { 0: "Tatooine", 1: "Tatooine", 7: "Dagobah", 9: "Endor" }
Trip = dict[int, str]


@dataclass
class BountyHunter:
    """A bounty hunter with a planet and a day to catch the Falcon."""

    planet: str
    day: int


# A hunt is a list of bounty hunters.
# Example: [BountyHunter("Tatooine", 7), BountyHunter("Endor", 9)]
Hunt = List[BountyHunter]
