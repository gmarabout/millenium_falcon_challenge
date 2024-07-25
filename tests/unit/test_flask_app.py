def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data is not None


def test_get_falcon_success_probability(client):
    plans = {
        "countdown": 8,
        "bounty_hunters": [
            {"planet": "Hoth", "day": 6},
            {"planet": "Hoth", "day": 7},
            {"planet": "Hoth", "day": 8},
        ],
    }

    response = client.post("/api/falcon/success_probability", json=plans)
    assert response.status_code == 200
    assert response.json == {
        "score": 81,
        "trip": {"0": "Tatooine", "6": "Hoth", "7": "Hoth", "8": "Endor"},
    }


def test_get_falcon_success_probability_error(client):
    plans = {
        "These are not": "the droids you are looking for",
    }

    response = client.post("/api/falcon/success_probability", json=plans)
    assert response.status_code == 400
