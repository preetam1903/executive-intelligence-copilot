"""
=========================================================
Executive Intelligence Copilot
Chart Understanding Agent
=========================================================

Responsibility
--------------
Understand the business meaning of each chart.

Current Version:
- Placeholder implementation.

Future Version:
- GPT Vision
- Chart reasoning
- Executive summary generation
"""
import json
import base64
from openai import OpenAI
import streamlit as st

class ChartUnderstandingAgent:

    def __init__(self):

        self.client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )

    def encode_image(self, image_path):
        """
        Convert image to Base64 for GPT Vision.
        """

        with open(image_path, "rb") as image_file:

            return base64.b64encode(
                image_file.read()
            ).decode("utf-8")

    def understand_chart(self, image_path):

        base64_image = self.encode_image(image_path)

        prompt = """
    You are an Executive Manufacturing Intelligence Agent.

    Analyse the chart image.

    Return ONLY valid JSON.

    {
        "chart_type":"",
        "chart_title":"",
        "business_area":"",
        "metric":"",
        "x_axis":"",
        "left_y_axis":"",
        "right_y_axis":"",
        "legend":[],
        "summary":"",
        "missing_information":[],
        "confidence":0.0
    }

    Rules:

    - Return JSON only.
    - No markdown.
    - No explanation.
    - Confidence must be between 0 and 1.
    - If information is unavailable, use empty string or empty array.
    """

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            response_format={"type": "json_object"},

            messages=[

                {
                    "role": "user",

                    "content": [

                        {
                            "type": "text",
                            "text": prompt
                        },

                        {
                            "type": "image_url",

                            "image_url": {

                                "url": f"data:image/png;base64,{base64_image}"

                            }

                        }

                    ]

                }

            ]

        )

        return json.loads(
            response.choices[0].message.content
        )

    #############

    def process(self, charts):

        understood_charts = []

        for chart in charts:

            try:

                understanding = self.understand_chart(
                    chart["image"]
                )

                chart["chart_type"] = understanding.get(
                    "chart_type",
                    ""
                )

                chart["chart_title"] = understanding.get(
                    "chart_title",
                    ""
                )

                chart["business_area"] = understanding.get(
                    "business_area",
                    ""
                )

                chart["metric"] = understanding.get(
                    "metric",
                    ""
                )

                chart["x_axis"] = understanding.get(
                    "x_axis",
                    ""
                )

                chart["left_y_axis"] = understanding.get(
                    "left_y_axis",
                    ""
                )

                chart["right_y_axis"] = understanding.get(
                    "right_y_axis",
                    ""
                )

                chart["legend"] = understanding.get(
                    "legend",
                    []
                )

                chart["summary"] = understanding.get(
                    "summary",
                    ""
                )

                chart["missing_information"] = understanding.get(
                    "missing_information",
                    []
                )

                chart["confidence"] = understanding.get(
                    "confidence",
                    0.0
                )

            except Exception as e:

                chart["chart_type"] = "Unknown"

                chart["chart_title"] = "Analysis Failed"

                chart["business_area"] = ""

                chart["metric"] = ""

                chart["x_axis"] = ""

                chart["left_y_axis"] = ""

                chart["right_y_axis"] = ""

                chart["legend"] = []

                chart["summary"] = str(e)

                chart["missing_information"] = ["AI Analysis Failed"]

                chart["confidence"] = 0.0

            understood_charts.append(chart)

        return understood_charts
