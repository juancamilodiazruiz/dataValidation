import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    """
    Extrae el texto de todas las páginas de un archivo PDF.
    :param pdf_path: Ruta al archivo PDF.
    :return: Texto extraído.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error al leer el PDF con PyMuPDF: {e}")
        return None

def extract_images_from_pdf(pdf_path, output_folder="extracted_images"):
    """
    Extrae imágenes de un archivo PDF y las guarda en una carpeta.
    :param pdf_path: Ruta al archivo PDF.
    :param output_folder: Carpeta donde se guardarán las imágenes.
    :return: Lista de rutas de las imágenes extraídas.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        doc = fitz.open(pdf_path)
        image_paths = []

        for i, page in enumerate(doc):
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_format = base_image["ext"]

                image_filename = f"{output_folder}/page_{i+1}_img_{img_index+1}.{image_format}"
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_bytes)

                image_paths.append(image_filename)

        return image_paths
    except Exception as e:
        print(f"Error al extraer imágenes del PDF con PyMuPDF: {e}")
        return []
