from abc import ABC, abstractmethod
from xquery.lib.config import DbState
import pyodbc


class DatabaseServerConnection(ABC):
    @abstractmethod
    def create_session(self) -> pyodbc.Connection or None:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass

    @abstractmethod
    def get_connection_state(self) -> str:
        pass

    @abstractmethod
    def set_connection_state(self, state: DbState) -> None:
        pass

    @abstractmethod
    def get_db_type(self) -> str:
        pass
