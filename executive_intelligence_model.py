"""
Executive Intelligence Model
Mission 1 - Version 1.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
import uuid


def generate_id():
    return str(uuid.uuid4())


# -------------------------------------------------------
# Observation (Atomic Fact)
# -------------------------------------------------------

@dataclass
class Observation:

    observation_id: str = field(default_factory=generate_id)

    metric: str = ""

    period: str = ""

    value: Any = None

    target: Any = None

    source_report: str = ""

    source_page: int = 0

    confidence: float = 1.0

    metadata: Dict = field(default_factory=dict)


# -------------------------------------------------------
# Executive Intelligence Object
# -------------------------------------------------------

@dataclass
class ExecutiveIntelligenceObject:

    object_id: str = field(default_factory=generate_id)

    object_type: str = ""

    title: str = ""

    plant: str = "Plant"

    unit: str = ""

    business_area: str = ""

    page: int = 0

    report_name: str = ""

    time_period: str = ""

    observations: List[Observation] = field(default_factory=list)

    commentary: List[str] = field(default_factory=list)

    insights: List[str] = field(default_factory=list)

    evidence: List[str] = field(default_factory=list)

    relationships: List[str] = field(default_factory=list)

    domain_intelligence: Dict = field(default_factory=dict)

    metadata: Dict = field(default_factory=dict)


# -------------------------------------------------------
# Business Area
# -------------------------------------------------------

@dataclass
class BusinessArea:

    name: str

    executive_objects: Dict[str, ExecutiveIntelligenceObject] = field(default_factory=dict)


# -------------------------------------------------------
# Unit
# -------------------------------------------------------

@dataclass
class Unit:

    name: str

    business_areas: Dict[str, BusinessArea] = field(default_factory=dict)


# -------------------------------------------------------
# Plant
# -------------------------------------------------------

@dataclass
class Plant:

    name: str = "Plant"

    business_areas: Dict[str, BusinessArea] = field(default_factory=dict)

    units: Dict[str, Unit] = field(default_factory=dict)


# -------------------------------------------------------
# Executive Intelligence Model
# -------------------------------------------------------

class ExecutiveIntelligenceModel:

    def __init__(self):

        self.plant = Plant()

        self.relationships = []

        self.discovery_queue = []

        self.report_history = []

    # --------------------------

    def add_business_area(self, area_name):

        if area_name not in self.plant.business_areas:

            self.plant.business_areas[area_name] = BusinessArea(area_name)

    # --------------------------

    def add_unit(self, unit_name):

        if unit_name not in self.plant.units:

            self.plant.units[unit_name] = Unit(unit_name)

    # --------------------------

    def add_business_area_to_unit(self, unit_name, area_name):

        self.add_unit(unit_name)

        unit = self.plant.units[unit_name]

        if area_name not in unit.business_areas:

            unit.business_areas[area_name] = BusinessArea(area_name)

    # --------------------------

    def add_object_to_business_area(self,
                                    area_name,
                                    executive_object):

        self.add_business_area(area_name)

        self.plant.business_areas[
            area_name
        ].executive_objects[
            executive_object.object_id
        ] = executive_object

    # --------------------------

    def add_object_to_unit(self,
                           unit_name,
                           area_name,
                           executive_object):

        self.add_business_area_to_unit(unit_name,
                                       area_name)

        self.plant.units[
            unit_name
        ].business_areas[
            area_name
        ].executive_objects[
            executive_object.object_id
        ] = executive_object

    # --------------------------

    def add_relationship(self,
                         relationship):

        self.relationships.append(relationship)

    # --------------------------

    def add_discovery(self,
                      discovery):

        self.discovery_queue.append(discovery)

    # --------------------------

    def add_report(self,
                   report_name):

        if report_name not in self.report_history:

            self.report_history.append(report_name)
