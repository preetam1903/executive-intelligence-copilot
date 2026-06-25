"""
vision_extractor.py

Mission 1

PDF → Images → GPT Vision → Standard JSON

Author : Executive Intelligence Platform
"""

import json
import base64
from io import BytesIO

import fitz  # PyMuPDF
from PIL import Image
from openai import OpenAI


class VisionExtractor:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    # ---------------------------------------------------------
    # Convert PDF page to Image
    # ---------------------------------------------------------

    def pdf_page_to_image(self, pdf_document, page_number):

        page = pdf_document.load_page(page_number)

        pix = page.get_pixmap(dpi=220)

        image = Image.open(BytesIO(pix.tobytes("png")))

        return image

    # ---------------------------------------------------------
    # Image → Base64
    # ---------------------------------------------------------

    def image_to_base64(self, image):

        buffer = BytesIO()

        image.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode()

    # ---------------------------------------------------------
    # Standard Prompt
    # ---------------------------------------------------------

    def build_prompt(self):

        return """
You are an Executive Manufacturing Intelligence extractor.

Return ONLY valid JSON.

Do not explain anything.

Your PRIMARY objective is to extract structured business intelligence from EVERY chart on this page.

For EVERY chart extract:

1. Chart Title
2. Chart Type
3. Business Area
4. X Axis Title
5. X Axis Labels
6. Y Axis Title
7. Y Axis Unit
8. Legend
9. Every Data Series
10. Every Visible Numerical Value
11. Target Line
12. Threshold Line
13. Trend
14. Commentary

After ALL charts are processed, extract:

- Tables
- KPI Cards
- Risks
- Actions
- Images
- Business Areas
- Units

Return JSON in this exact format.

{
  "page": 1,
  "executive_objects": [
    {
      "object_type": "KPI",
      "title": "Production",
      "unit": "HSM",
      "business_area": "Production",
      "time_period": "Weekly",
      "observations": [
        {
          "metric": "Production",
          "period": "W1",
          "value": "97",
          "target": "100"
        },
        {
          "metric": "Production",
          "period": "W2",
          "value": "95",
          "target": "100"
        }
      ],
      "commentary": [],
      "domain_intelligence": {
        "trend": "Down",
        "risk": "High"
      }
    }
  ]
}

IMPORTANT

Every item inside "observations" MUST be a JSON object.

Never return strings.

Never return numbers.

Never return arrays of values.

Each observation must contain:

metric
period
value
target
For charts extract:

Title

Chart Type

XAxis

YAxis

Series

Target

Actual

Forecast

Threshold

Trend

For Scatter Plot additionally extract

Correlation

Outliers

Clusters

Anomalies

Regression

Never omit information.

Return only JSON.
"""

    # ---------------------------------------------------------
    # Analyze One Image
    # ---------------------------------------------------------

    def analyze_image(self, image):

        encoded = self.image_to_base64(image)

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            response_format={"type": "json_object"},

            messages=[

                {

                    "role": "user",

                    "content": [

                        {

                            "type": "text",

                            "text": self.build_prompt()

                        },

                        {

                            "type": "image_url",

                            "image_url": {

                                "url": f"data:image/png;base64,{encoded}"

                            }

                        }

                    ]

                }

            ]

        )

        return json.loads(

            response.choices[0].message.content

        )

    # ---------------------------------------------------------
    # Process Complete PDF
    # ---------------------------------------------------------

    def process_pdf(self, uploaded_file):

        pdf = fitz.open(stream=uploaded_file.read(),
                        filetype="pdf")

        pages = []

        for page_number in range(len(pdf)):

            image = self.pdf_page_to_image(pdf,
                                           page_number)

            result = self.analyze_image(image)

            pages.append(result)

        pdf.close()

        return pages
