from pprint import pprint

import pytest

from millenium_falcon.routing import (
    compute_all_trips,
    check_autonomy,
    check_deadline,
    check_distances,
)
from millenium_falcon.domain import Routes


_ROUTES = [
    ("Tatooine", "Dagobah", 6),
    ("Dagobah", "Endor", 4),
    ("Dagobah", "Hoth", 1),
    ("Hoth", "Endor", 1),
    ("Tatooine", "Hoth", 6),
    # Extra routes
    ("Coruscant", "Alderaan", 4),
    ("Tatooine", "Naboo", 3),
    ("Naboo", "Bespin", 2),
    ("Bespin", "Yavin", 5),
    ("Yavin", "Kashyyyk", 4),
    ("Kashyyyk", "Corellia", 6),
    ("Corellia", "Mustafar", 3),
    ("Mustafar", "Kamino", 5),
    ("Kamino", "Geonosis", 2),
    ("Geonosis", "Jakku", 4),
    ("Jakku", "Scarif", 3),
    ("Scarif", "Coruscant", 6),
    ("Alderaan", "Endor", 3),
    ("Endor", "Yavin", 4),
    ("Yavin", "Hoth", 2),
    ("Hoth", "Naboo", 5),
    ("Naboo", "Kamino", 3),
    ("Kamino", "Mustafar", 4),
    ("Mustafar", "Corellia", 6),
    ("Corellia", "Tatooine", 5),
    ("Corellia", "Geonosis", 6),
    ("Tatooine", "Jakku", 4),
    ("Jakku", "Kashyyyk", 6),
    ("Kashyyyk", "Geonosis", 4),
    ("Geonosis", "Dagobah", 3),
    ("Dagobah", "Scarif", 2),
    ("Scarif", "Bespin", 6),
    ("Bespin", "Alderaan", 3),
    ("Alderaan", "Kamino", 4),
    ("Kamino", "Coruscant", 3),
    ("Dantooine", "Geonosis", 5),
]


def build_routes():
    return Routes(_ROUTES)


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
    routes = build_routes()
    assert check_distances({0: "Tatooine", 6: "Dagobah"}, routes)
    assert check_distances({0: "Tatooine", 6: "Dagobah", 7: "Hoth"}, routes)
    assert check_distances({0: "Tatooine", 6: "Dagobah", 7: "Hoth", 8: "Endor"}, routes)
    assert check_distances(
        {0: "Tatooine", 6: "Hoth", 7: "Hoth", 8: "Hoth", 9: "Endor"}, routes
    )
    assert not check_distances(
        {0: "Tatooine", 6: "Dagobah", 7: "Endor"}, routes
    )  # Wrong travel time (Dagobah -> Endor)
    assert not check_distances(
        {0: "Tatooine", 6: "Dagobah", 7: "Coruscant"}, routes
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
    routes = build_routes()
    trips = compute_all_trips(origin, destination, routes, max_time, autonomy)

    # Check we found the expected number of trips
    assert len(trips) == expected, "Number of trips does not match"

    # Make sure we don't produce duplicated trips...
    trips_as_tuples = [tuple(trip.items()) for trip in trips]
    assert len(set(trips_as_tuples)) == len(trips_as_tuples), "Duplicate trips found"

    # Check each trip
    for trip in trips:
        assert check_autonomy(trip, autonomy), "Autonomy check failed"
        assert check_deadline(trip, max_time), "Deadline check failed"
        assert check_distances(trip, routes), "Distance check failed"


def test_compute_all_trips_errors():
    routes = build_routes()
    # No routes given
    with pytest.raises(ValueError):
        compute_all_trips("Tatooine", "Endor", [], 10, 6)

    # Negative max_time
    with pytest.raises(ValueError):
        compute_all_trips("Tatooine", "Endor", routes, -1, 6)

    # Negative autonomy
    with pytest.raises(ValueError):
        compute_all_trips("Tatooine", "Endor", routes, 10, -1)
