"""
This module provides functions to compute all possible trips between two planets, respecting autonomy and time constraints.
"""

import logging
from typing import List

from ..domain.route import Route, Trip

logger = logging.getLogger(__name__)


REFUEL_TIME = 1  # The Falcon can refuel in 1 day


def compute_all_trips(
    origin: str, destination: str, routes: List[Route], max_time: int, autonomy: int
) -> List[Trip]:
    """
    Compute all paths between origin and destination that fits in max_time, respecting autonomy.
    We use a simple depth-first search algorithm to explore all possible paths.
    We also consider possible stops at each location to refuel the Falcon, or to avoid bounty hunters.
    However, we don't go back to already visited planets to be sure to find a solution in a fairly short amount of time.
    Avoiding bounty hunters by going back to already visited planets could be a good strategy, but we don't consider it here.
    """

    if max_time < 0:
        raise ValueError("max_time should be positive")
    if autonomy < 0:
        raise ValueError("autonomy should be positive")
    if not routes:
        raise ValueError("routes should not be empty")

    # Initial state
    all_trips = []
    initial_trip = {}

    # Recursively find all paths from origin to destination
    _explore(
        origin=origin,
        destination=destination,
        routes=routes,
        max_time=max_time,
        current_autonomy=autonomy,
        max_autonomy=autonomy,
        current_time=0,
        current_trip=initial_trip,
        all_trips=all_trips,
    )
    return all_trips


def _explore(
    origin: str,
    destination: str,
    routes: List[Route],
    max_time: int,
    current_autonomy: int,
    max_autonomy: int,
    current_time: int,
    current_trip: Trip,
    all_trips: List[Trip],
) -> None:
    """
    Explore all paths between origin and destination that fits in max_time, and respecting autonomy.
    Time complexity: O(max_time*num_of_planets*num_of_routes)
    Space complexity: O(max_time*num_of_planets)
    """
    current_trip[current_time] = origin

    logger.debug(
        f"Exploring {origin} -> {destination} at time {current_time} with autonomy {current_autonomy}"
    )

    # We have arrived at the destination
    if origin == destination:
        all_trips.append(current_trip)
        logger.debug(f"Found new trip: {current_trip}")
        return

    # We could decide to stay at the current planet for a while (ex: to refuel).
    # We can wait up to `max_time - current_time` days.
    for wait_time in range(max_time - current_time):
        if wait_time > 0:
            for i in range(wait_time + 1):
                # Mark the days spent on this planet
                # ex: `{..., 2: 'Tatooine', 3: 'Tatooine', 4: 'Tatooine', ...}`
                current_time += i
                current_trip[current_time] = origin

            # We have time to refuel the Falcon
            if wait_time >= REFUEL_TIME:
                current_autonomy = max_autonomy

        # Let's find next hops...
        visited = current_trip.values()
        next_hops = [
            route
            for route in routes
            if route.origin == origin and route.destination not in visited
        ]

        if not next_hops:
            # We are stuck, no more routes to explore
            return

        for route in next_hops:
            arrival_time = current_time + route.travel_time
            if arrival_time <= max_time and current_autonomy >= route.travel_time:
                new_autonomy = current_autonomy - route.travel_time
                new_trip = current_trip.copy()
                _explore(
                    origin=route.destination,
                    destination=destination,
                    routes=routes,
                    max_time=max_time,
                    current_autonomy=new_autonomy,
                    max_autonomy=max_autonomy,
                    current_time=arrival_time,
                    current_trip=new_trip,
                    all_trips=all_trips,
                )
    return


# ----------------------
# Check functions
# ----------------------


def check_autonomy(trip: Trip, autonomy: int) -> bool:
    """Check if the trip respects the given autonomy."""
    keys = trip.keys()
    remaining_autonomy = autonomy
    if keys:
        duration_at_same_location = 0
        previous_location = trip[0]
        previous_index = 0
        for i in sorted(keys):
            if i == 0:
                continue
            location = trip[i]
            if location == previous_location:
                duration_at_same_location += 1
                if duration_at_same_location >= REFUEL_TIME:
                    remaining_autonomy = autonomy
            else:
                duration_at_same_location = 0
                consumption = i - previous_index
                remaining_autonomy -= consumption
            if remaining_autonomy < 0:
                return False
            previous_location = location
            previous_index = i
    return True


def check_deadline(trip: Trip, deadline: int) -> bool:
    """Check if the trip respects the given deadline."""
    keys = trip.keys()
    if keys:
        return max(keys) <= deadline
    return True


def check_distances(trip: Trip, routes: List[Route]) -> bool:
    """Check if the trip respects the given distances."""
    keys = trip.keys()
    if keys:
        previous_location = trip[0]
        previous_index = 0
        for i in sorted(keys):
            if i == 0:
                continue
            location = trip[i]
            if location == previous_location:
                previous_index = i
                continue
            route = next(
                (
                    route
                    for route in routes
                    if route.origin == previous_location
                    and route.destination == location
                ),
                None,
            )
            if not route:
                return False
            if i - previous_index != route.travel_time:
                return False
            previous_location = location
            previous_index = i
    return True
