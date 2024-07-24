from millenium_falcon.util.scoring import count_bounty_hunter_days, probability_captured
from millenium_falcon.domain.bounty_hunter import BountyHunter, Hunt
import pytest


test_cases = [
    (
        {
            0: "Tatooine",
            3: "Bespin",
            4: "Bespin",
            5: "Naboo",
            6: "Naboo",
            7: "Naboo",
        },
        [
            BountyHunter("Tatooine", 1),
            BountyHunter("Tatooine", 2),
            BountyHunter("Bespin", 2),
            BountyHunter("Bespin", 3),
            BountyHunter("Bespin", 4),
            BountyHunter("Naboo", 4),
            BountyHunter("Naboo", 5),
        ],
        3,
    ),
    (
        {
            0: "Tatooine",
            1: "Tatooine",
            2: "Tatooine",
            3: "Tatooine",
            4: "Tatooine",
            5: "Tatooine",
        },
        [
            BountyHunter("Tatooine", 0),
            BountyHunter("Tatooine", 1),
            BountyHunter("Tatooine", 2),
            BountyHunter("Tatooine", 3),
            BountyHunter("Tatooine", 4),
            BountyHunter("Tatooine", 5),
        ],
        6,
    ),
    (
        {
            0: "Tatooine",
            1: "Naboo",
            2: "Endor",
            3: "Mustafar",
            4: "Endor",
            5: "Alderaan",
        },
        [
            BountyHunter("Naboo", 0),
            BountyHunter("Tatooine", 1),
            BountyHunter("Tatooine", 2),
            BountyHunter("Endor", 3),
            BountyHunter("Tatooine", 4),
            BountyHunter("Tatooine", 5),
        ],
        0,
    ),
    (
        {
            0: "Tatooine",
            1: "Naboo",
            2: "Endor",
            3: "Mustafar",
            4: "Endor",
            5: "Alderaan",
        },
        [],  # No Bounty hunters
        0,
    ),
    (
        {
            0: "Tatooine",
            1: "Naboo",
            2: "Endor",
            3: "Mustafar",
            4: "Endor",
            5: "Alderaan",
        },
        [
            BountyHunter("Tatooine", 0),
            BountyHunter("Naboo", 1),
            BountyHunter("Endor", 2),
            BountyHunter("Mustafar", 3),
            BountyHunter("Endor", 4),
            BountyHunter("Alderaan", 5),
        ],
        6,
    ),
]


@pytest.mark.parametrize("trip, hunt, expected_days", test_cases)
def test_count_bounty_hunter_days(trip, hunt, expected_days):
    assert count_bounty_hunter_days(trip, hunt) == expected_days


def test_probability_captured():
    assert probability_captured(0) == 0
    assert probability_captured(1) == 0.1
    assert probability_captured(2) == 0.19
    assert probability_captured(3) == 0.271
    assert probability_captured(4) == 0.344
    assert probability_captured(5) == 0.41
    assert probability_captured(6) == 0.469
    assert probability_captured(7) == 0.522
    assert probability_captured(8) == 0.57
    # etc.

    # Just in case...
    with pytest.raises(ValueError):
        probability_captured(-1)
