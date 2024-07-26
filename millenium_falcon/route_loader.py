from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .domain import Route


class RouteLoader:
    def __init__(self, engine):
        self.route_table = Table(
            "routes",
            MetaData(),
            autoload_with=engine,
        )
        self.session = sessionmaker(bind=engine)()

    def load_all_routes(self) -> List[Route]:
        results = self.session.query(self.route_table).all()
        routes = []
        for row in results:
            routes.append(
                Route(
                    row.origin,
                    row.destination,
                    row.travel_time,
                )
            )
            # Routes are bidirectional
            routes.append(
                Route(
                    row.destination,
                    row.origin,
                    row.travel_time,
                )
            )
        return routes
