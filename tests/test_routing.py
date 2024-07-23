from millenium_falcon.domain.route import Route
from millenium_falcon.util.routing import compute_all_trips

import pytest

routes = [
    Route("Tatooine", "Dagobah", 6),
    Route("Dagobah", "Endor", 4),
    Route("Dagobah", "Hoth", 1),
    Route("Hoth", "Endor", 1),
    Route("Tatooine", "Hoth", 6),
]


@pytest.mark.parametrize(
    "origin, destination, max_distance, autonomy, expected",
    [
        (
            "Tatooine",
            "Endor",
            10,
            -1,
            [
                {0: "Tatooine", 6: "Dagobah", 10: "Endor"},
                {0: "Tatooine", 6: "Dagobah", 7: "Hoth", 8: "Endor"},
                {0: "Tatooine", 6: "Hoth", 7: "Endor"},
            ],
        ),
        (
            "Tatooine",
            "Endor",
            8,
            -1,
            [
                {0: "Tatooine", 6: "Dagobah", 7: "Hoth", 8: "Endor"},
                {0: "Tatooine", 6: "Hoth", 7: "Endor"},
            ],
        ),
        ("Tatooine", "Endor", 6, -1, []),
    ],
)
def test_compute_all_trips(origin, destination, max_distance, autonomy, expected):
    compute_all_trips(origin, destination, routes, max_distance, autonomy) == expected
