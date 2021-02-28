from sqlalchemy.engine import create_engine, Engine
from sqlalchemy import Table, Column, MetaData
from sqlalchemy.types import BigInteger, DateTime, Integer, Text

from meldebot.mel.conf import get_psql_connection, using_database


class Database:
    def __init__(self) -> None:
        """
        Initialize the local variables according to the conf
        """
        if using_database() is True:
            self.using_database = True
        else:
            self.using_database = False

        # Init engine and tables as None for lazy-load
        self._engine = None
        self._motos_counter_table = None

    def __del__(self) -> None:
        """
        When this object is destroy we also want to close the connection engine
        """

        if self._engine:
            del self._engine

    @property
    def engine(self) -> Engine:
        """Return the database engine with the psql connection from the confs.

        The engine will be created if it hasn't been created yet
        and will be cached.

        Returns:
            Engine: Engine connection to the psql database
        """
        if self._engine is not None:
            return self._engine

        if self.using_database is True:
            self._engine = create_engine(get_psql_connection())
            return self._engine

        return None

    @property
    def motos_counter(self) -> Table:
        """
        Get the `motos_counter` table definition.

        Returns:
            Table: `motos_counter` table definition
        """

        if self._motos_counter_table is None:
            self._build_motos_counter_table()

        return self._motos_counter_table

    def _build_motos_counter_table(self, init: bool = False) -> None:
        """
        Create the Table with the connection metadata
        """

        metadata = MetaData(self.engine)
        self._motos_counter_table = Table(
            "motos_counter",
            metadata,
            Column("id", BigInteger, primary_key=True, index=True),
            Column("poll_id", Integer, index=True, nullable=False),
            Column("user_id", Integer, index=True, nullable=False),
            Column("vote", Integer, index=True, nullable=False),
            Column("date", DateTime, index=True, nullable=False),
        )

        if init is True:
            metadata.create_all()

    def init_database(self) -> None:
        """
        Create all the database Tables

        Warning: This method does not update existing tables
        """

        if self.using_database is False:
            raise Exception(
                "Trying to initialize the database without database connection"
            )

        self._build_motos_counter_table(init=True)
