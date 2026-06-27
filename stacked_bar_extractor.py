import numpy as np


class StackedBarExtractor:

    def find_bar_edges(self, img, center_x, x_axis):

        height, width = img.shape[:2]

        # -------- LEFT EDGE --------

        left = center_x

        while left > 5:

            dark = 0

            for y in range(max(0, x_axis - 80), x_axis):

                r, g, b = img[y, left]

                if not (r > 240 and g > 240 and b > 240):
                    dark += 1

            if dark < 3:
                break

            left -= 1

        # -------- RIGHT EDGE --------

        right = center_x

        while right < width - 5:

            dark = 0

            for y in range(max(0, x_axis - 80), x_axis):

                r, g, b = img[y, right]

                if not (r > 240 and g > 240 and b > 240):
                    dark += 1

            if dark < 3:
                break

            right += 1

        return left, right

    def measure_total_height(self, pil_image, center_x, x_axis):

        img = np.array(pil_image)

        left, right = self.find_bar_edges(
            img,
            center_x,
            x_axis
        )

        top = x_axis

        for y in range(x_axis, 0, -1):

            coloured = 0

            for x in range(left, right):

                r, g, b = img[y, x]

                if not (r > 240 and g > 240 and b > 240):
                    coloured += 1

            if coloured > (right - left) * 0.50:

                top = y

            elif top != x_axis:

                break

        return {

            "left": left,

            "right": right,

            "height": x_axis - top

        }
