import numpy as np


class BarExtractor:

    def detect_bars(self, pil_image):

        img = np.array(pil_image)

        height, width = img.shape[:2]

        gray = img.mean(axis=2)

        threshold = 235

        bars = []

        in_bar = False

        start_x = 0

        for x in range(width):

            column = gray[:, x]

            dark_pixels = np.sum(column < threshold)

            if dark_pixels > 20:

                if not in_bar:

                    start_x = x

                    in_bar = True

            else:

                if in_bar:

                    end_x = x

                    center = (start_x + end_x) // 2

                    top = height

                    bottom = 0

                    for xx in range(start_x, end_x):

                        ys = np.where(gray[:, xx] < threshold)[0]

                        if len(ys) == 0:
                            continue

                        top = min(top, ys.min())

                        bottom = max(bottom, ys.max())

                    if bottom - top > 20:

                        bars.append({

                            "center_x": center,

                            "left": start_x,

                            "right": end_x,

                            "top": int(top),

                            "bottom": int(bottom),

                            "height_pixels": int(bottom - top)

                        })

                    in_bar = False

        return bars
