from abc import ABC, abstractmethod
from typing import Any, Union

class AbstractDatabase(ABC):

    @abstractmethod
    def get(self, query: str) -> Union[Any, None]:
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def safe_sql(self, query: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def cursor(self) -> Any:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()