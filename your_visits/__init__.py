import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    load_dotenv()

    # DB
    # in-memory. see https://docs.sqlalchemy.org/en/14/core/engines.html
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    # uncomment below for saving to a file
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{os.path.join(BASE_DIR, 'dev.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    from .models import db

    db.init_app(app)

    # Views:
    from .routes import bp

    app.register_blueprint(bp)

    return app
