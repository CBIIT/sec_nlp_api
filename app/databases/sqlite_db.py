from pathlib import Path
import sqlite3
from flask import current_app
from typing import Union, Any
from app.databases.abstract_database import AbstractDatabase

class SqliteDb:

    def __init__(self, path: Path = None) -> None:
        super().__init__()
        self.path = path
        if path is None:
            self.path = current_app.config["SQLITE_DATABASE_URI"]
        self.db = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES)

    def cursor(self) -> sqlite3.Cursor:
        return self.db.cursor()

    def get(self, query: str) -> Union[Any, None]:
        # curr = self.db.cursor()
        # curr.execute(query)
        # return curr.fetchall()
        with self as db:
            db.cursor.execute(query)
            return db.cursor.fetchall()

    def __enter__(self):
        self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        return self

    def safe_sql(self, query: str) -> str:
        return query

    def close(self) -> None:
        self.db.close()