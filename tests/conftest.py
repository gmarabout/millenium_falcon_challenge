from typing import List

import pytest
from sqlalchemy import Engine, create_engine

from flask_app import app
from millenium_falcon.domain import Route
from millenium_falcon.route_loader import RouteLoader


@pytest.fixture
def db_engine() -> Engine:
    engine = create_engine("sqlite:///universe.db")
    return engine


@pytest.fixture
def route_loader(db_engine: Engine) -> RouteLoader:
    return RouteLoader(db_engine)


@pytest.fixture
def routes(route_loader: RouteLoader) -> List[Route]:
    return route_loader.load_all_routes()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
