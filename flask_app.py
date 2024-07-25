import os
from typing import List

from flask import Flask, render_template
from flask_pydantic import validate
from pydantic import BaseModel

from config import get_db_engine, get_millenium_falcon_config
from millenium_falcon.loaders.route_loader import RouteLoader
from millenium_falcon.services.falcon_service import FalconService

app = Flask(__name__)
db_url = os.environ.get("DATABASE_URL", "sqlite:///universe.db")


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
    config = get_millenium_falcon_config()
    db_engine = get_db_engine()

    autonomy = config["autonomy"]
    departure = config["departure"]
    arrival = config["arrival"]

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
    app.run(debug=True, port=5000)
