import numpy as np


class PlotAnalyzer:

    def analyze(self, pil_image):

        img = np.array(pil_image)

        gray = img.mean(axis=2)

        h, w = gray.shape

        # ---------- Find Bottom Axis ----------

        row_scores = []

        for y in range(h):

            dark = np.sum(gray[y] < 150)

            row_scores.append(dark)

        baseline = int(np.argmax(row_scores))

        # ---------- Find Left Axis ----------

        col_scores = []

        for x in range(w):

            dark = np.sum(gray[:, x] < 150)

            col_scores.append(dark)

        left_axis = int(np.argmax(col_scores))

        # ---------- Plot Area ----------

        plot = {

            "left": left_axis,

            "right": w - 1,

            "top": 0,

            "bottom": baseline,

            "width": w - left_axis,

            "height": baseline

        }

                # -----------------------------
        # Find X Axis
        # -----------------------------

        x_axis = baseline

        for y in range(baseline, baseline - 40, -1):

            if y < 0:
                break

            dark = np.sum(gray[y] < 120)

            if dark > plot["width"] * 0.60:

                x_axis = y

                break

        plot["x_axis"] = x_axis

        return plot
