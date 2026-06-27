import fitz
from PIL import Image
import io
import os
PLOT_CROP = {

    "left": 0.13,

    "top": 0.22,

    "right": 0.98,

    "bottom": 0.92

}

class ChartDetector:

    def __init__(self):

        self.output_folder = "chart_images"

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    def convert_pdf_to_images(self, uploaded_file):

        pdf_bytes = uploaded_file.read()

        doc = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages = []

        for page_no in range(len(doc)):

            page = doc.load_page(page_no)

            pix = page.get_pixmap(
                matrix=fitz.Matrix(3, 3)
            )

            image = Image.open(
                io.BytesIO(
                    pix.tobytes("png")
                )
            )

            pages.append(image)

        return pages

    def crop_chart(self, page_image, bbox):

        left, top, right, bottom = bbox

        width = page_image.width
        height = page_image.height

    # Because PDF is rendered at 3x,
    # scale the GPT coordinates.

        scale_x = page_image.width / 1000
        scale_y = page_image.height / 1000

        left *= scale_x
        right *= scale_x

        top *= scale_y
        bottom *= scale_y

        # Different padding for each side
        left_padding = 20
        top_padding = 20
        right_padding = 10
        bottom_padding = 80

        left = max(0, left - left_padding)
        top = max(0, top - top_padding)

        right = min(width, right + right_padding)

# Keep the crop tighter vertically
        bottom = min(height, bottom - bottom_padding)

        return page_image.crop(
            (
                int(left),
                int(top),
                int(right),
                int(bottom)
            )
        )
