"""
knowledge_repository.py

Mission 1
Executive Intelligence Platform

Repository Manager
SQLite Backend
"""

import sqlite3
import json
import os
from datetime import datetime


class RepositoryManager:

    def __init__(self, db_path="repository/repository.db"):

        self.db_path = db_path

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.connection = sqlite3.connect(db_path)

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

    # ----------------------------------------------------
    # Initialize Database
    # ----------------------------------------------------

    def initialize_database(self):

        self.create_executive_objects_table()

        self.create_observations_table()

        self.create_relationships_table()

        self.create_reports_table()

        self.create_discovery_table()

        self.connection.commit()

    # ----------------------------------------------------
    # Executive Objects
    # ----------------------------------------------------

    def create_executive_objects_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS executive_objects(

            object_id TEXT PRIMARY KEY,

            object_type TEXT,

            title TEXT,

            plant TEXT,

            unit TEXT,

            business_area TEXT,

            report_name TEXT,

            page INTEGER,

            time_period TEXT,

            commentary TEXT,

            insights TEXT,

            evidence TEXT,

            domain_intelligence TEXT,

            metadata TEXT,

            created_on TEXT

        )

        """)

    # ----------------------------------------------------
    # Observations
    # ----------------------------------------------------

    def create_observations_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS observations(

            observation_id TEXT PRIMARY KEY,

            object_id TEXT,

            metric TEXT,

            period TEXT,

            value TEXT,

            target TEXT,

            source_report TEXT,

            source_page INTEGER,

            confidence REAL,

            metadata TEXT

        )

        """)

    # ----------------------------------------------------
    # Relationships
    # ----------------------------------------------------

    def create_relationships_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS relationships(

            relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,

            source TEXT,

            target TEXT,

            relationship_type TEXT,

            confidence REAL,

            evidence TEXT

        )

        """)

    # ----------------------------------------------------
    # Reports
    # ----------------------------------------------------

    def create_reports_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS reports(

            report_name TEXT PRIMARY KEY,

            upload_time TEXT,

            total_pages INTEGER,

            metadata TEXT

        )

        """)

    # ----------------------------------------------------
    # Discovery Queue
    # ----------------------------------------------------

    def create_discovery_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS discovery_queue(

            discovery_id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT,

            object_type TEXT,

            suggested_business_area TEXT,

            report_name TEXT,

            page INTEGER,

            confidence REAL,

            status TEXT

        )

        """)

    # ----------------------------------------------------
    # Report Exists?
    # ----------------------------------------------------

    def report_exists(self, report_name):

        self.cursor.execute(

            "SELECT report_name FROM reports WHERE report_name=?",

            (report_name,)

        )

        return self.cursor.fetchone() is not None

    # ----------------------------------------------------
    # Save Report
    # ----------------------------------------------------

    def save_report(self,
                    report_name,
                    total_pages,
                    metadata=None):

        if metadata is None:

            metadata = {}

        if self.report_exists(report_name):

            return

        self.cursor.execute("""

        INSERT INTO reports

        VALUES(?,?,?,?)

        """,

        (

            report_name,

            datetime.now().isoformat(),

            total_pages,

            json.dumps(metadata)

        )

        )

        self.connection.commit()

    # ----------------------------------------------------
    # Object Exists?
    # ----------------------------------------------------

    def object_exists(self,
                      object_id):

        self.cursor.execute(

            "SELECT object_id FROM executive_objects WHERE object_id=?",

            (object_id,)

        )

        return self.cursor.fetchone() is not None

    # ----------------------------------------------------
    # Close
    # ----------------------------------------------------

    def close(self):

        self.connection.commit()

        self.connection.close()
