from typing import List

import pytest
from sqlalchemy import create_engine

from millenium_falcon.adapters.repository import SQLAlchemyRouteRepository
from millenium_falcon.domain.route import Route


@pytest.fixture
def db_engine():
    engine = create_engine("sqlite:///universe.db")
    return engine


@pytest.fixture
def repository(db_engine):
    return SQLAlchemyRouteRepository(db_engine)


@pytest.fixture
def routes(repository) -> List[Route]:
    return repository.get_all()
