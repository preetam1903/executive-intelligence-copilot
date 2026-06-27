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
You are an Enterprise Dashboard Layout Intelligence Engine.

Analyze every chart on this dashboard page.

For every chart return ALL structural information that can be identified.

Return ONLY valid JSON.

For each chart return:

[
  {
    "header": "",
    "chart_type": "",
    "bbox": [0, 0, 0, 0],
    "confidence": 99,
    "structure": {
      "legend": [
        {
          "colour": "",
          "meaning": ""
        }
      ],
      "x_axis": {
        "title": "",
        "labels": []
      },
      "y_axis": {
        "title": "",
        "unit": "",
        "minimum": "",
        "maximum": "",
        "interval": ""
      }
    }
  }
]

Rules

1. Return ONLY valid JSON.
2. Do not infer metadata.
3. Do not infer business area.
4. Do not generate analysis capabilities.
5. Do not generate clarification items.
6. Leave unknown fields blank.

Example

[
{
"header":"Production Volume vs Target",

"chart_type":"Grouped Bar",

"bbox":[120,180,760,540],

"confidence":99,

"structure":{

"legend":[
{
"colour":"Blue",
"meaning":"Actual"
},
{
"colour":"Green",
"meaning":"Target"
}
],

"x_axis":{
"title":"Production Week",
"labels":["W1","W2","W3","W4"]
},

"y_axis":{
"title":"Production",
"unit":"KBOE",
"minimum":"0",
"maximum":"120",
"interval":"20"
},

"target_line":{
"present":true,
"label":"Target",
"value":"",
"colour":"Red"
},

"threshold_line":{
"present":false,
"label":"",
"value":""
},

"data_labels":{
"present":false
}

},

"clarification_required":[

]

}

]

Do not explain.
Return ONLY JSON.
"""
        response = self.client.chat.completions.create(

            model="gpt-4.1",
            temperature=0,
            max_completion_tokens=12000,

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

            

        )

        result = response.choices[0].message.content.strip()
        print("============== RAW GPT RESPONSE ==============")
        print(result)
        print("==============================================")

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return result
