"""
blink/config.py
Ian Kollipara
2022.03.31

Blink Config
"""

# Imports
from dataclasses import dataclass
from typing import List, Literal, Tuple, TypedDict

from .middleware import TulparMiddleware


class SQLiteParams(TypedDict):
    """SQLiteParams denotes the parameters
    needed for an SQLite PonyORM DB Connection.
    """

    filename: str
    create_db: bool


class PostgresParams(TypedDict):
    """PostgresParams denotes the parameters
    needed for an Postgres PonyORM DB Connection.
    """

    user: str
    password: str
    host: str
    database: str


class MySQLParams(TypedDict):
    """MySQLParams denotes the parameters
    needed for an MySQL PonyORM DB Connection.
    """

    user: str
    passwd: str
    host: str
    database: str


class OracleParams(TypedDict):
    """OracleParams denotes the parameters
    needed for an Oracle PonyORM DB Connection.
    """

    user: str
    password: str
    dsn: str


class CockroachParams(TypedDict):
    """CockroachParams denotes the parameters
    needed for an Cockroach PonyORM DB Connection.
    """

    user: str
    passwd: str
    host: str
    database: str
    sslmode: Literal["disable"]


DB_PARAMS = (
    Tuple[Literal["sqlite"], SQLiteParams]
    | Tuple[Literal["postgres"], PostgresParams]
    | Tuple[Literal["mysql"], MySQLParams]
    | Tuple[Literal["oracle"], OracleParams]
    | Tuple[Literal["cockroach"], CockroachParams]
)


@dataclass
class TulparConfig:
    """BlinkConfig is the base class for all configuration files
    `config.py` *must* inherit from this class.
    """

    app_name: str
    db_params: DB_PARAMS
    middleware: List[TulparMiddleware]
