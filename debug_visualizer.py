from PIL import ImageDraw


class DebugVisualizer:

    def draw_bar_boxes(self, image, centers, heights, x_axis):

        output = image.copy()

        draw = ImageDraw.Draw(output)

        for center, height in zip(centers, heights):

            top = int(x_axis - height)
            bottom = int(x_axis)

            # Draw a vertical green line
            draw.line(
                [
                    (int(center), top),
                    (int(center), bottom)
                ],
                fill="lime",
                width=3
            )

            # Draw a small green dot at the top
            draw.ellipse(
                [
                    (int(center) - 3, top - 3),
                    (int(center) + 3, top + 3)
                ],
                fill="lime"
            )

            # Draw a small green dot at the bottom
            draw.ellipse(
                [
                    (int(center) - 3, bottom - 3),
                    (int(center) + 3, bottom + 3)
                ],
                fill="lime"
            )

        return output
