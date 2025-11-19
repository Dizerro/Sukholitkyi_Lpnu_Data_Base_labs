import os, yaml
from flask import Flask
from .utils.db import db, ma
from .route import register_blueprints

def _load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "config", "app.yml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def create_app():
    cfg = _load_config()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg["database"]["url"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = cfg["flask"]["secret_key"]

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        # Таблиці створювати НЕ потрібно, бо ти вже робиш це своїм SQL.
        # Але ORM потрібна для моделей/зв'язків.
        register_blueprints(app)
    return app