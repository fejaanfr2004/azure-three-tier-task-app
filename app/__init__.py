import os
from urllib.parse import quote_plus

from flask import Flask
from dotenv import load_dotenv

from .database import db

load_dotenv(".env")


def create_app():
    app = Flask(__name__)

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    odbc_connection = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER=tcp:{server},1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    connection_string = (
        "mssql+pyodbc:///?odbc_connect="
        + quote_plus(odbc_connection)
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
     "pool_pre_ping": True,
     "pool_recycle": 1800
}
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app
