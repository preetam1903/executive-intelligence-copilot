import numpy as np


class PlotAnalyzer:

    def analyze(self, pil_image):

        img = np.array(pil_image)

        gray = img.mean(axis=2)

        h, w = gray.shape

        # -----------------------------
        # Find Bottom Axis
        # -----------------------------

        row_scores = []

        for y in range(h):

            dark = np.sum(gray[y] < 150)

            row_scores.append(dark)

        baseline = int(np.argmax(row_scores))

        # -----------------------------
        # Find Left Axis
        # -----------------------------

        col_scores = []

        for x in range(w):

            dark = np.sum(gray[:, x] < 150)

            col_scores.append(dark)

        left_axis = int(np.argmax(col_scores))

        plot = {

            "left": left_axis,

            "right": w - 1,

            "top": 0,

            "bottom": baseline,

            "width": (w - 1) - left_axis,

            "height": baseline

        }

        # -----------------------------
        # Refine X Axis
        # -----------------------------

        x_axis = baseline

        for y in range(baseline, max(baseline - 40, 0), -1):

            dark = np.sum(gray[y] < 120)

            if dark > plot["width"] * 0.60:

                x_axis = y

                break

        plot["x_axis"] = x_axis

        return plot
    

    def compute_expected_bar_positions(self, plot, number_of_labels):
        if number_of_labels <= 0:
            return []
        left = plot["left"]
        right = plot["right"]

        width = right - left

        spacing = width / number_of_labels

        centers = []

        for i in range(number_of_labels):

            center = int(left + (i + 0.5) * spacing)

            centers.append(center)

        return centers
