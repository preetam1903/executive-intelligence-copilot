"""
repository_updater.py

Mission 1
Version 2

Repository Intelligence Layer

Responsibilities

1. Insert Executive Objects
2. Detect duplicates
3. Insert Observations
4. Maintain Report History
5. Maintain Discovery Queue
6. Update Existing Knowledge
"""

import json
from datetime import datetime


class RepositoryUpdater:

    # ----------------------------------------------------
    # Constructor
    # ----------------------------------------------------

    def __init__(self, repository):

        self.repository = repository

    # ----------------------------------------------------
    # Safe String
    # ----------------------------------------------------

    def safe_string(self, value):

        if value is None:
            return ""

        if isinstance(value, dict):
            return json.dumps(value)

        if isinstance(value, list):
            return json.dumps(value)

        return str(value).strip()

    # ----------------------------------------------------
    # Safe Lower
    # ----------------------------------------------------

    def safe_lower(self, value):

        return self.safe_string(value).lower()

    # ----------------------------------------------------
    # Business Key
    # ----------------------------------------------------

    def create_business_key(
            self,
            executive_object):

        fields = [

            executive_object.object_type,

            executive_object.title,

            executive_object.plant,

            executive_object.unit,

            executive_object.business_area,

            executive_object.time_period

        ]

        return "|".join(

            self.safe_lower(f)

            for f in fields

        )

    # ----------------------------------------------------
    # Check Duplicate Executive Object
    # ----------------------------------------------------

    def executive_object_exists(
            self,
            executive_object):

        self.repository.cursor.execute(

            """
            SELECT object_id

            FROM executive_objects

            WHERE lower(object_type)=?

            AND lower(title)=?
            AND lower(plant)=?
            AND lower(unit)=?
            AND lower(business_area)=?
            AND lower(time_period)=?
            """,

            (

                self.safe_lower(
                    executive_object.object_type
                ),

                self.safe_lower(
                    executive_object.title
                ),

                self.safe_lower(
                    executive_object.plant
                ),

                self.safe_lower(
                    executive_object.unit
                ),

                self.safe_lower(
                    executive_object.business_area
                ),

                self.safe_lower(
                    executive_object.time_period
                )

            )

        )

        row = self.repository.cursor.fetchone()

        if row:

            return True, row["object_id"]

        return False, None

        # ----------------------------------------------------
    # Save Executive Object
    # ----------------------------------------------------
    def save_executive_object(
            self,
            executive_object):

        exists, object_id = self.executive_object_exists(
            executive_object
        )

        if exists:

            self.update_existing_object(
                object_id,
                executive_object
            )

            return object_id

        try:

            self.repository.cursor.execute(

                """
                INSERT INTO executive_objects
                (
                    object_id,
                    object_type,
                    title,
                    plant,
                    unit,
                    business_area,
                    report_name,
                    page,
                    time_period,
                    commentary,
                    insights,
                    evidence,
                    domain_intelligence,
                    metadata,
                    created_date
                )

                VALUES
                (
                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                )
                """,

                (

                    executive_object.object_id,

                    self.safe_string(executive_object.object_type),

                    self.safe_string(executive_object.title),

                    self.safe_string(executive_object.plant),

                    self.safe_string(executive_object.unit),

                    self.safe_string(executive_object.business_area),

                    self.safe_string(executive_object.report_name),

                    executive_object.page,

                    self.safe_string(executive_object.time_period),

                    json.dumps(executive_object.commentary),

                    json.dumps(executive_object.insights),

                    json.dumps(executive_object.evidence),

                    json.dumps(executive_object.domain_intelligence),

                    json.dumps(executive_object.metadata),

                    datetime.now().isoformat()

                )

            )

            self.repository.connection.commit()

            return executive_object.object_id

        except Exception as ex:

            print("=" * 80)
            print("SAVE EXECUTIVE OBJECT ERROR")
            print(type(ex))
            print(ex)
            print("=" * 80)

            raise

    # ----------------------------------------------------
    # Update Existing Executive Object
    # ----------------------------------------------------

    def update_existing_object(
            self,
            object_id,
            executive_object):

        self.repository.cursor.execute(

            """
            UPDATE executive_objects

            SET

                report_name=?,

                page=?,

                commentary=?,

                insights=?,

                evidence=?,

                domain_intelligence=?,

                metadata=?

            WHERE object_id=?

            """,

            (

                self.safe_string(
                    executive_object.report_name
                ),

                executive_object.page,

                json.dumps(
                    executive_object.commentary
                ),

                json.dumps(
                    executive_object.insights
                ),

                json.dumps(
                    executive_object.evidence
                ),

                json.dumps(
                    executive_object.domain_intelligence
                ),

                json.dumps(
                    executive_object.metadata
                ),

                object_id

            )

        )

        self.repository.connection.commit()

        return object_id
        # ----------------------------------------------------
    # Observation Exists
    # ----------------------------------------------------

    def observation_exists(
            self,
            observation):

        self.repository.cursor.execute(

            """
            SELECT observation_id

            FROM observations

            WHERE

                metric=?

            AND period=?
            AND value=?
            AND source_report=?

            """,

            (

                self.safe_string(
                    observation.metric
                ),

                self.safe_string(
                    observation.period
                ),

                self.safe_string(
                    observation.value
                ),

                self.safe_string(
                    observation.source_report
                )

            )

        )

        row = self.repository.cursor.fetchone()

        if row:

            return True

        return False

    # ----------------------------------------------------
    # Save Observations
    # ----------------------------------------------------

    def save_observations(
            self,
            object_id,
            observations):

        inserted = 0

        skipped = 0

        for observation in observations:

            if self.observation_exists(
                    observation):

                skipped += 1

                continue

            self.repository.cursor.execute(

                """
                INSERT INTO observations
                (
                    observation_id,
                    object_id,
                    metric,
                    period,
                    value,
                    target,
                    source_report,
                    source_page,
                    confidence,
                    metadata
                )

                VALUES
                (
                    ?,?,?,?,?,?,?,?,?,?
                )
                """,

                (

                    observation.observation_id,

                    object_id,

                    self.safe_string(
                        observation.metric
                    ),

                    self.safe_string(
                        observation.period
                    ),

                    self.safe_string(
                        observation.value
                    ),

                    self.safe_string(
                        observation.target
                    ),

                    self.safe_string(
                        observation.source_report
                    ),

                    observation.source_page,

                    observation.confidence,

                    json.dumps(
                        observation.metadata
                    )

                )

            )

            inserted += 1

        self.repository.connection.commit()

        return {

            "inserted": inserted,

            "duplicates": skipped

        }

    # ----------------------------------------------------
    # Save Report History
    # ----------------------------------------------------

    def save_report_history(
            self,
            report_name):

        try:

            self.repository.cursor.execute(

                """
                INSERT INTO report_history
                (
                    report_name,
                    loaded_date
                )

                VALUES
                (
                    ?,?
                )
                """,

                (

                    report_name,

                    datetime.now().isoformat()

                )

            )

            self.repository.connection.commit()

        except Exception:

            pass

        # ----------------------------------------------------
    # Discovery Queue
    # ----------------------------------------------------
        # ----------------------------------------------------
    # Discovery Queue
    # ----------------------------------------------------

    def save_discovery(
            self,
            executive_object):

        try:

            title = self.safe_string(
                executive_object.title
            )

            if title == "":
                return

            self.repository.cursor.execute(

                """
                SELECT discovery_id

                FROM discovery_queue

                WHERE lower(title)=?

                """,

                (

                    self.safe_lower(title),

                )

            )

            row = self.repository.cursor.fetchone()

            if row:
                return

            self.repository.cursor.execute(

                """
                INSERT INTO discovery_queue
                (

                    title,

                    object_type,

                    suggested_business_area,

                    report_name,

                    page,

                    confidence,

                    status

                )

                VALUES
                (
                    ?,?,?,?,?,?,?
                )

                """,

                (

                    self.safe_string(
                        executive_object.title
                    ),

                    self.safe_string(
                        executive_object.object_type
                    ),

                    self.safe_string(
                        executive_object.business_area
                    ),

                    self.safe_string(
                        executive_object.report_name
                    ),

                    executive_object.page,

                    1.0,

                    "Pending"

                )

            )

            self.repository.connection.commit()

        except Exception as ex:

            print("=" * 80)
            print("SAVE DISCOVERY ERROR")
            print(type(ex))
            print(ex)
            print("=" * 80)

            raise
    
            

    # ----------------------------------------------------
    # Repository Statistics
    # ----------------------------------------------------

        # ----------------------------------------------------
    # Repository Statistics
    # ----------------------------------------------------

    def repository_statistics(self):

        stats = {}

        tables = [

            "executive_objects",

            "observations",

            "relationships",

            "discovery_queue",

            "reports"

        ]

        for table in tables:

            try:

                self.repository.cursor.execute(

                    f"SELECT COUNT(*) AS cnt FROM {table}"

                )

                row = self.repository.cursor.fetchone()

                if row:

                    stats[table] = row["cnt"]

                else:

                    stats[table] = 0

            except Exception as ex:

                print(f"Repository Statistics Error ({table}) : {ex}")

                stats[table] = 0

        return stats

    # ----------------------------------------------------
    # Process Executive Object
    # ----------------------------------------------------

    def process_object(
            self,
            executive_object):

        object_id = self.save_executive_object(

            executive_object

        )

        observation_result = self.save_observations(

            object_id,

            executive_object.observations

        )

        self.save_discovery(

            executive_object

        )

        self.save_report_history(

            executive_object.report_name

        )

        return {

            "object_id": object_id,

            "observations": observation_result

        }

    # ----------------------------------------------------
    # Process Complete Report
    # ----------------------------------------------------

    def process_report(
            self,
            executive_objects):

        summary = {

            "objects_processed": 0,

            "observations_inserted": 0,

            "duplicates": 0

        }

        for obj in executive_objects:

            result = self.process_object(

                obj

            )

            summary["objects_processed"] += 1

            summary["observations_inserted"] += result[
                "observations"
            ]["inserted"]

            summary["duplicates"] += result[
                "observations"
            ]["duplicates"]

        summary["repository"] = self.repository_statistics()

        return summary
