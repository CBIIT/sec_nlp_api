from psycopg2 import connect
from typing import Union, Any
from app.databases.abstract_database import AbstractDatabase


class PostgresDb(AbstractDatabase):

    def __init__(self, connection: connect) -> None:
        super().__init__()
        self.db = connection

    def cursor(self):
        return self.db.cursor()

    def get(self, query: str) -> Union[Any, None]:
        with self.db.cursor() as cursor:
            cursor.execute(self.safe_sql(query))
            return cursor.fetchall()

    def save(self, query: str, data: tuple) -> None:
        curr = self.db.cursor()
        curr.execute(query, data)
        self.db.commit()

    def safe_sql(self, query: str) -> Union[str, None]:
        if query:
            query = query.replace('?', '%s')
        return query

    def close(self):
        self.db.close()
