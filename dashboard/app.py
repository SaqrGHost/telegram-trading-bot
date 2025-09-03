"""Placeholder for optional dashboard."""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "Dashboard placeholder"


if __name__ == "__main__":
    app.run(debug=True)
