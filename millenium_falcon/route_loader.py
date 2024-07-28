"""
This module is responsible for loading routes from the database.
It uses SQLAlchemy to interact with the database and load the routes.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


class RouteLoader:
    def __init__(self, engine):
        self.route_table = Table(
            "routes",
            MetaData(),
            autoload_with=engine,
        )
        self.session = sessionmaker(bind=engine)()

    def load_all_routes(self) -> List[Tuple[str, str, int]]:
        results = self.session.query(self.route_table).all()
        routes = []
        for row in results:
            routes.append(
                (
                    row.origin,
                    row.destination,
                    row.travel_time,
                )
            )

        return routes
