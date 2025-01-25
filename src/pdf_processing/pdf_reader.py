from pdf2image import convert_from_path

def extract_images_from_pdf(pdf_path):
    """
    Convierte las páginas de un PDF a imágenes.
    :param pdf_path: Ruta al archivo PDF.
    :return: Lista de imágenes extraídas.
    """
    images = convert_from_path(pdf_path)
    return images
