from flask import Flask, jsonify
from flask_cors import CORS
import os

from .extensions import api, db
from .resources import ns
from .auth import ns as auth_ns

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(auth_ns)

    with app.app_context():
        db.create_all()

    return app