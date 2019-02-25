#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains class Database that interacts with a database"""

import psycopg2
from psycopg2.extras import RealDictCursor
from .config import Config
from .logger import error_catcher

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__Version__ = "0.1.0"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


class Database:
    """Interact with the database"""

    __slots__ = ['logger', 'config', 'conn', 'cursor', 'test']

    @error_catcher()
    def __init__(self, logger, cursor_factory=RealDictCursor, test=False):
        """Create a new connection with the databse"""

        # Initializes self.logger
        self.logger = logger
        self.config = Config(self.logger)
        self.test = test
        self._connect(cursor_factory)

    @error_catcher()
    def _connect(self, cursor_factory):
        """Connects to db"""

        kwargs = self.config.get_db_creds()
        if cursor_factory:
            kwargs["cursor_factory"] = cursor_factory
        conn = psycopg2.connect(**kwargs)
        self.logger.info("Database Connected")
        self.conn = conn
        self.conn.autocommit = True
        self.cursor = conn.cursor()
        # Creates tables if do not exist
        self._create_tables()

    def _create_tables(self):
        """Method that is overwritten when inherited"""

        pass

    @error_catcher()
    def execute(self, sql, data=None):
        """Executes a query"""

        if data is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, data)
        try:
            return self.cursor.fetchall()
        except psycopg2.ProgrammingError:
            self.logger.warning("No results to fetch")
            return None

    @error_catcher()
    def close(self):
        """Closes the database connection correctly"""

        # If testing delete test table
        if self.test:
            self.db.execute("DROP TABLE IF EXISTS test_bgp_mrt;")
        self.cursor.close()
        self.conn.close()


class ROAs_Table(Database):
    """Announcements table class"""

    __slots__ = []

    @error_catcher()
    def __init__(self, logger, cursor_factory=RealDictCursor, test=False):
        """Initializes the announcement table"""
        Database.__init__(self, logger, cursor_factory, test)

    @error_catcher()
    def _create_tables(self):
        """ Creates tables if they do not exist"""

        if self.test is False:
            sql = """CREATE TABLE IF NOT EXISTS roas (
                  roas_id serial PRIMARY KEY,
                  asn bigint,
                  prefix inet,
                  max_length integer
                  );"""
        else:
            sql = """CREATE TABLE IF NOT EXISTS test_roas (
              test_roas_id serial PRIMARY KEY,
              random_num int
              );"""
        self.cursor.execute(sql)

    @error_catcher()
    def clear_table(self):
        """Clears the tables. Should be called at the start of every run"""

        self.logger.info("Clearing Roas")
        self.cursor.execute("DELETE FROM roas")
        self.logger.info("ROAs Table Cleared")

    @property
    def table(self):
        """Returns the name of the table"""

        return "roas"

    @property
    def columns(self):
        """Returns the columns of the table"""

        return ['asn',
                'prefix',
                'max_length'
                ]
