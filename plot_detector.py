from PIL import Image
import numpy as np


class PlotDetector:

    def detect_plot_area(self, chart_image):

        img = np.array(chart_image)

        gray = img.mean(axis=2)

        height, width = gray.shape

        left = width
        right = 0
        top = height
        bottom = 0

        # Detect non-white pixels
        threshold = 245

        for y in range(height):
            for x in range(width):

                if gray[y, x] < threshold:

                    left = min(left, x)
                    right = max(right, x)
                    top = min(top, y)
                    bottom = max(bottom, y)

        padding = 10

        left = max(0, left - padding)
        top = max(0, top - padding)
        right = min(width, right + padding)
        bottom = min(height, bottom + padding)

        return chart_image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )
