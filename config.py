import json
import logging

from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


def load_config(json_config_file):
    """Load a JSON configuration file, and return the parsed content as a dict."""
    with open(json_config_file) as f:
        logger.info("Loading configuration from %s", json_config_file)
        return json.load(f)


def create_db_engine(config):
    """Create a SQLAlchemy database engine from a configuration dict."""
    routes_db = config.get("routes_db")
    if not routes_db:
        raise ValueError("Missing routes_db in config")
    logger.info("Creating database engine for %s", routes_db)
    db_engine = create_engine(f"sqlite:///{routes_db}")
    return db_engine
