import os
from typing import List

from flask import Flask, render_template
from flask_pydantic import validate
from pydantic import BaseModel

from config import load_config, create_db_engine
from millenium_falcon.route_loader import RouteLoader
from millenium_falcon.falcon_service import FalconService

FALCON_CONFIG_FILE = os.environ.get("FALCON_CONFIG_FILE", "millenium-falcon.json")

app = Flask(__name__)

falcon_config = load_config(FALCON_CONFIG_FILE)
db_engine = create_db_engine(falcon_config)


class BountyHunterSchema(BaseModel):
    planet: str
    day: int


class EmpireSchema(BaseModel):
    countdown: int
    bounty_hunters: List[BountyHunterSchema]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/falcon/success_probability", methods=["POST", "PUT"])
@validate()
def get_falcon_success_probability(body: EmpireSchema):

    autonomy = falcon_config["autonomy"]
    departure = falcon_config["departure"]
    arrival = falcon_config["arrival"]

    routes = RouteLoader(db_engine).load_all_routes()
    service = FalconService(autonomy, departure, arrival, routes)

    bounty_hunters = [
        (bounty_hunter.planet, bounty_hunter.day)
        for bounty_hunter in body.bounty_hunters
    ]
    trip, score = service.success_probability(
        countdown=body.countdown,
        bounty_hunters=bounty_hunters,
    )
    return {"trip": trip, "score": score}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
