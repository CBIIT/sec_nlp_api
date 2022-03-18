import sqlite3
from flask import current_app
from typing import Union, Any
from app.db.abstract_database import AbstractDatabase

class SqliteDb(AbstractDatabase):

    def __init__(self) -> None:
        super().__init__()
        self.db = sqlite3.connect(current_app.config["SQLITE_DATABASE_URI"], detect_types=sqlite3.PARSE_DECLTYPES)

    def get(self, query: str) -> Union[Any, None]:
        if query and self.db:
            cursor = self.db.cursor().execute(query)
            return cursor.fetchall()

    def close(self) -> None:
        self.db.close()