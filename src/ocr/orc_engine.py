import pytesseract
import cv2
import numpy as np
from src.config import TESSERACT_CMD

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text_from_image(image):
    """
    Aplica OCR a una imagen para extraer texto.
    :param image: Imagen PIL extraída del PDF.
    :return: Texto extraído.
    """
    # Convertir imagen PIL a OpenCV
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Binarización para mejorar el OCR
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    # Aplicar OCR
    text = pytesseract.image_to_string(binary_image, lang='eng')  # Cambiar 'eng' según idioma
    return text
