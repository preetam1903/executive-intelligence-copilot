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

    def detect_bar_centers(self, pil_image, plot):

        img = np.array(pil_image)

        gray = img.mean(axis=2)

        left = plot["left"]

        right = plot["right"]

        bottom = plot["x_axis"]

        scan_height = 60

        histogram = []

        for x in range(left, right):

            dark = 0

            for y in range(max(bottom - scan_height, 0), bottom):

                if gray[y, x] < 170:

                    dark += 1

            histogram.append(dark)

        centers = []

        inside = False

        start = 0

        for i, value in enumerate(histogram):

            if value > 8:

                if not inside:

                    start = i

                    inside = True

            else:

                if inside:

                    end = i

                    center = left + (start + end) // 2

                    centers.append(center)

                    inside = False

        # Handle final bar reaching image edge
        if inside:

            end = len(histogram) - 1

            center = left + (start + end) // 2

            centers.append(center)

        return centers
