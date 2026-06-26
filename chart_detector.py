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

        # Expand the detected box
        padding_x = 40
        padding_y = 40

        left = max(0, left - padding_x)
        top = max(0, top - padding_y)

        right = min(width, right + padding_x)
        bottom = min(height, bottom + padding_y)

        return page_image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )
    
