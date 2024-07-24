import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from millenium_falcon.adapters.repository import SQLAlchemyRouteRepository


@pytest.fixture
def db_engine():
    engine = create_engine("sqlite:///universe.db")
    return engine


@pytest.fixture
def repository(db_engine):
    return SQLAlchemyRouteRepository(db_engine)
