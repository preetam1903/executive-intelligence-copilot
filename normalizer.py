"""
normalizer.py

Mission 1

Converts Vision JSON into Executive Intelligence Objects (EIO)
"""

from executive_intelligence_model import (
    ExecutiveIntelligenceObject,
    Observation
)


class Normalizer:

    def __init__(self):
        pass

    # --------------------------------------------------------
    # Normalize complete report
    # --------------------------------------------------------

    def normalize_report(self,
                         vision_pages,
                         report_name):

        executive_objects = []

        for page in vision_pages:

            executive_objects.extend(

                self.normalize_page(
                    page,
                    report_name
                )

            )

        return executive_objects

    # --------------------------------------------------------
    # Normalize one page
    # --------------------------------------------------------

    def normalize_page(self,
                       page_json,
                       report_name):

        objects = []

        page_number = page_json.get("page", 0)

        page_objects = page_json.get(
            "executive_objects",
            []
        )

        for obj in page_objects:

            objects.append(

                self.create_executive_object(

                    obj,

                    page_number,

                    report_name

                )

            )

        return objects

    # --------------------------------------------------------
    # Create Executive Object
    # --------------------------------------------------------

    def create_executive_object(self,
                                obj,
                                page_number,
                                report_name):

        eio = ExecutiveIntelligenceObject()

        eio.object_type = obj.get(
            "object_type",
            ""
        )

        eio.title = obj.get(
            "title",
            ""
        )

        eio.unit = obj.get(
            "unit",
            ""
        )

        eio.business_area = obj.get(
            "business_area",
            ""
        )

        eio.page = page_number

        eio.report_name = report_name

        eio.time_period = obj.get(
            "time_period",
            ""
        )

        eio.commentary = obj.get(
            "commentary",
            []
        )

        eio.domain_intelligence = obj.get(
            "domain_intelligence",
            {}
        )

        observations = obj.get(
            "observations",
            []
        )

        for observation in observations:

            if not isinstance(observation, dict):

                print("Skipping invalid observation:", observation)

                continue

            obs = self.create_observation(

                observation,

                report_name,

                page_number

            )

            if obs is not None:

                eio.observations.append(obs)

        return eio

    # --------------------------------------------------------
    # Create Observation
    # --------------------------------------------------------

    def create_observation(self,
                           observation_json,
                           report_name,
                           page_number):

        print("Observation JSON:", observation_json)
        print(type(observation_json))

    # Ignore invalid observations
        if not isinstance(observation_json, dict):

            print("Skipping invalid observation")

            return None

        observation = Observation()

        observation.metric = observation_json.get(
            "metric",
            ""
        )

        observation.period = observation_json.get(
            "period",
            ""
        )

        observation.value = observation_json.get(
            "value",
            ""
        )

        observation.target = observation_json.get(
            "target",
            ""
        )

        observation.source_report = report_name

        observation.source_page = page_number

        observation.confidence = 1.0

        observation.metadata = observation_json

        return observation
