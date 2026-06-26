import cv2
import numpy as np


class BarExtractor:

    def detect_bars(self, pil_image):

        image = cv2.cvtColor(
            np.array(pil_image),
            cv2.COLOR_RGB2BGR
        )

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, thresh = cv2.threshold(
            gray,
            240,
            255,
            cv2.THRESH_BINARY_INV
        )

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        bars = []

        for contour in contours:

            x, y, w, h = cv2.boundingRect(contour)

            if h < 20:
                continue

            if w < 4:
                continue

            if h < w:
                continue

            bars.append({
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })

        bars = sorted(
            bars,
            key=lambda b: b["x"]
        )

        return bars
