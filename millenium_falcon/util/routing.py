from ..domain.route import Route
from typing import Set, List

REFULLING_TIME = 1  # Time to refuel the spaceship (in days)

# A trip is a dictionary where the key is the day and the value is the planet
# Example: { 0: "Tatooine", 1: "Tatooine", 7: "Dagobah", 9: "Endor" }
Trip = dict[int, str]


def compute_all_trips(
    origin: str, destination: str, routes: List[Route], max_time: int, autonomy: int
) -> List[Trip]:
    """Compute all path between origin and destination that fits in max_time."""

    # Initialization
    all_trips = []
    explore(origin, destination, routes, max_time, autonomy, 0, {0: origin}, all_trips)
    return all_trips


def explore(
    origin: str,
    destination: str,
    routes: List[Route],
    max_time: int,
    autonomy: int,
    current_time: int,
    current_trip: Trip,
    all_trips: List[Trip],
) -> None:
    """Explore all paths between origin and destination that fits in max_time."""

    # We have arrived at the destination
    if origin == destination:
        all_trips.append(current_trip)
        return

    # Let's find next hops...
    next_hops = [
        route
        for route in routes
        if route.origin == origin and route.destination not in current_trip.values()
    ]
    for route in next_hops:
        travel_time = route.travel_time
        arrival_time = current_time + travel_time
        if arrival_time <= max_time and autonomy >= travel_time:
            new_trip = current_trip.copy()
            new_trip[arrival_time] = route.destination
            explore(
                route.destination,
                destination,
                routes,
                max_time,
                autonomy,
                current_time + travel_time,
                new_trip,
                all_trips,
            )
    return
