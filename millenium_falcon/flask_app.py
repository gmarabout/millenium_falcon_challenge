import os
from flask import Flask

app = Flask(__name__)
db_url = os.environ.get("DATABASE_URL", "sqlite:///universe.db")
secret_key = os.environ.get("SECRET_KEY", "dev")


if __name__ == "__main__":
    app.run(debug=True)
