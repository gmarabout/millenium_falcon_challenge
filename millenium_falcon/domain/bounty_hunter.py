from dataclasses import dataclass
from typing import List


@dataclass
class BountyHunter:
    """A bounty hunter with a planet and a day to catch the Falcon."""

    planet: str
    day: int


# A hunt is a list of bounty hunters.
# Example: [BountyHunter("Tatooine", 7), BountyHunter("Endor", 9)]
Hunt = List[BountyHunter]
