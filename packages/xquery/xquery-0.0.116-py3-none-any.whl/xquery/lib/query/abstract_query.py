from abc import ABC, abstractmethod
import pandas as pd


class Query(ABC):
    @abstractmethod
    def execute_query(self, query_code: str) -> None:
        pass

    @abstractmethod
    def execute_query_create_df(self, query_code: str) -> pd.DataFrame or None:
        pass

    def validate_query(self, query_code: str):
        pass
