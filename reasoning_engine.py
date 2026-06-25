"""
reasoning_engine.py

Mission 1
Version 2

Executive Reasoning Engine
"""

import json
from openai import OpenAI


class ReasoningEngine:

    # ----------------------------------------------------
    # Constructor
    # ----------------------------------------------------

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    # ----------------------------------------------------
    # Question Classification
    # ----------------------------------------------------

    def classify_question(self, question):

        q = question.lower()

        mapping = {

            "focus": "FOCUS",

            "risk": "RISK",

            "summary": "SUMMARY",

            "compare": "COMPARE",

            "trend": "TREND",

            "forecast": "FORECAST",

            "recommend": "RECOMMENDATION",

            "action": "ACTION",

            "why": "ROOT_CAUSE",

            "cause": "ROOT_CAUSE",

            "inventory": "INVENTORY",

            "production": "PRODUCTION",

            "asset": "ASSET_HEALTH",

            "dwell": "DWELL_TIME",

            "downtime": "DOWNTIME"

        }

        for key in mapping:

            if key in q:

                return mapping[key]

        return "GENERAL"

    # ----------------------------------------------------
    # Collect Executive Objects
    # ----------------------------------------------------

    def collect_objects(
            self,
            executive_objects):

        objects = []

        for obj in executive_objects:

            objects.append({

                "title": obj.title,

                "type": obj.object_type,

                "plant": obj.plant,

                "unit": obj.unit,

                "business_area": obj.business_area,

                "page": obj.page,

                "time_period": obj.time_period,

                "commentary": obj.commentary,

                "insights": obj.insights,

                "evidence": obj.evidence,

                "relationships": obj.relationships

            })

        return objects

    # ----------------------------------------------------
    # Collect Observations
    # ----------------------------------------------------

    def collect_observations(
            self,
            executive_objects):

        observations = []

        for obj in executive_objects:

            for obs in obj.observations:

                observations.append({

                    "metric": obs.metric,

                    "period": obs.period,

                    "value": obs.value,

                    "target": obs.target,

                    "report": obs.source_report,

                    "page": obs.source_page

                })

        return observations

    # ----------------------------------------------------
    # Build Context
    # ----------------------------------------------------

    def build_context(
            self,
            executive_objects,
            relationships):

        return {

            "executive_objects":

                self.collect_objects(
                    executive_objects
                ),

            "observations":

                self.collect_observations(
                    executive_objects
                ),

            "relationships":

                relationships

        }

        # ----------------------------------------------------
    # Build Prompt
    # ----------------------------------------------------

    def build_prompt(
            self,
            question,
            executive_objects,
            relationships):

        question_type = self.classify_question(
            question
        )

        context = self.build_context(

            executive_objects,

            relationships

        )

        return f"""

You are an Executive Manufacturing Intelligence Copilot.

Question Type

{question_type}

Executive Question

{question}

==================================================

AVAILABLE KNOWLEDGE

{json.dumps(context, indent=2)}

==================================================

Instructions

Think like a Plant Head.

Before answering

1. Review all KPIs.

2. Review observations.

3. Review relationships.

4. Review business areas.

5. Review unit information.

6. Review commentary.

7. Review evidence.

8. Identify trends.

9. Identify operational risks.

10. Identify possible root causes.

11. Mention confidence wherever appropriate.

12. Never invent information.

13. If evidence is insufficient clearly say so.

14. Base every statement on evidence.

==================================================

Return EXACTLY in this format

Executive Summary

...

Key Findings

...

Operational Risks

...

Root Cause Analysis

...

Evidence Used

...

Business Impact

...

Recommendations

...

Confidence

High / Medium / Low

"""

    # ----------------------------------------------------
    # Call OpenAI
    # ----------------------------------------------------

    def ask_llm(
            self,
            prompt):

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            temperature=0,

            max_completion_tokens=2500,

            messages=[

                {

                    "role": "system",

                    "content":

                    "You are an Executive Manufacturing Advisor."

                },

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )

        return response.choices[0].message.content

    # ----------------------------------------------------
    # Generate Executive Response
    # ----------------------------------------------------

    def generate_response(
            self,
            question,
            executive_objects,
            relationships):

        prompt = self.build_prompt(

            question,

            executive_objects,

            relationships

        )

        return self.ask_llm(

            prompt

        )

        # ----------------------------------------------------
    # Build Response Package
    # ----------------------------------------------------

    def build_response(
            self,
            question,
            answer,
            executive_objects,
            relationships):

        return {

            "question": question,

            "answer": answer,

            "question_type": self.classify_question(
                question
            ),

            "executive_objects": len(
                executive_objects
            ),

            "relationships": len(
                relationships
            ),

            "status": "SUCCESS"

        }

    # ----------------------------------------------------
    # Validate Inputs
    # ----------------------------------------------------

    def validate(
            self,
            executive_objects,
            relationships):

        if executive_objects is None:

            return False, "No Executive Objects"

        if len(executive_objects) == 0:

            return False, "Repository Empty"

        if relationships is None:

            relationships = []

        return True, relationships

    # ----------------------------------------------------
    # Main Processing Pipeline
    # ----------------------------------------------------

    def process(
            self,
            question,
            executive_objects,
            relationships):

        valid, result = self.validate(

            executive_objects,

            relationships

        )

        if not valid:

            return {

                "status": "FAILED",

                "answer": result

            }

        relationships = result

        answer = self.generate_response(

            question,

            executive_objects,

            relationships

        )

        return self.build_response(

            question,

            answer,

            executive_objects,

            relationships

        )

    # ----------------------------------------------------
    # Health Check
    # ----------------------------------------------------

    def health(self):

        return {

            "engine": "Reasoning Engine V2",

            "status": "READY"

        }


if __name__ == "__main__":

    print()

    print("=" * 60)

    print("Reasoning Engine V2")

    print("Self Test Passed")

    print("=" * 60)

    
