from millenium_falcon.services.falcon_service import FalconService


def test_falcon_service_example_1(routes):
    service = FalconService(6, "Tatooine", "Endor", routes)
    bounty_hunters = [
        ("Hoth", 6),
        ("Hoth", 7),
        ("Hoth", 8),
    ]
    trip, score = service.success_probability(
        countdown=7,
        bounty_hunters=bounty_hunters,
    )
    assert trip is None
    assert score == 0


def test_falcon_service_example_2(routes):
    service = FalconService(6, "Tatooine", "Endor", routes)
    bounty_hunters = [
        ("Hoth", 6),
        ("Hoth", 7),
        ("Hoth", 8),
    ]
    trip, score = service.success_probability(
        countdown=8,
        bounty_hunters=bounty_hunters,
    )
    assert trip == {0: "Tatooine", 6: "Hoth", 7: "Hoth", 8: "Endor"}
    assert score == 81


def test_falcon_service_example_3(routes):
    service = FalconService(6, "Tatooine", "Endor", routes)
    bounty_hunters = [
        ("Hoth", 6),
        ("Hoth", 7),
        ("Hoth", 8),
    ]
    trip, score = service.success_probability(
        countdown=9,
        bounty_hunters=bounty_hunters,
    )
    assert trip == {0: "Tatooine", 6: "Dagobah", 7: "Dagobah", 8: "Hoth", 9: "Endor"}
    assert score == 90
