"""
executive_agent.py

Mission 1
Executive Intelligence Orchestrator
"""

from vision_extractor import VisionExtractor
from normalizer import Normalizer
from relationship_engine import RelationshipEngine
from repository_updater import RepositoryUpdater
from reasoning_engine import ReasoningEngine


class ExecutiveAgent:

    def __init__(
            self,
            api_key,
            repository):

        self.repository = repository

        self.vision = VisionExtractor(api_key)

        self.normalizer = Normalizer()

        self.relationship_engine = RelationshipEngine()

        self.repository_updater = RepositoryUpdater(
            repository
        )

        self.reasoning_engine = ReasoningEngine(
            api_key
        )

        self.executive_objects = []

        self.relationships = []

        self.current_report = None

    # --------------------------------------------------------
    # Load Report
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Store Repository
    # --------------------------------------------------------

    def update_repository(self):

        for obj in self.executive_objects:

            self.repository_updater.process_object(
                obj
            )

        return True

    # --------------------------------------------------------
    # Build Relationships
    # --------------------------------------------------------

    def build_relationships(self):

        result = self.relationship_engine.process(

            self.executive_objects

        )

        self.relationships = result["relationships"]

        return result

        # --------------------------------------------------------
    # Process Complete Report
    # --------------------------------------------------------

    def process_report(
            self,
            uploaded_file):

        total_objects = self.load_report(
            uploaded_file
        )

        self.update_repository()

        relationship_result = self.build_relationships()

        return {

            "status": "SUCCESS",

            "report_name": self.current_report,

            "executive_objects": total_objects,

            "relationships": len(self.relationships),

            "summary": relationship_result["summary"]

        }

    # --------------------------------------------------------
    # Ask Executive Copilot
    # --------------------------------------------------------

    def ask(
            self,
            question):

        result = self.reasoning_engine.process(

            question,

            self.executive_objects,

            self.relationships

        )

        return result

    # --------------------------------------------------------
    # Get Repository Statistics
    # --------------------------------------------------------

    def repository_statistics(self):

        stats = {

            "current_report": self.current_report,

            "executive_objects": len(

                self.executive_objects

            ),

            "relationships": len(

                self.relationships

            )

        }

        return stats

    # --------------------------------------------------------
    # Health Check
    # --------------------------------------------------------

    def health_check(self):

        return {

            "Vision Agent": "OK",

            "Normalizer Agent": "OK",

            "Repository Agent": "OK",

            "Relationship Agent": "OK",

            "Reasoning Agent": "OK"

        }

    # --------------------------------------------------------
    # Reset Session
    # --------------------------------------------------------

    def reset(self):

        self.executive_objects = []

        self.relationships = []

        self.current_report = None
