from openai import OpenAI
import base64
import io


class HeaderAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    def _image_to_base64(self, image):

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def detect_headers(self, page_image):

        image_b64 = self._image_to_base64(page_image)

        prompt = """
You are an expert dashboard layout detection engine.

Analyze this dashboard page.

For every chart return:

1. Header
2. Chart Type
3. Bounding Box [left, top, right, bottom]
4. Confidence (0-100)
5. Missing Structural Items

Possible Missing Items:

- Header
- Legend
- X Axis Title
- Y Axis Title
- Units
- Target Line
- Threshold
- Data Labels

Return ONLY valid JSON.

Example:

[
  {
    "header":"Production Volume vs Target",
    "chart_type":"Grouped Bar",
    "bbox":[120,180,760,540],
    "confidence":99,
    "missing_items":[]
  }
]

Do not explain.
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            messages=[

                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        }
                    ]
                }

            ],

            temperature=0

        )

        return response.choices[0].message.content
