"""
xray_engine.py

AI X-Ray Engine
Version 1
"""

from datetime import datetime


class XRayEngine:

    def __init__(self):

        self.pipeline = []

    # ----------------------------------------------------
    # Reset
    # ----------------------------------------------------

    def reset(self):

        self.pipeline = []

    # ----------------------------------------------------
    # Start Stage
    # ----------------------------------------------------

    def start_stage(
            self,
            stage):

        item = {

            "stage": stage,

            "start_time": datetime.now(),

            "end_time": None,

            "duration_ms": None,

            "status": "Running",

            "metrics": {},

            "notes": []

        }

        self.pipeline.append(item)

        return len(self.pipeline) - 1

    # ----------------------------------------------------
    # Finish Stage
    # ----------------------------------------------------

    def finish_stage(
            self,
            stage_id):

        stage = self.pipeline[stage_id]

        stage["end_time"] = datetime.now()

        duration = (

            stage["end_time"] -

            stage["start_time"]

        ).total_seconds()

        stage["duration_ms"] = round(

            duration * 1000,

            2

        )

        stage["status"] = "Completed"

    # ----------------------------------------------------
    # Add Metric
    # ----------------------------------------------------

    def add_metric(
            self,
            stage_id,
            key,
            value):

        self.pipeline[stage_id]["metrics"][key] = value

    # ----------------------------------------------------
    # Add Note
    # ----------------------------------------------------

    def add_note(
            self,
            stage_id,
            note):

        self.pipeline[stage_id]["notes"].append(note)


        # ----------------------------------------------------
    # Stage Failed
    # ----------------------------------------------------

    def fail_stage(
            self,
            stage_id,
            error):

        stage = self.pipeline[stage_id]

        stage["end_time"] = datetime.now()

        duration = (

            stage["end_time"] -

            stage["start_time"]

        ).total_seconds()

        stage["duration_ms"] = round(

            duration * 1000,

            2

        )

        stage["status"] = "Failed"

        stage["error"] = str(error)

    # ----------------------------------------------------
    # Get Pipeline
    # ----------------------------------------------------

    def get_pipeline(self):

        return self.pipeline

    # ----------------------------------------------------
    # Pipeline Summary
    # ----------------------------------------------------

    def summary(self):

        total_time = 0

        completed = 0

        failed = 0

        running = 0

        for stage in self.pipeline:

            total_time += stage.get(
                "duration_ms",
                0
            ) or 0

            if stage["status"] == "Completed":
                completed += 1

            elif stage["status"] == "Failed":
                failed += 1

            else:
                running += 1

        return {

            "total_stages": len(
                self.pipeline
            ),

            "completed": completed,

            "failed": failed,

            "running": running,

            "total_time_ms": round(
                total_time,
                2
            )

        }

    # ----------------------------------------------------
    # Export
    # ----------------------------------------------------

    def export(self):

        return {

            "summary":

                self.summary(),

            "pipeline":

                self.pipeline

        }


if __name__ == "__main__":

    xray = XRayEngine()

    stage = xray.start_stage(
        "Vision AI"
    )

    xray.add_metric(
        stage,
        "Pages",
        12
    )

    xray.add_metric(
        stage,
        "Charts",
        8
    )

    xray.add_note(
        stage,
        "Vision extraction completed successfully."
    )

    xray.finish_stage(
        stage
    )

    print(

        xray.export()

    )
