from millenium_falcon.services.routing_service import RoutingService
from millenium_falcon.domain.bounty_hunter import BountyHunter


def test_routing_service_example_1(repository):
    routing_service = RoutingService(repository)
    bounty_hunters = [
        BountyHunter("Hoth", 6),
        BountyHunter("Hoth", 7),
        BountyHunter("Hoth", 8),
    ]
    trip, score = routing_service.get_odds(
        departure="Tatooine",
        arrival="Endor",
        autonomy=6,
        countdown=7,
        bounty_hunters=bounty_hunters,
    )
    assert trip is None
    assert score == 0


def test_routing_service_example_2(repository):
    routing_service = RoutingService(repository)
    bounty_hunters = [
        BountyHunter("Hoth", 6),
        BountyHunter("Hoth", 7),
        BountyHunter("Hoth", 8),
    ]
    trip, score = routing_service.get_odds(
        departure="Tatooine",
        arrival="Endor",
        autonomy=6,
        countdown=8,
        bounty_hunters=bounty_hunters,
    )
    assert trip == {0: "Tatooine", 6: "Hoth", 7: "Hoth", 8: "Endor"}
    assert score == 81


def test_routing_service_example_3(repository):
    routing_service = RoutingService(repository)
    bounty_hunters = [
        BountyHunter("Hoth", 6),
        BountyHunter("Hoth", 7),
        BountyHunter("Hoth", 8),
    ]
    trip, score = routing_service.get_odds(
        departure="Tatooine",
        arrival="Endor",
        autonomy=6,
        countdown=9,
        bounty_hunters=bounty_hunters,
    )
    assert trip == {0: "Tatooine", 6: "Dagobah", 7: "Dagobah", 8: "Hoth", 9: "Endor"}
    assert score == 90
