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
You are an Enterprise Dashboard Layout Detection Engine.

Analyze this dashboard page.

For EVERY chart identify:

1. Header
2. Chart Type
3. Bounding Box
   [left, top, right, bottom]
4. Confidence (0-100)

Now analyse the chart structure.

For each item return one of:

Present
Missing
Not Applicable
Low Confidence

Check:

- Header
- Legend
- X Axis Title
- X Axis Labels
- Y Axis Title
- Y Axis Labels
- Units
- Target Line
- Threshold Line
- Data Labels

Do NOT guess.

If an item is unclear, return Low Confidence.

Return ONLY valid JSON.

Example

[
{
"header":"Production Volume vs Target",
"chart_type":"Grouped Bar",
"bbox":[120,180,760,540],
"confidence":99,
"structure":{
"header":"Present",
"legend":"Present",
"x_axis_title":"Present",
"x_axis_labels":"Present",
"y_axis_title":"Missing",
"y_axis_labels":"Present",
"units":"Present",
"target_line":"Present",
"threshold":"Not Applicable",
"data_labels":"Missing"
}
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
