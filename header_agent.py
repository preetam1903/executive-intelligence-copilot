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

{
    "header":"",
    "chart_type":"",
    "bbox":[left,top,right,bottom],
    "confidence":99,

    "structure":{

        "legend":[
            {
                "colour":"",
                "meaning":""
            }
        ],

        "x_axis":{
            "title":"",
            "labels":[]
        },

        "y_axis":{
            "title":"",
            "unit":"",
            "minimum":"",
            "maximum":"",
            "interval":""
        },

        "target_line":{
            "present":true,
            "label":"",
            "value":"",
            "colour":""
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

"metadata":{

"x_axis_type":"",

"time_granularity":"",

"number_of_periods":"",

"number_of_series":"",

"orientation":"",

"chart_purpose":"",

"business_area":"",

"supports_trend_analysis":true,

"supports_target_comparison":true,

"supports_correlation":true

},

"analysis_capabilities":{

"can_extract_values":true,

"can_detect_spikes":true,

"can_detect_outliers":true,

"can_detect_trend":true,

"can_compare_series":true,

"can_forecast":true

},

Rules

1. Extract every piece of structural information visible.

2. Infer chart metadata.

3. Identify analysis capabilities.

4. If the X-axis contains values like 202252, convert them to YearWeek format (2022-W52).

5. If anything cannot be determined confidently, leave it blank.

6. If clarification is required, add a learning item.

7. Return ONLY valid JSON.

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
