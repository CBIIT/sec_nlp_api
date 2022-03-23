import psycopg2
from flask import current_app
from typing import Union, Any
from app.databases.abstract_database import AbstractDatabase


class PostgresDb(AbstractDatabase):

    def __init__(self) -> None:
        super().__init__()
        self.db = psycopg2.connect(
            host=current_app.config["POSTGRESQL_HOST"],
            port=current_app.config["POSTGRESQL_PORT"],
            database=current_app.config["POSTGRESQL_DATABASE_NAME"],
            user=current_app.config['POSTGRESQL_USERNAME'],
            password=current_app.config["POSTGRESQL_PASSWORD"]
        )

    def get(self, query: str) -> Union[Any, None]:
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        self.db.close()
