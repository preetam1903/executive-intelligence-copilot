import fitz  # PyMuPDF
from PIL import Image
import io
import os
import cv2
import numpy as np


class ChartDetector:

    def __init__(self):

        self.output_folder = "chart_images"

        os.makedirs(self.output_folder, exist_ok=True)

    def convert_pdf_to_images(self, pdf_path):

        doc = fitz.open(pdf_path)

        pages = []

        for page_no in range(len(doc)):

            page = doc.load_page(page_no)

            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

            image = Image.open(io.BytesIO(pix.tobytes("png")))

            pages.append(image)

        return pages

    def detect_chart_regions(self, page_image):

        image = np.array(page_image)

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        charts = []

        for contour in contours:

            x, y, w, h = cv2.boundingRect(contour)

            area = w * h

            if area < 80000:
                continue

            charts.append({

                "bbox": (x, y, w, h),

                "area": area

            })

        charts = sorted(
            charts,
            key=lambda c: (c["bbox"][1], c["bbox"][0])
        )

        return charts
