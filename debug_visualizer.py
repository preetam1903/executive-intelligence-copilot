from PIL import ImageDraw


class DebugVisualizer:

    def draw_bar_boxes(self, image, centers, heights, x_axis):

        output = image.copy()

        draw = ImageDraw.Draw(output)

        BAR_HALF_WIDTH = 6

        for center, height in zip(centers, heights):

            left = center - BAR_HALF_WIDTH
            right = center + BAR_HALF_WIDTH

            top = x_axis - height
            bottom = x_axis

            draw.rectangle(
                [left, top, right, bottom],
                outline="lime",
                width=2
            )

        return output
