import numpy as np


class StackedBarExtractor:

    def find_bar_edges(self, center_x):

        """
        Use a fixed-width window around the expected bar center.
        This prevents the detector from merging adjacent bars.
        """

        BAR_HALF_WIDTH = 6

        left = max(0, center_x - BAR_HALF_WIDTH)
        right = center_x + BAR_HALF_WIDTH

        return left, right

    def measure_total_height(self, pil_image, center_x, x_axis):

        img = np.array(pil_image)

        height, width = img.shape[:2]

        left, right = self.find_bar_edges(center_x)

        right = min(right, width - 1)

        top = x_axis

        found = False

        # Scan upward from X-axis
        for y in range(x_axis, 0, -1):

            coloured_pixels = 0

            for x in range(left, right + 1):

                r, g, b = img[y, x]

                # Ignore near-white pixels
                if not (r > 240 and g > 240 and b > 240):
                    coloured_pixels += 1

            # At least half the pixels in this row must belong to the bar
            if coloured_pixels >= ((right - left + 1) * 0.5):

                top = y
                found = True

            elif found:
                break

        return {
            "left": left,
            "right": right,
            "top": top,
            "height": x_axis - top
        }
