from PIL import Image, ImageDraw
import colorsys

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
        centers=[]

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

        # ----------------------------------------------------------
    # RGB -> Color Name
    # ----------------------------------------------------------

    def classify_pixel(self, rgb):

        r, g, b = rgb

        h, s, v = colorsys.rgb_to_hsv(
            r / 255.0,
            g / 255.0,
            b / 255.0
        )

        h = h * 360
        s = s * 100
        v = v * 100

        # White / Background
        if s < 15 and v > 90:
            return "WHITE"

        # Red
        if h < 15 or h > 345:
            return "RED"

        # Orange
        if 15 <= h <= 50:
            return "ORANGE"

        # Green
        if 70 <= h <= 170:
            return "GREEN"

        # Blue
        if 180 <= h <= 260:
            return "BLUE"

        return "OTHER"

        # ----------------------------------------------------------
    # Classify one sampled bar
    # ----------------------------------------------------------

    def classify_bar(self, sample):

        results = []

        for row in sample:

            votes = []

            for pixel in row:

                votes.append(
                    self.classify_pixel(pixel)
                )

            counts = {}

            for vote in votes:

                counts[vote] = counts.get(vote, 0) + 1

            majority = max(
                counts,
                key=counts.get
            )

            results.append(majority)

        return results
