"""
A Command line interface for the Falcon service.
"""

import click
import logging

from config import load_config, create_db_engine
from millenium_falcon.loaders.route_loader import RouteLoader
from millenium_falcon.services.falcon_service import FalconService

logger = logging.getLogger(__name__)


@click.command()
@click.argument("falcon_file", type=click.Path(exists=True))
@click.argument("empire_file", type=click.Path(exists=True))
@click.option("--display-trip", is_flag=True, help="Display the trip details")
def compute_probability(falcon_file, empire_file, display_trip):
    # Load the Falcon and Empire data from the JSON files
    falcon_data = load_config(falcon_file)
    empire_data = load_config(empire_file)

    # Create the database engine
    db_engine = create_db_engine(falcon_data)

    # Load the routes from the database
    route_loader = RouteLoader(db_engine)
    routes = route_loader.load_all_routes()

    # Create the FalconService instance
    falcon_service = FalconService(
        all_routes=routes,
        autonomy=falcon_data["autonomy"],
        departure=falcon_data["departure"],
        arrival=falcon_data["arrival"],
    )

    # Compute the probability of success
    countdown = empire_data["countdown"]
    bounty_hunters = [
        (bounty_hunter["planet"], bounty_hunter["day"])
        for bounty_hunter in empire_data["bounty_hunters"]
    ]
    trip, probability = falcon_service.success_probability(countdown, bounty_hunters)

    if display_trip:
        # Print the trip details
        print("Trip details:")
        for time, planet in trip.items():
            print(f" {time}: {planet}")
    # Print the result
    print("Probability to succeed: {probability}%".format(probability=probability))


if __name__ == "__main__":
    compute_probability()
