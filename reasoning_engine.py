"""
reasoning_engine.py

Mission 1
Executive Intelligence Copilot

Version 1
"""

import json

from openai import OpenAI


class ReasoningEngine:

    def __init__(self,
                 api_key):

        self.client = OpenAI(
            api_key=api_key
        )

    # --------------------------------------------------------
    # Question Classification
    # --------------------------------------------------------

    def classify_question(
            self,
            question):

        q = question.lower()

        if "focus" in q:
            return "FOCUS"

        if "risk" in q:
            return "RISK"

        if "summary" in q:
            return "SUMMARY"

        if "compare" in q:
            return "COMPARE"

        if "why" in q:
            return "ROOT_CAUSE"

        if "recommend" in q:
            return "RECOMMENDATION"

        return "GENERAL"

    # --------------------------------------------------------
    # Collect Evidence
    # --------------------------------------------------------

    def collect_evidence(
            self,
            executive_objects):

        evidence = []

        for obj in executive_objects:

            evidence.append({

                "title": obj.title,

                "type": obj.object_type,

                "business_area": obj.business_area,

                "unit": obj.unit,

                "page": obj.page,

                "commentary": obj.commentary,

                "relationships": obj.relationships,

                "observations": [

                    vars(obs)

                    for obs in obj.observations

                ]

            })

        return evidence

    # --------------------------------------------------------
    # Related Metrics
    # --------------------------------------------------------

    def related_metrics(
            self,
            executive_objects):

        metrics = []

        for obj in executive_objects:

            for obs in obj.observations:

                metrics.append({

                    "metric": obs.metric,

                    "period": obs.period,

                    "value": obs.value,

                    "target": obs.target

                })

        return metrics

        # --------------------------------------------------------
    # Relationship Context
    # --------------------------------------------------------

    def relationship_context(
            self,
            relationships):

        context = []

        for rel in relationships:

            context.append({

                "source": rel.get("source", ""),

                "target": rel.get("target", ""),

                "relationship": rel.get("relationship", ""),

                "confidence": rel.get("confidence", 0)

            })

        return context

    # --------------------------------------------------------
    # Build AI Context
    # --------------------------------------------------------

    def build_context(
            self,
            executive_objects,
            relationships):

        context = {

            "executive_objects":

                self.collect_evidence(
                    executive_objects
                ),

            "related_metrics":

                self.related_metrics(
                    executive_objects
                ),

            "relationships":

                self.relationship_context(
                    relationships
                )

        }

        return context

    # --------------------------------------------------------
    # Prompt Builder
    # --------------------------------------------------------

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

        prompt = f"""
You are an Executive Manufacturing Intelligence Copilot.

Question Type:
{question_type}

Executive Question:
{question}

Available Operational Knowledge:

{json.dumps(context, indent=2)}

Instructions

Think like a COO of a manufacturing company.

Before answering ALWAYS

1. Review every KPI.

2. Review every chart.

3. Review commentary.

4. Review target breaches.

5. Review related metrics.

6. Review relationships.

7. Look for operational patterns.

8. Check if one KPI may explain another.

9. If multiple causes are possible, mention them.

10. Base every statement on evidence.

Never invent information.

If evidence is insufficient, clearly state that.

Prioritize operational impact over statistical description.

Return EXACTLY in this format

━━━━━━━━━━━━━━━━━━

Executive Summary

━━━━━━━━━━━━━━━━━━

...

━━━━━━━━━━━━━━━━━━

Evidence

━━━━━━━━━━━━━━━━━━

...

━━━━━━━━━━━━━━━━━━

Related Metrics Checked

━━━━━━━━━━━━━━━━━━

...

━━━━━━━━━━━━━━━━━━

AI Reasoning

━━━━━━━━━━━━━━━━━━

...

━━━━━━━━━━━━━━━━━━

Recommended Actions

━━━━━━━━━━━━━━━━━━

...
"""

        return prompt

        # --------------------------------------------------------
    # Ask OpenAI
    # --------------------------------------------------------

    def ask_llm(
            self,
            prompt):

        try:

            response = self.client.chat.completions.create(

                model="gpt-4.1",
                max_completion_tokens=2500,

                temperature=0,

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are an experienced Manufacturing "
                            "Executive Advisor. Base every answer only "
                            "on the supplied operational evidence."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ]

            )

            return response.choices[0].message.content

        except Exception as ex:

            return f"""
            Executive Summary

            Unable to generate answer.

            Evidence

            Not Available

            AI Reasoning

            OpenAI Error

            Details

            {str(ex)}
            """

    # --------------------------------------------------------
    # Generate Executive Answer
    # --------------------------------------------------------

    def generate_answer(
            self,
            question,
            executive_objects,
            relationships):

        prompt = self.build_prompt(

            question,

            executive_objects,

            relationships

        )

        answer = self.ask_llm(

            prompt

        )

        return answer

    # --------------------------------------------------------
    # Build Executive Package
    # --------------------------------------------------------

    def executive_package(
            self,
            question,
            executive_objects,
            relationships):

        answer = self.generate_answer(

            question,

            executive_objects,

            relationships

        )

        package = {

            "question": question,

            "answer": answer,

            "relationship_count": len(relationships),

            "executive_object_count": len(executive_objects)

        }

        return package

        # --------------------------------------------------------
    # Validate Context
    # --------------------------------------------------------

    def validate_context(
            self,
            executive_objects,
            relationships):

        validation = {

            "objects_found": len(executive_objects),

            "relationships_found": len(relationships),

            "status": "OK"

        }

        if len(executive_objects) == 0:

            validation["status"] = "NO_EXECUTIVE_OBJECTS"

        return validation

    # --------------------------------------------------------
    # Future Hook (Mission 2)
    # Executive Challenge Agent
    # --------------------------------------------------------

    def challenge_answer(
            self,
            answer):

        # Mission 2:
        # Challenge the answer by checking
        # - Missing KPIs
        # - Missing Commentary
        # - Missing Relationships
        # - Alternative Explanations

        return answer

    # --------------------------------------------------------
    # Main Entry Point
    # --------------------------------------------------------

    def process(
            self,
            question,
            executive_objects,
            relationships):

        validation = self.validate_context(
            executive_objects,
            relationships
        )

        if validation["status"] != "OK":

            return {

                "status": validation["status"],

                "answer": "No operational knowledge available."

            }

        package = self.executive_package(

            question,

            executive_objects,

            relationships

        )

        package["answer"] = self.challenge_answer(

            package["answer"]

        )

        package["validation"] = validation

        return package
