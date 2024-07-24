from dataclasses import dataclass


@dataclass
class BountyHunter:
    """A bounty hunter with a planet and a day to catch the Falcon."""

    planet: str
    day: int
