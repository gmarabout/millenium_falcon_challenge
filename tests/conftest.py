from typing import List

import pytest
from sqlalchemy import Engine, create_engine

from millenium_falcon.loaders.route_loader import RouteLoader
from millenium_falcon.domain.route import Route


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
