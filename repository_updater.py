"""
repository_updater.py

Mission 1

Responsible for

1. Detect duplicate knowledge
2. Insert new Executive Objects
3. Insert Observations
4. Update Discovery Queue
"""

import json
from datetime import datetime

from executive_intelligence_model import ExecutiveIntelligenceObject


class RepositoryUpdater:

    def __init__(self, repository):

        self.repository = repository

    # ---------------------------------------------------
    # BUSINESS KEY
    # ---------------------------------------------------

    def create_business_key(self, executive_object):

        business_area = str(
            executive_object.business_area or ""
        ).strip().lower()

        unit = str(
            executive_object.unit or ""
        ).strip().lower()

        title = str(
        executive_object.title or ""
        ).strip().lower()

        object_type = str(
            executive_object.object_type or ""
        ).strip().lower()

        return "|".join([

            business_area,

            unit,

            title,

            object_type

        ])

    # ---------------------------------------------------
    # CHECK DUPLICATE OBJECT
    # ---------------------------------------------------

    def object_exists(self, executive_object):

        business_key = self.create_business_key(executive_object)

        self.repository.cursor.execute("""

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

            executive_object.object_type.lower(),

            executive_object.title.lower(),

            executive_object.plant.lower(),

            executive_object.unit.lower(),

            executive_object.business_area.lower(),

            executive_object.time_period.lower()

        )

        )

        row = self.repository.cursor.fetchone()

        if row:

            return True, row["object_id"]

        return False, None

    # ---------------------------------------------------
    # SAVE EXECUTIVE OBJECT
    # ---------------------------------------------------

    def save_executive_object(self, executive_object):

        exists, object_id = self.object_exists(executive_object)

        if exists:

            return object_id

        self.repository.cursor.execute("""

        INSERT INTO executive_objects

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

            executive_object.object_id,

            executive_object.object_type,

            executive_object.title,

            executive_object.plant,

            executive_object.unit,

            executive_object.business_area,

            executive_object.report_name,

            executive_object.page,

            executive_object.time_period,

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

    # ---------------------------------------------------
    # SAVE OBSERVATIONS
    # ---------------------------------------------------

    def save_observations(self,
                          object_id,
                          observations):

        for observation in observations:

            self.repository.cursor.execute("""

            SELECT observation_id

            FROM observations

            WHERE metric=?

            AND period=?

            AND value=?

            AND source_report=?

            """,

            (

                observation.metric,

                observation.period,

                str(observation.value),

                observation.source_report

            )

            )

            row = self.repository.cursor.fetchone()

            if row:

                continue

            self.repository.cursor.execute("""

            INSERT INTO observations

            VALUES(?,?,?,?,?,?,?,?,?,?)

            """,

            (

                observation.observation_id,

                object_id,

                observation.metric,

                observation.period,

                str(observation.value),

                str(observation.target),

                observation.source_report,

                observation.source_page,

                observation.confidence,

                json.dumps(observation.metadata)

            )

            )

        self.repository.connection.commit()

    # ---------------------------------------------------
    # SAVE DISCOVERY
    # ---------------------------------------------------

    def save_discovery(self,
                       title,
                       object_type,
                       business_area,
                       report_name,
                       page,
                       confidence):

        self.repository.cursor.execute("""

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

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            title,

            object_type,

            business_area,

            report_name,

            page,

            confidence,

            "Pending"

        )

        )

        self.repository.connection.commit()

    # ---------------------------------------------------
    # MAIN ENTRY
    # ---------------------------------------------------

    def process_object(self,
                       executive_object):

        object_id = self.save_executive_object(

            executive_object

        )

        self.save_observations(

            object_id,

            executive_object.observations

        )

        return object_id
