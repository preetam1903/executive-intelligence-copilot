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
You are a Senior Business Intelligence Chart Analyst.

Your ONLY responsibility is to extract chart values.

The chart structure has already been detected.

Do NOT detect:
- Chart Type
- Legend
- X Axis
- Y Axis
- Units

These are already known.

==================================================

CHART METADATA

{json.dumps(layout_json, indent=2)}

==================================================

IMPORTANT

Ignore:

- Chart title
- Chart number
- White margins
- Legend area
- Decorative elements

Focus ONLY on the plotted data region.

==================================================

YOUR TASK

Read every plotted value.

If it is a Bar chart:
- Detect every bar
- Read every bar height
- Convert height to actual value using the Y-axis scale

If it is a Grouped Bar:
- Read every bar for every series
- Keep series separate

If it is a Stacked Bar:
- Read every coloured stack independently
- Return each stack value
- Return stack total if visible

If it is a Line chart:
- Read every point

If it is a Scatter chart:
- Read every point coordinate

==================================================

Rules

Never invent values.

If uncertain,
estimate using the Y-axis.

Every value must contain

- x
- y
- confidence
- extraction_method

Confidence

100 = exact label

95 = accurate visual reading

80 = estimated

60 = uncertain

Below 60

Do NOT guess.

==================================================

Return ONLY JSON.

Example

{
  "series":[
    {
      "name":"Actual",
      "points":[
        {
          "x":"2023-W01",
          "y":95,
          "confidence":97,
          "extraction_method":"Bar Height"
        }
      ]
    }
  ]
}
"""


        response = self.client.chat.completions.create(

            model="gpt-4.1",

            temperature=0.1,

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
