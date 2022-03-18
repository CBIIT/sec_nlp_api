from abc import ABC, abstractmethod
from typing import Any, Union

class AbstractDatabase(ABC):

    @abstractmethod
    def get(self, query: str) -> Union[Any, None]:
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()