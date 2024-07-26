# Millenium Falcon Challenge

This project is a solution for the Dataiku [Millenium Falcon Challenge](https://github.com/dataiku/millenium-falcon-challenge).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Source Code Organization](#source-code-organization)
- [How it works](#how-it-works)

## Requirements

You need Python >3.12 installed and Poetry >1.8 for dependencies.

## Installation

To install the depencencies, enter:

```shell
poetry install
```

## Usage

### Run the tests

Tests are written using Pytest.
To run all tests:

```shell
poetry run pytest
```

### The Web app

The web app is a Flask app with a single page.
To run the app, enter in the terminal:

```shell
poetry run python flask_app.py
```

Then you can open your Web browser to [http://localhost:5000](http://localhost:5000). This will show a simple web page asking to select a JSON file describing the plans of the Empire.
This file must be a valid JSON and have the following structure:

```json
{
  "countdown": 6,
  "bounty_hunters": [
    { "planet": "Tatooine", "day": 4 },
    { "planet": "Dagobah", "day": 5 }
  ]
}
```

If not, you will get a complain from R2D2.
Once selected, press "Upload and Send" and see the odds of seeing a good ending for Star Wars.

#### Using Docker and Docker Compose

You can also run the Web app using Docker compose, which can be convenient if you don't want to install Python and Poetry:

```bash
$ docker compose up -d
```

### The Command Line Interface (CLI)

The CLI is made in Python with Click and available via the file `cli.py`.
To run it, enter in your terminal:

```bash
$ poetry shell
$ python cli.py <path to the falcon configuration file> <path to the Empire plans file>
```

Example:

```bash
$ python cli.py millenium-falcon.json data/empire2.json
Probability to succeed: 81%
```

You can use the `--display-trip` option to display the safest trip to Endor, if any.

```bash
$ python cli.py millenium-falcon.json data/empire2.json --display-trip
Trip details:
 0: Tatooine
 6: Hoth
 7: Hoth
 8: Endor
Probability to succeed: 81%
```

## Source Code Organization

The source code organization of the project follows a typical Python project structure.
Here is a brief overview:

- `flask_app.py`: The main file for running the web app using Flask. This module also declares the HTTP endpoints.
- `cli.py`: The main file for running the command line interface (CLI) using Click.
- `config.py`: Contains configuration helpers for the project.
- `millenium_falcon` : Contains the backend modules
  - `domain.py`: Contains the domain classes and structures (mainly route and trip)
  - `route_loader.py`: Contains route loaders, relies on SQLAlchemy.
  - `falcon_services.py`: Contains business logic for the Falcon-related services.
  - `routing.py`: Contains the code for finding trip accross planets.
  - `scoring.py`: Contains the code to score trips (basically compute the odds of not being caughts by Bounty Hunters)
- `tests`: Contains tests (unit, acceptance).
- `templates`: Contains Flask template. This app contains only one page and one template.
- `data`: Contains some "Empire plans" you can use for testing.

## How it works

The app mechanism is very simple: Given the Falcon and Empire config, we first use the `routing` algorithm to find all possible trips from "departure" to "destination".
This is implemented using a depth first tree search.
The noticable points about this algorithm are:

- The search will not revisit already visited locations. This is a implementation choice to reduce the complexity of the tree search. However, going back to already visited could have been a good strategy to avoid bounty hunters (as soon as we arrive in time to save Endor).
- The search will evaluate the possibility to stay on a planet a day or more (but no more than the remaining time until Endor destruction). This offers the possibility to find a trip that is safer (avoiding bounty hunters), and gives refuling opportunities (at cost of extra complexity).
- The `millenium_falcon/routing.py` module also provide some _checkers_ used in unit test to verify found trips respect the autonomy, deadline, and distances contraints.

See [routing.py](millenium_falcon/routing.py) for more details about the routing implementation.

Once we found at least one trip, respecting all the constraints, we pass each of them to the `scoring` module to determine the probability of not being caught.
We keep the best trip and its score. These are the response sent to the web page (even if the web page displays only the score, as requested).

See [scoring.py](millenium_falcon/scoring.py) for more details about the implementation.

## Possible Improvements

- Evaluate a routing algorithm that would use Empire plans to explicitely and more intelligently avoid bounty hunters.
- Evaluate a routing algorithm that would prefer revisiting a planet to avoid bounty hunters (as soon as it respect the deadline).
