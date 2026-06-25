"""
executive_agent.py

Mission 1
Version 2

Master Orchestrator
"""

from vision_extractor import VisionExtractor
from normalizer import Normalizer
from repository_updater import RepositoryUpdater
from relationship_engine import RelationshipEngine
from reasoning_engine import ReasoningEngine
from xray_engine import XRayEngine


class ExecutiveAgent:

    # ----------------------------------------------------
    # Constructor
    # ----------------------------------------------------

    def __init__(
            self,
            api_key,
            repository):

        self.repository = repository

        self.vision = VisionExtractor(
            api_key
        )

        self.normalizer = Normalizer()

        self.repository_updater = RepositoryUpdater(
            repository
        )

        self.relationship_engine = RelationshipEngine()

        self.reasoning_engine = ReasoningEngine(
            api_key
        )

        self.executive_objects = []

        self.relationships = []

        self.current_report = None
        self.xray = XRayEngine()

    # ----------------------------------------------------
    # Load Report
    # ----------------------------------------------------

    def load_report(
            self,
            uploaded_file):

        self.current_report = uploaded_file.name

        pages = self.vision.process_pdf(
            uploaded_file
        )

        self.executive_objects = self.normalizer.normalize_report(

            pages,

            self.current_report

        )

        return len(self.executive_objects)

    # ----------------------------------------------------
    # Repository
    # ----------------------------------------------------

    def update_repository(self):

        return self.repository_updater.process_report(

            self.executive_objects

        )

    # ----------------------------------------------------
    # Relationships
    # ----------------------------------------------------

    def build_relationships(self):

        result = self.relationship_engine.process(

            self.executive_objects

        )

        self.executive_objects = result[
            "executive_objects"
        ]

        self.relationships = result[
            "relationships"
        ]

        return result

        # ----------------------------------------------------
    # Complete Processing Pipeline
    # ----------------------------------------------------

        # ----------------------------------------------------
    # Complete Processing Pipeline
    # ----------------------------------------------------

    def process_report(
            self,
            uploaded_file):

        self.xray.reset()

        # -------------------------------
        # Vision + Normalization
        # -------------------------------

        stage = self.xray.start_stage(
            "Vision + Normalizer"
        )

        total_objects = self.load_report(
            uploaded_file
        )

        self.xray.add_metric(
            stage,
            "Executive Objects",
            total_objects
        )

        self.xray.add_metric(
            stage,
            "Report",
            uploaded_file.name
        )

        self.xray.finish_stage(
            stage
        )

        # -------------------------------
        # Repository
        # -------------------------------

        stage = self.xray.start_stage(
            "Knowledge Repository"
        )

        repository_summary = self.update_repository()

        self.xray.add_metric(
            stage,
            "Objects Saved",
            repository_summary["objects_processed"]
        )

        self.xray.add_metric(
            stage,
            "Observations Saved",
            repository_summary["observations_inserted"]
        )

        self.xray.finish_stage(
            stage
        )

        # -------------------------------
        # Relationship Engine
        # -------------------------------

        stage = self.xray.start_stage(
            "Relationship Engine"
        )

        relationship_summary = self.build_relationships()

        self.xray.add_metric(
            stage,
            "Relationships",
            len(self.relationships)
        )

        self.xray.finish_stage(
            stage
        )

        return {

            "status": "SUCCESS",

            "report_name": self.current_report,

            "executive_objects": total_objects,

            "repository": repository_summary,

            "relationships": len(self.relationships),

            "relationship_summary": relationship_summary["summary"]

        }

        # ----------------------------------------------------
    # Executive Chat
    # ----------------------------------------------------

    def ask(
            self,
            question):

        stage = self.xray.start_stage(
            "Reasoning Engine"
        )

        result = self.reasoning_engine.process(

            question,

            self.executive_objects,

            self.relationships

        )

        self.xray.add_metric(

            stage,

            "Question",

            question

        )

        self.xray.add_metric(

            stage,

            "Executive Objects Used",

            len(self.executive_objects)

        )

        self.xray.add_metric(

            stage,

            "Relationships Used",

            len(self.relationships)

        )

        self.xray.add_metric(

            stage,

            "Question Type",

            result.get(

                "question_type",

                "Unknown"

            )

        )

        self.xray.finish_stage(

            stage

        )

        return result

    # ----------------------------------------------------
    # Repository Statistics
    # ----------------------------------------------------

    def repository_statistics(self):

        return self.repository_updater.repository_statistics()

    # ----------------------------------------------------
    # Health Check
    # ----------------------------------------------------

    def health_check(self):

        return {

            "Vision Agent": "READY",

            "Normalizer": "READY",

            "Repository": "READY",

            "Relationship Engine": "READY",

            "Reasoning Engine": "READY"

        }

        # ----------------------------------------------------
    # X-Ray
    # ----------------------------------------------------

    def get_xray(self):

        return self.xray.export()

    # ----------------------------------------------------
    # Reset
    # ----------------------------------------------------

    def reset(self):

        self.executive_objects = []

        self.relationships = []
        self.xray.reset()

        self.current_report = None

    # ----------------------------------------------------
    # Current Session
    # ----------------------------------------------------

    def current_session(self):

        return {

            "report": self.current_report,

            "executive_objects": len(

                self.executive_objects

            ),

            "relationships": len(

                self.relationships

            )

        }


if __name__ == "__main__":

    print()

    print("=" * 60)

    print("Executive Agent V2")

    print("Self Test Passed")

    print("=" * 60)

    
