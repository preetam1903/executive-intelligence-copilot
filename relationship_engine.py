"""
relationship_engine.py

Mission 1
"""

from collections import defaultdict


class RelationshipEngine:

    def __init__(self):

        self.relationships = []

    # --------------------------------------------------------
    # Detect trend
    # --------------------------------------------------------

    def detect_trend(self, values):

        if len(values) < 2:
            return "Unknown"

        if values[-1] > values[0]:
            return "Up"

        if values[-1] < values[0]:
            return "Down"

        return "Flat"

    # --------------------------------------------------------
    # Calculate relationship confidence
    # --------------------------------------------------------

    def confidence(self, metric1, metric2):

        if metric1 == metric2:
            return 1.0

        return 0.80

    # --------------------------------------------------------
    # Compare two metrics
    # --------------------------------------------------------

    def compare_metrics(self,
                        metric1,
                        metric2,
                        values1,
                        values2):

        trend1 = self.detect_trend(values1)

        trend2 = self.detect_trend(values2)

        if trend1 == trend2:

            relationship = "SAME_DIRECTION"

        else:

            relationship = "OPPOSITE_DIRECTION"

        return {

            "source": metric1,

            "target": metric2,

            "relationship": relationship,

            "trend_source": trend1,

            "trend_target": trend2,

            "confidence": self.confidence(metric1,
                                          metric2)

        }

    # --------------------------------------------------------
    # Build weekly metric dictionary
    # --------------------------------------------------------

    def build_metric_dictionary(self,
                                executive_objects):

        metrics = defaultdict(list)

        for obj in executive_objects:

            for obs in obj.observations:

                try:

                    value = float(obs.value)

                except:

                    continue

                metrics[obs.metric].append(value)

        return metrics
        # --------------------------------------------------------
    # Detect relationships between all metrics
    # --------------------------------------------------------

    def detect_relationships(self, executive_objects):

        metrics = self.build_metric_dictionary(
            executive_objects
        )

        metric_names = list(metrics.keys())

        relationships = []

        for i in range(len(metric_names)):

            for j in range(i + 1, len(metric_names)):

                metric1 = metric_names[i]
                metric2 = metric_names[j]

                values1 = metrics[metric1]
                values2 = metrics[metric2]

                if len(values1) < 2 or len(values2) < 2:
                    continue

                relationship = self.compare_metrics(
                    metric1,
                    metric2,
                    values1,
                    values2
                )

                relationships.append(
                    relationship
                )

        self.relationships = relationships

        return relationships

    # --------------------------------------------------------
    # Attach relationships back to Executive Objects
    # --------------------------------------------------------

    def attach_relationships(self,
                             executive_objects):

        for obj in executive_objects:

            obj.relationships = []

            object_metrics = set()

            for obs in obj.observations:
                object_metrics.add(obs.metric)

            for rel in self.relationships:

                if rel["source"] in object_metrics or \
                   rel["target"] in object_metrics:

                    obj.relationships.append(rel)

        return executive_objects

    # --------------------------------------------------------
    # Detect target breaches
    # --------------------------------------------------------

    def detect_target_breaches(
            self,
            executive_objects):

        breaches = []

        for obj in executive_objects:

            for obs in obj.observations:

                try:

                    actual = float(obs.value)
                    target = float(obs.target)

                except:

                    continue

                if actual < target:

                    breaches.append({

                        "metric": obs.metric,

                        "period": obs.period,

                        "actual": actual,

                        "target": target,

                        "status": "Below Target"

                    })

                elif actual > target:

                    breaches.append({

                        "metric": obs.metric,

                        "period": obs.period,

                        "actual": actual,

                        "target": target,

                        "status": "Above Target"

                    })

        return breaches

    # --------------------------------------------------------
    # Detect repeated metrics
    # --------------------------------------------------------

    def repeated_metrics(
            self,
            executive_objects):

        counter = defaultdict(int)

        for obj in executive_objects:

            for obs in obj.observations:

                counter[obs.metric] += 1

        repeated = {}

        for metric, count in counter.items():

            if count > 1:

                repeated[metric] = count

        return repeated

        # --------------------------------------------------------
    # Rolling 4 Week Analysis
    # --------------------------------------------------------

    def rolling_four_week_analysis(self, executive_objects):

        analysis = {}

        metrics = self.build_metric_dictionary(executive_objects)

        for metric, values in metrics.items():

            if len(values) < 4:

                continue

            latest_window = values[-4:]

            trend = self.detect_trend(latest_window)

            average = sum(latest_window) / len(latest_window)

            analysis[metric] = {

                "window": latest_window,

                "average": round(average, 2),

                "trend": trend

            }

        return analysis

    # --------------------------------------------------------
    # Executive Summary
    # --------------------------------------------------------

    def executive_summary(self,
                          executive_objects):

        summary = []

        rolling = self.rolling_four_week_analysis(
            executive_objects
        )

        breaches = self.detect_target_breaches(
            executive_objects
        )

        repeated = self.repeated_metrics(
            executive_objects
        )

        relationships = self.detect_relationships(
            executive_objects
        )

        summary.append({

            "rolling_analysis": rolling

        })

        summary.append({

            "target_breaches": breaches

        })

        summary.append({

            "repeated_metrics": repeated

        })

        summary.append({

            "relationships": relationships

        })

        return summary

    # --------------------------------------------------------
    # Main Processing Pipeline
    # --------------------------------------------------------

    def process(self,
                executive_objects):

        self.detect_relationships(
            executive_objects
        )

        executive_objects = self.attach_relationships(
            executive_objects
        )

        summary = self.executive_summary(
            executive_objects
        )

        return {

            "executive_objects": executive_objects,

            "relationships": self.relationships,

            "summary": summary

        }
