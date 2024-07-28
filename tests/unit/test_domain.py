from millenium_falcon.domain import Routes, Route

data = [
    ("Tatooine", "Dagobah", 6),
    ("Dagobah", "Endor", 4),
    ("Dagobah", "Hoth", 1),
    ("Hoth", "Endor", 1),
    ("Tatooine", "Hoth", 6),
]


def test_build_routes():
    routes = Routes(data)
    assert routes.routes == {
        "Tatooine": {"Dagobah": 6, "Hoth": 6},
        "Dagobah": {"Tatooine": 6, "Endor": 4, "Hoth": 1},
        "Endor": {"Dagobah": 4, "Hoth": 1},
        "Hoth": {"Dagobah": 1, "Endor": 1, "Tatooine": 6},
    }

    routes = Routes([])
    assert routes.routes == {}


def test_next_hops():
    routes = Routes(data)
    assert routes.next_hops("Tatooine") == [
        Route("Tatooine", "Dagobah", 6),
        Route("Tatooine", "Hoth", 6),
    ]
    assert routes.next_hops("Dagobah") == [
        Route("Dagobah", "Tatooine", 6),
        Route("Dagobah", "Endor", 4),
        Route("Dagobah", "Hoth", 1),
    ]

    assert routes.next_hops("Endor") == [
        Route("Endor", "Dagobah", 4),
        Route("Endor", "Hoth", 1),
    ]
    assert routes.next_hops("Hoth") == [
        Route("Hoth", "Dagobah", 1),
        Route("Hoth", "Endor", 1),
        Route("Hoth", "Tatooine", 6),
    ]

    assert routes.next_hops("Coruscant") == []
    assert routes.next_hops("Earth") == []


def test_find_route():
    routes = Routes(data)
    assert routes.find_route("Tatooine", "Dagobah") == Route("Tatooine", "Dagobah", 6)
    assert routes.find_route("Tatooine", "Endor") is None
    assert routes.find_route("Dagobah", "Endor") == Route("Dagobah", "Endor", 4)
    assert routes.find_route("Hoth", "Endor") == Route("Hoth", "Endor", 1)
    assert routes.find_route("Hoth", "Tatooine") == Route("Hoth", "Tatooine", 6)
    assert routes.find_route("Endor", "Hoth") == Route("Endor", "Hoth", 1)
    assert routes.find_route("Endor", "Tatooine") is None
    assert routes.find_route("Dagobah", "Tatooine") == Route("Dagobah", "Tatooine", 6)
    assert routes.find_route("Dagobah", "Hoth") == Route("Dagobah", "Hoth", 1)
    assert routes.find_route("Hoth", "Dagobah") == Route("Hoth", "Dagobah", 1)
    assert routes.find_route("Hoth", "Tatooine") == Route("Hoth", "Tatooine", 6)
    assert routes.find_route("Endor", "Dagobah") == Route("Endor", "Dagobah", 4)
    assert routes.find_route("Endor", "Tatooine") is None
    assert routes.find_route("Tatooine", "Endor") is None
    assert routes.find_route("Tatooine", "Hoth") == Route("Tatooine", "Hoth", 6)
    assert routes.find_route("Dagobah", "Hoth") == Route("Dagobah", "Hoth", 1)
    assert routes.find_route("Dagobah", "Endor") == Route("Dagobah", "Endor", 4)
    assert routes.find_route("Hoth", "Endor") == Route("Hoth", "Endor", 1)
    assert routes.find_route("Earth", "Tatooine") is None
    assert routes.find_route("Tatooine", "Earth") is None
