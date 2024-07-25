import json
import logging

from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

with open("millenium-falcon.json") as f:
    logger.debug("Loading millenium-falcon config")
    millenium_falcon_config = json.load(f)

    routes_db = millenium_falcon_config["routes_db"]
    logger.debug(f"Connecting to routes DB: {routes_db}")
    db_engine = create_engine(f"sqlite:///{routes_db}")


def get_millenium_falcon_config():
    return millenium_falcon_config


def get_db_engine():
    return db_engine
