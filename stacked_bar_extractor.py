import numpy as np


class StackedBarExtractor:

    def measure_total_height(self, pil_image, center_x, x_axis):

        img = np.array(pil_image)

        height, width = img.shape[:2]

        half_width = 6          # examine 13 pixels around the center
        min_dark_pixels = 5     # row must contain at least this many coloured pixels

        top = None

        for y in range(x_axis, 0, -1):

            dark_count = 0

            for x in range(
                max(0, center_x - half_width),
                min(width, center_x + half_width + 1)
            ):

                r, g, b = img[y, x]

                # Ignore white / near-white background
                if not (r > 240 and g > 240 and b > 240):
                    dark_count += 1

            if dark_count >= min_dark_pixels:
                top = y
            elif top is not None:
                # We have left the bar
                break

        if top is None:
            return 0

        return x_axis - top
