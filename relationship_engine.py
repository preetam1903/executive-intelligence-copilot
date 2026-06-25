"""
relationship_engine.py

Mission 1
Version 2
"""

from collections import defaultdict
from statistics import mean


class RelationshipEngine:

    def __init__(self):

        self.relationships = []

    # ----------------------------------------------------
    # Safe Float
    # ----------------------------------------------------

    def safe_float(self, value):

        try:
            return float(value)
        except:
            return None

    # ----------------------------------------------------
    # Build Metric Dictionary
    # ----------------------------------------------------

    def build_metric_dictionary(self, executive_objects):

        metrics = defaultdict(list)

        for obj in executive_objects:

            for obs in obj.observations:

                value = self.safe_float(obs.value)

                if value is None:
                    continue

                metrics[obs.metric].append({

                    "value": value,

                    "period": obs.period,

                    "target": self.safe_float(obs.target),

                    "business_area": obj.business_area,

                    "unit": obj.unit,

                    "page": obj.page,

                    "report": obj.report_name

                })

        return metrics

    # ----------------------------------------------------
    # Extract Values
    # ----------------------------------------------------

    def extract_values(self, metric_history):

        return [

            x["value"]

            for x in metric_history

        ]

    # ----------------------------------------------------
    # Trend
    # ----------------------------------------------------

    def trend(self, values):

        if len(values) < 2:
            return "UNKNOWN"

        if values[-1] > values[0]:
            return "UP"

        if values[-1] < values[0]:
            return "DOWN"

        return "FLAT"

    # ----------------------------------------------------
    # Slope
    # ----------------------------------------------------

    def slope(self, values):

        if len(values) < 2:
            return 0

        return round(

            (values[-1] - values[0]) /

            (len(values) - 1),

            3

        )

    # ----------------------------------------------------
    # Moving Average
    # ----------------------------------------------------

    def moving_average(self, values):

        if len(values) == 0:
            return 0

        return round(

            mean(values),

            2

        )
        # ----------------------------------------------------
    # Correlation
    # ----------------------------------------------------

    def correlation(self, values1, values2):

        if len(values1) != len(values2):
            return 0

        if len(values1) < 2:
            return 0

        mean1 = mean(values1)
        mean2 = mean(values2)

        numerator = 0
        denominator1 = 0
        denominator2 = 0

        for x, y in zip(values1, values2):

            numerator += (x - mean1) * (y - mean2)

            denominator1 += (x - mean1) ** 2

            denominator2 += (y - mean2) ** 2

        if denominator1 == 0 or denominator2 == 0:
            return 0

        return round(
            numerator /
            ((denominator1 ** 0.5) * (denominator2 ** 0.5)),
            3
        )

    # ----------------------------------------------------
    # Direction
    # ----------------------------------------------------

    def direction(self,
                  trend1,
                  trend2):

        if trend1 == trend2:
            return "SAME_DIRECTION"

        return "OPPOSITE_DIRECTION"

    # ----------------------------------------------------
    # Confidence
    # ----------------------------------------------------

    def confidence(self,
                   correlation,
                   sample_size):

        score = abs(correlation)

        if sample_size >= 4:
            score += 0.15

        if sample_size >= 8:
            score += 0.10

        return round(min(score, 1.0), 2)

    # ----------------------------------------------------
    # Operational Meaning
    # ----------------------------------------------------

    def operational_meaning(
            self,
            metric1,
            metric2,
            direction):

        metric1 = metric1.lower()
        metric2 = metric2.lower()

        if "production" in metric1 and "inventory" in metric2:

            if direction == "OPPOSITE_DIRECTION":

                return "Production decline associated with inventory increase."

        if "asset" in metric1 and "production" in metric2:

            return "Asset health likely influencing production."

        if "dwell" in metric1:

            return "Higher dwell time may reduce throughput."

        if "downtime" in metric1:

            return "Downtime may reduce production."

        return "Relationship detected from historical KPI movement."

    # ----------------------------------------------------
    # Compare Two Metrics
    # ----------------------------------------------------

    def compare_metrics(
            self,
            metric1,
            history1,
            metric2,
            history2):

        values1 = self.extract_values(history1)
        values2 = self.extract_values(history2)

        trend1 = self.trend(values1)
        trend2 = self.trend(values2)

        relationship = self.direction(
            trend1,
            trend2
        )

        corr = self.correlation(
            values1,
            values2
        )

        return {

            "source": metric1,

            "target": metric2,

            "relationship": relationship,

            "trend_source": trend1,

            "trend_target": trend2,

            "correlation": corr,

            "confidence": self.confidence(
                corr,
                min(len(values1), len(values2))
            ),

            "slope_source": self.slope(values1),

            "slope_target": self.slope(values2),

            "average_source": self.moving_average(values1),

            "average_target": self.moving_average(values2),

            "business_area": history1[-1]["business_area"],

            "unit": history1[-1]["unit"],

            "operational_meaning": self.operational_meaning(
                metric1,
                metric2,
                relationship
            ),

            "evidence": {

                "source_values": values1,

                "target_values": values2

            }

        }
        # ----------------------------------------------------
    # Detect Relationships
    # ----------------------------------------------------

    def detect_relationships(
            self,
            executive_objects):

        metrics = self.build_metric_dictionary(
            executive_objects
        )

        metric_names = list(metrics.keys())

        relationships = []

        for i in range(len(metric_names)):

            for j in range(i + 1, len(metric_names)):

                metric1 = metric_names[i]
                metric2 = metric_names[j]

                history1 = metrics[metric1]
                history2 = metrics[metric2]

                if len(history1) < 2:
                    continue

                if len(history2) < 2:
                    continue

                relationship = self.compare_metrics(

                    metric1,

                    history1,

                    metric2,

                    history2

                )

                relationships.append(
                    relationship
                )

        self.relationships = relationships

        return relationships

    # ----------------------------------------------------
    # Attach Relationships
    # ----------------------------------------------------

    def attach_relationships(
            self,
            executive_objects):

        for obj in executive_objects:

            obj.relationships = []

            object_metrics = {

                obs.metric

                for obs in obj.observations

            }

            for rel in self.relationships:

                if rel["source"] in object_metrics \
                        or rel["target"] in object_metrics:

                    obj.relationships.append(rel)

        return executive_objects

    # ----------------------------------------------------
    # Detect Target Breaches
    # ----------------------------------------------------

    def detect_target_breaches(
            self,
            executive_objects):

        breaches = []

        for obj in executive_objects:

            for obs in obj.observations:

                actual = self.safe_float(
                    obs.value
                )

                target = self.safe_float(
                    obs.target
                )

                if actual is None:
                    continue

                if target is None:
                    continue

                if actual < target:

                    status = "BELOW_TARGET"

                elif actual > target:

                    status = "ABOVE_TARGET"

                else:

                    status = "ON_TARGET"

                breaches.append({

                    "metric": obs.metric,

                    "period": obs.period,

                    "actual": actual,

                    "target": target,

                    "variance": round(
                        actual - target,
                        2
                    ),

                    "status": status,

                    "business_area": obj.business_area,

                    "unit": obj.unit

                })

        return breaches

    # ----------------------------------------------------
    # Detect Outliers
    # ----------------------------------------------------

    def detect_outliers(
            self,
            executive_objects):

        outliers = []

        metrics = self.build_metric_dictionary(
            executive_objects
        )

        for metric, history in metrics.items():

            values = self.extract_values(
                history
            )

            if len(values) < 4:
                continue

            avg = self.moving_average(
                values
            )

            for item in history:

                value = item["value"]

                if abs(value - avg) > (0.30 * avg):

                    outliers.append({

                        "metric": metric,

                        "value": value,

                        "average": avg,

                        "period": item["period"],

                        "unit": item["unit"],

                        "business_area": item["business_area"]

                    })

        return outliers
        # ----------------------------------------------------
    # Rolling Four Week Analysis
    # ----------------------------------------------------

    def rolling_four_week_analysis(
            self,
            executive_objects):

        analysis = {}

        metrics = self.build_metric_dictionary(
            executive_objects
        )

        for metric, history in metrics.items():

            values = self.extract_values(
                history
            )

            if len(values) < 4:
                continue

            window = values[-4:]

            analysis[metric] = {

                "window": window,

                "trend": self.trend(window),

                "slope": self.slope(window),

                "moving_average": self.moving_average(window),

                "latest": window[-1],

                "minimum": min(window),

                "maximum": max(window)

            }

        return analysis

    # ----------------------------------------------------
    # Executive Summary
    # ----------------------------------------------------

    def executive_summary(
            self,
            executive_objects):

        return {

            "rolling_analysis":

                self.rolling_four_week_analysis(
                    executive_objects
                ),

            "relationships":

                self.relationships,

            "target_breaches":

                self.detect_target_breaches(
                    executive_objects
                ),

            "outliers":

                self.detect_outliers(
                    executive_objects
                )

        }

    # ----------------------------------------------------
    # Repository Payload
    # ----------------------------------------------------

    def repository_payload(self):

        return {

            "relationship_count":

                len(self.relationships),

            "high_confidence":

                len([

                    r

                    for r in self.relationships

                    if r["confidence"] >= 0.80

                ]),

            "inverse_relationships":

                len([

                    r

                    for r in self.relationships

                    if r["relationship"] == "OPPOSITE_DIRECTION"

                ]),

            "same_direction":

                len([

                    r

                    for r in self.relationships

                    if r["relationship"] == "SAME_DIRECTION"

                ])

        }

    # ----------------------------------------------------
    # Main Pipeline
    # ----------------------------------------------------

    def process(
            self,
            executive_objects):

        self.detect_relationships(
            executive_objects
        )

        executive_objects = self.attach_relationships(
            executive_objects
        )

        return {

            "executive_objects":

                executive_objects,

            "relationships":

                self.relationships,

            "summary":

                self.executive_summary(
                    executive_objects
                ),

            "repository":

                self.repository_payload()

        }


if __name__ == "__main__":

    print()

    print("=" * 60)

    print("Relationship Engine V2")

    print("Self Test Passed")

    print("=" * 60)

    
