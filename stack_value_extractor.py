from PIL import Image, ImageDraw


class StackValueExtractor:

    def __init__(self, metadata):

        self.metadata = metadata

    # ----------------------------------------------------------
    # Compute center X position of every bar
    # ----------------------------------------------------------

    def compute_bar_centers(self):

        left = self.metadata["plot_area"]["left"]
        right = self.metadata["plot_area"]["right"]

        total_bars = self.metadata["bars"]

        distance = right - left

        spacing = distance / (total_bars - 1)

        for i in range(total_bars):

            center = round(left + i * spacing)

            centers.append(center)

        return centers

    # ----------------------------------------------------------
    # Draw sampling lines
    # ----------------------------------------------------------

    def draw_sampling_lines(self, chart_image):

        image = chart_image.copy()

        draw = ImageDraw.Draw(image)

        centers = self.compute_bar_centers()

        top = self.metadata["plot_area"]["top"]
        bottom = self.metadata["plot_area"]["bottom"]

        for center in centers:

            for offset in [-2, -1, 0, 1, 2]:

                x = center + offset

                draw.line(

                    [
                        (x, top),
                        (x, bottom)
                    ],

                    fill=(0, 255, 0),

                    width=1

                )

        return image

        # ----------------------------------------------------------
    # Sample one bar
    # ----------------------------------------------------------

    def sample_bar(self, image, center_x):

        top = self.metadata["plot_area"]["top"]
        bottom = self.metadata["plot_area"]["bottom"]

        pixels = []

        for y in range(top, bottom):

            row = []

            for dx in [-2, -1, 0, 1, 2]:

                x = center_x + dx

                row.append(
                    image.getpixel((x, y))
                )

            pixels.append(row)

        return pixels
