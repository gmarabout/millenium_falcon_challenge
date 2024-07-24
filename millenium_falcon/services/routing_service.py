import logging
from typing import List, Tuple

from ..adapters.repository import RouteRepository
from ..domain.bounty_hunter import BountyHunter
from ..domain.route import Trip
from ..util.routing import compute_all_trips
from ..util.scoring import count_bounty_hunter_days, probability_not_captured

logger = logging.getLogger(__name__)


class RoutingService:
    def __init__(self, route_repository: RouteRepository):
        self.route_repository = route_repository

    def get_odds(
        self,
        departure: str,
        arrival: str,
        autonomy: int,
        countdown: int,
        bounty_hunters: List[BountyHunter],
    ) -> Tuple[Trip, int]:
        """
        Compute the odds of successfully reaching the destination without being captured by bounty hunters.
        """
        # Get all routes from database
        routes = self.route_repository.get_all()

        # Compute all possible trips
        all_trips = compute_all_trips(departure, arrival, routes, countdown, autonomy)

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
