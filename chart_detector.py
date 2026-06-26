import fitz  # PyMuPDF
from PIL import Image
import io
import os



class ChartDetector:

    def __init__(self):

        self.output_folder = "chart_images"

        os.makedirs(self.output_folder, exist_ok=True)

    def convert_pdf_to_images(self, pdf_path):

        pdf_bytes = pdf_path.read()

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        pages = []

        for page_no in range(len(doc)):

            page = doc.load_page(page_no)

            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

            image = Image.open(io.BytesIO(pix.tobytes("png")))

            pages.append(image)

        return pages

    
    def detect_chart_regions(self, page_image):

        """
        Placeholder for GPT Vision Layout Detection.
        Returns detected chart regions.
        """

        return []
