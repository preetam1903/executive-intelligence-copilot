import json
import base64
from io import BytesIO

from PIL import Image
from openai import OpenAI


class ChartAnalysisAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    def image_to_base64(self, image):

        buffer = BytesIO()

        image.save(buffer, format="PNG")

        return base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

    def analyze_chart(self, chart_image, layout_json):

        image_base64 = self.image_to_base64(chart_image)

        prompt = f"""
You are an Enterprise Chart Analysis Agent.

The chart layout has already been identified.

DO NOT detect:

- Chart Type
- Legend
- Axis
- Units

Use the metadata below.

Chart Metadata

{json.dumps(layout_json, indent=2)}

------------------------------------------------

Your ONLY task is to extract numerical values.

Instructions

1. Read every visible data series.

2. Return every point.

3. If a value cannot be read exactly,
estimate it using the Y-axis.

4. Every value must contain:

- x
- y
- confidence
- extraction_method

5. Confidence should be between 0 and 100.

6. extraction_method should be one of

- Data Label
- Bar Height
- Line Position
- Scatter Position
- Estimated from Axis

Return ONLY valid JSON.

Example

{{
    "series":[
        {{
            "name":"Actual",
            "points":[
                {{
                    "x":"2023-W01",
                    "y":92,
                    "confidence":98,
                    "extraction_method":"Bar Height"
                }},
                {{
                    "x":"2023-W02",
                    "y":95,
                    "confidence":97,
                    "extraction_method":"Bar Height"
                }}
            ]
        }}
    ]
}}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            temperature=0,

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
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }

                    ]
                }

            ]

        )

        return response.choices[0].message.content
