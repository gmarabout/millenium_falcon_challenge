import os
from typing import List

from flask import Flask, render_template
from flask_pydantic import validate
from pydantic import BaseModel

from config import get_db_engine, get_millenium_falcon_config
from millenium_falcon.adapters.repository import SQLAlchemyRouteRepository
from millenium_falcon.services.falcon_service import FalconService

app = Flask(__name__)
db_url = os.environ.get("DATABASE_URL", "sqlite:///universe.db")
secret_key = os.environ.get("SECRET_KEY", "dev")


class BountyHunterSchema(BaseModel):
    planet: str
    day: int


class EmpireSchema(BaseModel):
    countdown: int
    bounty_hunters: List[BountyHunterSchema]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/falcon/success", methods=["POST", "PUT"])
@validate()
def get_falcon_success(body: EmpireSchema):
    config = get_millenium_falcon_config()
    db_engine = get_db_engine()

    autonomy = config["autonomy"]
    departure = config["departure"]
    arrival = config["arrival"]

    routes = SQLAlchemyRouteRepository(db_engine).get_all()
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
    app.run(debug=True)
