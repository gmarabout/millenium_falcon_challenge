"""
Domain classes for the Millenium Falcon problem.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Route:
    """
    Represents a route between two planets.

    Attributes:
        origin (str): The origin planet.
        destination (str): The destination planet.
        travel_time (int): The travel time between the origin and destination planets.
    """

    origin: str
    destination: str
    travel_time: int

    def __str__(self):
        return f"{self.origin} -> {self.destination} ({self.travel_time} days)"


class Routes:
    """
    Represents a collection of routes between planets.

    Attributes:
        routes (dict[str, dict[str, int]]): A dictionary that stores the routes between planets and their travel times.

    Methods:
        __init__(routes: List[Tuple[str, str, int]]): Initializes the Routes object with a list of raw routes data.
        get_neighbours(planet: str) -> List[Tuple[str, int]]: Returns a list of neighboring planets and their travel times from the given planet.
        find_route(origin: str, destination: str) -> Tuple[str, int]: Finds the route from the given origin to the destination.
    """

    def __init__(self, data: List[Tuple[str, str, int]]):
        self.routes = {}  # type: dict[str, dict[str, int]]
        for row in data:
            origin = row[0]
            destination = row[1]
            travel_time = row[2]
            # We store both ways
            if origin not in self.routes:
                self.routes[origin] = {}
            self.routes[origin][destination] = travel_time
            if destination not in self.routes:
                self.routes[destination] = {}
            self.routes[destination][origin] = travel_time

    def next_hops(self, planet: str) -> List[Route]:
        """
        Returns a list of Route objects representing the neighboring planets and their travel times from the given planet.

        Parameters:
        - planet (str): The name of the planet.

        Returns:
        - List[Route]: A list of Route objects representing the neighboring planets and their travel times.
        """
        if planet not in self.routes.keys():
            return []
        return [
            Route(planet, neighbour, travel_time)
            for neighbour, travel_time in self.routes[planet].items()
        ]

    def find_route(self, origin: str, destination: str) -> Optional[Route]:
        """
        Finds a route from the given origin to the given destination.

        Args:
            origin (str): The starting point of the route.
            destination (str): The destination point of the route.

        Returns:
            Optional[Route]: The route from the origin to the destination, or None if no route is found.
        """
        routes_from_origin = self.next_hops(origin)
        if not routes_from_origin:
            return None
        return next(
            (route for route in routes_from_origin if route.destination == destination),
            None,
        )

    def __str__(self):
        return str(self.routes)


# A trip is a dictionary where the key is the day and the value is the planet where the Falcon is.
# Example: { 0: "Tatooine", 1: "Tatooine", 7: "Dagobah", 9: "Endor" }
# This allows easy "lookup by time".
Trip = dict[int, str]
