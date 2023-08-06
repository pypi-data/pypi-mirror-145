import pyodbc
from xquery.lib.config import SqlServerConfig, DbState, DbType
from xquery.lib.db.abstract_db_connection import DatabaseServerConnection
from google.cloud import bigquery


class SqlServerConnection(DatabaseServerConnection):
    """Creates SQL Server connection."""
    def __init__(self, server_config: SqlServerConfig):
        self.server_config = server_config
        self.connection_state = DbState.DISCONNECTED
        self.db_type = DbType.SQL_SERVER
        self.session = None

    def create_session(self) -> pyodbc.Connection:
        """Creates SQL Server sql_cnxn based on instance parameters."""
        self.set_connection_state(DbState.CONNECTING)
        self.session = pyodbc.connect(self.server_config.full_config)
        self.set_connection_state(DbState.CONNECTED)
        return self.session

    def close_connection(self):
        if self.connection_state == DbState.CONNECTED:
            self.session.close()
            self.set_connection_state(DbState.DISCONNECTED)
            self.session = None
            print(f'CLOSED SQL SERVER SESSION.')
        else:
            print('NO ACTIVE SESSION TO BE CLOSED.')

    def get_connection_state(self):
        return self.connection_state

    def set_connection_state(self, state: DbState):
        self.connection_state = state

    def get_db_type(self):
        return self.db_type

    def get_session_id(self) -> int or None:
        """Retrieves SQL sql_cnxn id from current sql_cnxn."""
        if self.connection_state == DbState.CONNECTED:
            cursor = self.session
            session_id = cursor.execute('SELECT @@SPID AS session_id').fetchone()[0]
            return session_id
        else:
            return None


class BqServerConnection(DatabaseServerConnection):
    def __init__(self, credentials_filepath: str):
        self.server_config = credentials_filepath
        self.connection_state = DbState.DISCONNECTED
        self.db_type = DbType.BIGQUERY
        self.session = None

    def create_session(self) -> bigquery.client.Client:
        self.set_connection_state(DbState.CONNECTING)
        self.session = bigquery.Client.from_service_account_json(self.server_config)
        self.set_connection_state(DbState.CONNECTED)
        return self.session

    def close_connection(self):
        if self.connection_state == DbState.CONNECTED:
            self.session.close()
            self.set_connection_state(DbState.DISCONNECTED)
            print(f'CLOSED BQ SERVER SESSION.')
            self.session = None
        else:
            print('NO ACTIVE SESSION TO BE CLOSED.')

    def get_connection_state(self):
        return self.connection_state

    def set_connection_state(self, state: DbState):
        self.connection_state = state

    def get_db_type(self):
        return self.db_type
