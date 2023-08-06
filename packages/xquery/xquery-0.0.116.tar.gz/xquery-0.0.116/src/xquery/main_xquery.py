import pandas as pd
from xquery.lib.db.db_connections import SqlServerConnection, BqServerConnection, \
    DbState  # DbState has to be imported from db_connections, not from config.py directly as checking for equality would return False
from xquery.lib.query.queries import SqlQuery, BigQuery
from xquery.lib.config import SqlServerConfig, BigQueryConfig
from xquery.lib.utility import get_json


class XQuery:
    """An interface for SQL Server connection and querying. Uses trusted connection by default."""
    def __init__(self):
        self.session = None
        self.db_query_engine = None
        self.db_type = None

    def set_connection_sql_server(self, server_name: str, database_name: str, **kwargs) -> None:
        """Starts Sql Server sql_cnxn"""
        server_config = SqlServerConfig(server_name=server_name, database_name=database_name, **kwargs)
        print(server_config.full_config)
        print(f'CONNECTING TO SQL SERVER. Database_name: {server_name}')
        sql_connection = SqlServerConnection(server_config=server_config)
        sql_connection.create_session()
        if sql_connection.get_connection_state() == DbState.CONNECTED:
            session_id = sql_connection.get_session_id()
            print(f'SUCCESSFULY CONNECTED TO SQL SERVER. Session ID: {session_id}')
            self.db_type = sql_connection.get_db_type()
            self.session = sql_connection
            self.db_query_engine = SqlQuery(self.session.session)
        else:
            print('Issue Connecting')

    def set_connection_big_query(self, bq_secret_filepath: str) -> None:
        """Starts BiqQuery sql_cnxn"""
        bq_secret = get_json(bq_secret_filepath)
        BigQueryConfig.type = bq_secret['type']
        BigQueryConfig.client_email = bq_secret['client_email']
        BigQueryConfig.project_id = bq_secret['project_id']
        print(f'CONNECTING TO BIGQUERY. Account type: {BigQueryConfig.type}, project_id: {BigQueryConfig.project_id}, client_email:{BigQueryConfig.client_email}')
        bq_connection = BqServerConnection(credentials_filepath=bq_secret_filepath)
        bq_connection.create_session()
        if bq_connection.get_connection_state() == DbState.CONNECTED:
            print(f'SUCCESSFULY CONNECTED TO BIGQUERY.')
            self.db_type = bq_connection.get_db_type()
            self.session = bq_connection
            self.db_query_engine = BigQuery(self.session.session)
        else:
            print('Issue Connecting')

    def push_query(self, query_code) -> None:
        if self.db_type is None:
            return None
        print(f'RUNNING QUERY.')
        self.db_query_engine.execute_query(query_code)
        print('FINISHED QUERY')
        return None

    def pull_query(self, query_code) -> pd.DataFrame or None:
        if self.db_type is None:
            return None
        print(f'RUNNING QUERY.')
        df = self.db_query_engine.execute_query_create_df(query_code)
        print('FINISHED QUERY')
        return df


