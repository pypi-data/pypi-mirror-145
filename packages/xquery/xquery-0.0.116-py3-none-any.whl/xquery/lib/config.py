from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
from xquery.lib.utility import build_config_str_from_params


BQ_CLIENT_SECRET_FILE = 'C:/credentials/bq_credentials.json'


@dataclass(frozen=True)  # blocks ability to change class after setup
class SqlServerConfig:
    """Stores Sql Server configuration details."""
    server_name: str
    database_name: str
    driver: str = '{ODBC Driver 17 for SQL Server}'
    is_trusted_connection: str = 'yes'
    UID: Optional[str] = None
    PWD: Optional[str] = None
    full_config: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'full_config', build_config_str_from_params(server_name=self.server_name,
                                                                             database_name=self.database_name,
                                                                             driver=self.driver,
                                                                             trusted_connection=self.is_trusted_connection,
                                                                             # name trusted_connection used on purpose instead of is_trusted_connection. pyodbc requires trusted_connection as param name, however I want more descriptive name in dataclass.
                                                                             UID=self.UID,
                                                                             PWD=self.PWD
                                                                             )
                           )  # this way it's possible to overwrite parameter despite frozen=True


@dataclass(frozen=True)
class BigQueryConfig:
    """Stores BigQuery configuration details."""
    type: str
    project_id: str
    client_email: str


class DbState(Enum):
    """Contains possible states for Sql Server connection"""
    CONNECTING = auto()
    CONNECTED = auto()
    ERROR = auto()
    DISCONNECTED = auto()


class DbType(Enum):
    """Contains possible states for Sql Server connection"""
    SQL_SERVER = auto()
    BIGQUERY = auto()
