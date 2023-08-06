from xquery.lib.query.abstract_query import Query
import pyodbc
import pandas as pd
from google.cloud import bigquery


class SqlQuery(Query):
    def __init__(self, session: pyodbc.Connection):
        self.session = session

    def execute_query(self, query_code: str) -> None:
        self.session.execute(query_code)
        self.session.commit()

    def execute_query_create_df(self, query_code: str) -> pd.DataFrame:
        df = pd.read_sql(query_code, self.session)
        self.session.commit()
        return df


class BigQuery(Query):
    def __init__(self, session: bigquery.client.Client):
        self.session = session

    def execute_query(self, query_code: str) -> None:
        pass

    def execute_query_create_df(self, query_code: str) -> pd.DataFrame:
        query_results = self.session.query(query_code)
        df = query_results.to_dataframe()
        return df

