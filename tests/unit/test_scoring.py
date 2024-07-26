from millenium_falcon.scoring import (
    count_bounty_hunter_days,
    probability_not_captured,
)
import pytest


test_cases = [
    (
        # Trip
        {
            0: "Tatooine",
            3: "Bespin",
            4: "Bespin",
            5: "Naboo",
            6: "Naboo",
            7: "Naboo",
        },
        # Bounty hunters
        [
            ("Tatooine", 1),
            ("Tatooine", 2),
            ("Bespin", 2),
            ("Bespin", 3),
            ("Bespin", 4),
            ("Naboo", 4),
            ("Naboo", 5),
        ],
        3,
    ),
    (
        # Trip
        {
            0: "Tatooine",
            1: "Tatooine",
            2: "Tatooine",
            3: "Tatooine",
            4: "Tatooine",
            5: "Tatooine",
        },
        # Bounty hunters
        [
            ("Tatooine", 0),
            ("Tatooine", 1),
            ("Tatooine", 2),
            ("Tatooine", 3),
            ("Tatooine", 4),
            ("Tatooine", 5),
        ],
        6,
    ),
    (
        # Trip
        {
            0: "Tatooine",
            1: "Naboo",
            2: "Endor",
            3: "Mustafar",
            4: "Endor",
            5: "Alderaan",
        },
        # Bounty hunters
        [
            ("Naboo", 0),
            ("Tatooine", 1),
            ("Tatooine", 2),
            ("Endor", 3),
            ("Tatooine", 4),
            ("Tatooine", 5),
        ],
        0,
    ),
    (
        # Trip
        {
            0: "Tatooine",
            1: "Naboo",
            2: "Endor",
            3: "Mustafar",
            4: "Endor",
            5: "Alderaan",
        },
        # Bounty hunters
        [],
        0,
    ),
    (
        # Trip
        {
            0: "Tatooine",
            1: "Naboo",
            2: "Endor",
            3: "Mustafar",
            4: "Endor",
            5: "Alderaan",
        },
        # Bounty hunters
        [
            ("Tatooine", 0),
            ("Naboo", 1),
            ("Endor", 2),
            ("Mustafar", 3),
            ("Endor", 4),
            ("Alderaan", 5),
        ],
        6,
    ),
]


@pytest.mark.parametrize("trip, bounty_hunters, expected_days", test_cases)
def test_count_bounty_hunter_days(trip, bounty_hunters, expected_days):
    assert count_bounty_hunter_days(trip, bounty_hunters) == expected_days


def test_probability_not_captured():
    assert probability_not_captured(0) == 100
    assert probability_not_captured(1) == 90
    assert probability_not_captured(2) == 81
    assert probability_not_captured(3) == 73
    # etc.

    # Just in case...
    with pytest.raises(ValueError):
        probability_not_captured(-1)
