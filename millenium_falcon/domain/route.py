from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Route:
    """A route between two planets with travel time (in days)."""

    origin: str
    destination: str
    travel_time: int
