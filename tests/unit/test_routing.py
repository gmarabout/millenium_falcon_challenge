from pprint import pprint

import pytest

from millenium_falcon.domain.route import Route, Trip
from millenium_falcon.util.routing import (
    compute_all_trips,
    check_autonomy,
    check_deadline,
    check_distances,
)


_ROUTES = [
    Route("Tatooine", "Dagobah", 6),
    Route("Dagobah", "Endor", 4),
    Route("Dagobah", "Hoth", 1),
    Route("Hoth", "Endor", 1),
    Route("Tatooine", "Hoth", 6),
    # Some additional routes:
    Route("Coruscant", "Alderaan", 4),
    Route("Tatooine", "Naboo", 3),
    Route("Naboo", "Bespin", 2),
    Route("Bespin", "Yavin", 5),
    Route("Yavin", "Kashyyyk", 4),
    Route("Kashyyyk", "Corellia", 6),
    Route("Corellia", "Mustafar", 3),
    Route("Mustafar", "Kamino", 5),
    Route("Kamino", "Geonosis", 2),
    Route("Geonosis", "Jakku", 4),
    Route("Jakku", "Scarif", 3),
    Route("Scarif", "Coruscant", 6),
    Route("Alderaan", "Endor", 3),
    Route("Endor", "Yavin", 4),
    Route("Yavin", "Hoth", 2),
    Route("Hoth", "Naboo", 5),
    Route("Naboo", "Kamino", 3),
    Route("Kamino", "Mustafar", 4),
    Route("Mustafar", "Corellia", 6),
    Route("Corellia", "Tatooine", 5),
    Route("Corellia", "Geonosis", 6),
    Route("Tatooine", "Jakku", 4),
    Route("Jakku", "Kashyyyk", 6),
    Route("Kashyyyk", "Geonosis", 4),
    Route("Geonosis", "Dagobah", 3),
    Route("Dagobah", "Scarif", 2),
    Route("Scarif", "Bespin", 6),
    Route("Bespin", "Alderaan", 3),
    Route("Alderaan", "Kamino", 4),
    Route("Kamino", "Coruscant", 3),
    Route("Dantooine", "Geonosis", 5),
]


def get_all_routes():
    # Routes are bidirectional
    return _ROUTES + [
        Route(route.destination, route.origin, route.travel_time) for route in _ROUTES
    ]


def test_check_autonomy():
    # No refuel needed
    assert check_autonomy({0: "Tatooine", 6: "Dagobah"}, 6)
    assert check_autonomy({0: "Tatooine", 1: "Tatooine", 5: "Hoth"}, 6)

    # Refueled
    assert check_autonomy({0: "Tatooine", 6: "Dagobah", 7: "Dagobah", 13: "Hoth"}, 6)
    assert check_autonomy(
        {
            0: "Tatooine",
            1: "Tatooine",
            5: "Hoth",
            6: "Hoth",
            7: "Hoth",
            12: "Endor",
            13: "Death Star",
        },
        6,
    )

    # Not enough autonomy
    assert not check_autonomy({0: "Tatooine", 6: "Hoth", 20: "Endor"}, 5)
    assert not check_autonomy({0: "Tatooine", 6: "Dagobah", 7: "Hoth", 8: "Endor"}, 5)
    assert not check_autonomy(
        {
            0: "Tatooine",
            1: "Tatooine",
            2: "Tatooine",
            8: "Dagobah",
            9: "Dagobah",
            10: "Dagobah",
            14: "Endor",
        },
        2,
    )


def test_check_deadlines():
    assert check_deadline({0: "Tatooine", 6: "Dagobah"}, 7)
    assert check_deadline({0: "Tatooine", 1: "Tatooine", 5: "Hoth"}, 6)
    assert check_deadline({0: "Tatooine", 6: "Dagobah", 7: "Dagobah", 13: "Hoth"}, 14)
    assert check_deadline({0: "Tatooine", 6: "Dagobah"}, 6)
    assert not check_deadline(
        {0: "Tatooine", 6: "Dagobah", 7: "Dagobah", 13: "Hoth"}, 5
    )
    assert not check_deadline({0: "Tatooine", 6: "Dagobah"}, 5)


def test_check_distances():
    assert check_distances({0: "Tatooine", 6: "Dagobah"}, get_all_routes())
    assert check_distances({0: "Tatooine", 6: "Dagobah", 7: "Hoth"}, get_all_routes())
    assert check_distances(
        {0: "Tatooine", 6: "Dagobah", 7: "Hoth", 8: "Endor"}, get_all_routes()
    )
    assert check_distances(
        {0: "Tatooine", 6: "Hoth", 7: "Hoth", 8: "Hoth", 9: "Endor"}, get_all_routes()
    )
    assert not check_distances(
        {0: "Tatooine", 6: "Dagobah", 7: "Endor"}, get_all_routes()
    )  # Wrong travel time (Dagobah -> Endor)
    assert not check_distances(
        {0: "Tatooine", 6: "Dagobah", 7: "Coruscant"}, get_all_routes()
    )  # Wrong destination (Coruscant)


TRIP_TEST_CASES = [
    (
        "Tatooine",
        "Endor",
        7,
        6,
        0,
    ),
    (
        "Tatooine",
        "Endor",
        10,
        6,
        6,
    ),
    (
        "Tatooine",
        "Endor",
        8,
        6,
        1,
    ),
    ("Tatooine", "Endor", 6, 6, 0),
    ("Tatooine", "Endor", 10, 2, 0),
    ("Tatooine", "Coruscant", 15, 4, 8),
    ("Tatooine", "Endor", 10, 100, 16),  # Plenty of autonomy
    ("Tatooine", "Endor", 100, 0, 0),  # No autonomy
    ("Tatooine", "Dantooine", 10, 5, 0),  # No route to destination
    ("Earth", "Tatooine", 10, 5, 0),  # Not a valid source
    ("Tatooine", "Earth", 10, 5, 0),  # Not a valid destination
]


@pytest.mark.parametrize(
    "origin, destination, max_time, autonomy, expected",
    TRIP_TEST_CASES,
)
def test_compute_all_trips(origin, destination, max_time, autonomy, expected):
    trips = compute_all_trips(origin, destination, get_all_routes(), max_time, autonomy)

    # Check we found the expected number of trips (empirical)
    assert len(trips) == expected, "Number of trips does not match"

    # Make sure we don't have duplicates...
    trips_as_tuples = [tuple(trip.items()) for trip in trips]
    assert len(set(trips_as_tuples)) == len(trips_as_tuples), "Duplicate trips found"

    # Check each trip
    for trip in trips:
        assert check_autonomy(trip, autonomy), "Autonomy check failed"
        assert check_deadline(trip, max_time), "Deadline check failed"
        assert check_distances(trip, get_all_routes()), "Distance check failed"


def test_compute_all_trips_errors():
    # No routes given
    with pytest.raises(ValueError):
        compute_all_trips("Tatooine", "Endor", [], 10, 6)

    # Negative max_time
    with pytest.raises(ValueError):
        compute_all_trips("Tatooine", "Endor", get_all_routes(), -1, 6)

    # Negative autonomy
    with pytest.raises(ValueError):
        compute_all_trips("Tatooine", "Endor", get_all_routes(), 10, -1)
