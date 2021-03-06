import sqlite3
import click

from flask import (current_app, g)
from flask.cli import with_appcontext
from psycopg2 import connect
from app.databases.postgres_db import PostgresDb

def get_db():
    if "db" not in g:
        g.db = PostgresDb(connection=
            connect(
                host=current_app.config["POSTGRESQL_HOST"],
                port=current_app.config["POSTGRESQL_PORT"],
                database=current_app.config["POSTGRESQL_DATABASE_NAME"],
                user=current_app.config['POSTGRESQL_USERNAME'],
                password=current_app.config["POSTGRESQL_PASSWORD"]
            )   
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
    
def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)