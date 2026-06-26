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

        return page_image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )
    def crop_plot_area(self, chart_image):

        width, height = chart_image.size

        left = int(width * PLOT_CROP["left"])

        right = int(width * PLOT_CROP["right"])

        top = int(height * PLOT_CROP["top"])

        bottom = int(height * PLOT_CROP["bottom"])

        return chart_image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )
