from openai import OpenAI
import base64
import io
import json


class XAxisAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    def _image_to_base64(self, image):

        buffer = io.BytesIO()

        image.save(buffer, format="PNG")

        return base64.b64encode(
            buffer.getvalue()
        ).decode()

    def extract_labels(self, chart_image):

        image_b64 = self._image_to_base64(chart_image)

        prompt = """
You are an OCR engine.

Your ONLY job is to read the X-axis labels from this chart.

Rules

1. Read every visible X-axis label.
2. Read from left to right.
3. Preserve the exact text.
4. Do not guess.
5. Return ONLY JSON.

Example

{
    "labels":[
        "2022-W52",
        "2023-W01",
        "2023-W02",
        "2023-W03"
    ]
}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            temperature=0,

            messages=[

                {
                    "role":"user",

                    "content":[

                        {
                            "type":"text",
                            "text":prompt
                        },

                        {
                            "type":"image_url",
                            "image_url":{
                                "url":f"data:image/png;base64,{image_b64}"
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

        return json.loads(result)
