"""
This module provides Falcon-related services.
"""

import logging
from typing import List, Tuple

from .domain import Trip, Route
from .routing import compute_all_trips
from .scoring import count_bounty_hunter_days, probability_not_captured

logger = logging.getLogger(__name__)


class FalconService:
    """
    The FalconService class represents a service for computing the probability of successfully reaching a destination
    without being captured by bounty hunters.

    Attributes:
        autonomy (int): The autonomy of the Millennium Falcon, representing the maximum number of days it can travel without refueling.
        departure (str): The departure location of the Millennium Falcon.
        arrival (str): The arrival location of the Millennium Falcon.
        all_routes (List[Route]): A list of all available routes for the Millennium Falcon to travel between locations.

    Methods:
        success_probability(countdown: int, bounty_hunters: List[Tuple[str, int]]) -> Tuple[Trip, int]:
            Compute the probability of successfully reaching the destination without being captured by bounty hunters.

    """

    def __init__(
        self, autonomy: int, departure: str, arrival: str, all_routes: List[Route]
    ):
        self.autonomy = autonomy
        self.departure = departure
        self.arrival = arrival
        self.all_routes = all_routes

    def success_probability(
        self,
        countdown: int,
        bounty_hunters: List[Tuple[str, int]],
    ) -> Tuple[Trip, int]:
        """
        Compute the probability of successfully reaching the destination without being captured by bounty hunters.

        Args:
            countdown (int): The remaining time in days before the Millennium Falcon must reach the destination.
            bounty_hunters (List[Tuple[str, int]]): A list of bounty hunters that may attempt to capture the Millennium Falcon.

        Returns:
            Tuple[Trip, int]: A tuple containing the best trip (Trip object) and its success probability (int).

        """
        # Compute all possible trips
        all_trips = compute_all_trips(
            self.departure, self.arrival, self.all_routes, countdown, self.autonomy
        )

        # Find the best trip
        best_score = 0
        best_trip = None
        for trip in all_trips:
            hunts = count_bounty_hunter_days(trip, bounty_hunters)
            score = probability_not_captured(hunts)
            if score > best_score:
                best_score = score
                best_trip = trip
        logger.debug(f"Best trip: {best_trip} with score {best_score}%")

        # Return the best trip and its score, if any
        return best_trip, best_score
