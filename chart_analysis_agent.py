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

        example_json = """
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
                },
                {
                    "x":"2023-W02",
                    "y":98,
                    "confidence":95,
                    "extraction_method":"Bar Height"
                }
            ]
        }
    ]
}
"""

        prompt = f"""
You are a Senior Enterprise Chart Analysis Agent.

The dashboard layout has already been analysed.

The following information is already known.

{json.dumps(layout_json, indent=2)}

------------------------------------------------

Ignore

- Dashboard title
- Chart title
- Legend
- White margins
- Decorative elements

Focus ONLY on the plotted data.

------------------------------------------------

If chart_type is

Bar

Read every bar.

Grouped Bar

Read every series separately.

Stacked Bar

Read every coloured stack separately.

Line

Read every point.

Scatter

Read every point coordinate.

------------------------------------------------

Rules

Never invent values.

Estimate only when necessary.

Every extracted value must contain

x

y

confidence

extraction_method

Confidence

100 = exact

95 = visual

80 = estimated

60 = uncertain

Below 60

Do not guess.

Return ONLY valid JSON.

Example

{example_json}
"""




                response = self.client.chat.completions.create(

                    model="gpt-4.1",

                    temperature=0.1,

                    max_completion_tokens=4000,

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

                result = response.choices[0].message.content.strip()

                result = result.replace("```json", "")
                result = result.replace("```", "")
                result = result.strip()

                try:

                    json.loads(result)

                    return result

                except Exception as e:

                    print("Invalid JSON returned by GPT")
                    print(result)

                    return json.dumps(
                        {
                            "error": "Invalid JSON returned",
                            "raw_response": result
                        },
                        indent=4
                    )
