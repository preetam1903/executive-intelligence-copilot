import numpy as np


class StackedBarExtractor:

    def measure_total_height(self, pil_image, center_x, x_axis):

        img = np.array(pil_image)

        h = img.shape[0]

        top = x_axis

        found = False

        for y in range(x_axis, 0, -1):

            pixel = img[y, center_x]

            r, g, b = pixel

            # Ignore white background

            if r > 235 and g > 235 and b > 235:
                continue

            top = y

            found = True

        if not found:
            return 0

        return x_axis - top
