import pandas as pd
from src.pdf_processing.pdf_data_extractor import extract_data_from_pdf
from src.pdf_processing.pdf_declaration_extractor import extract_names_and_ids
from src.pdf_processing.pdf_equivalents_extractor import extract_equivalents_data
#from src.pdf_processing.pdf_rut_extractor import extract_rut_data_reordered
from src.pdf_processing.pdf_rut_v2_extractor import extract_rut_data_reordered
from src.pdf_processing.pdf_vinculation_extractor import extract_vinculation_data

def compare_pdf_data(pdf_path_genesis, pdf_path_declaracion, pdf_path_equivalentes, pdf_path_rut, pdf_path_vinculacion):
    """
    Compara los datos extraídos de los cinco archivos PDF página por página,
    asegurando que todas las páginas sean consideradas en la comparación.
    """
    # Extraer datos de los cinco documentos
    extracted_data_genesis = extract_data_from_pdf(pdf_path_genesis)
    extracted_data_declaration = extract_names_and_ids(pdf_path_declaracion)
    extracted_data_equivalents = extract_equivalents_data(pdf_path_equivalentes)
    extracted_data_rut = extract_rut_data_reordered(pdf_path_rut)
    extracted_data_vinculacion = extract_vinculation_data(pdf_path_vinculacion)

    # Convertir los datos en DataFrames
    df_genesis = pd.DataFrame(extracted_data_genesis)
    df_declaration = pd.DataFrame(extracted_data_declaration)
    df_equivalents = pd.DataFrame(extracted_data_equivalents)
    df_rut = pd.DataFrame(extracted_data_rut)
    df_vinculacion = pd.DataFrame(extracted_data_vinculacion)

    # Verificar si "Página" existe antes de convertir a int
    for df in [df_genesis, df_declaration, df_equivalents, df_rut, df_vinculacion]:
        if "Página" in df.columns:
            df["Página"] = df["Página"].astype(int)
            
    # Verificar las columnas antes de la fusión
    #print("Columnas en df_vinculacion antes del merge:", df_vinculacion.columns)

    # Renombrar columnas para evitar conflictos
    df_equivalents.rename(columns={"Nombre": "Nombre_Equivalente", "Cédula": "Cédula_Equivalente"}, inplace=True)
    df_rut.rename(columns={"Nombre": "Nombre_RUT", "Cédula": "Cédula_RUT"}, inplace=True)
    #df_vinculacion.rename(columns={"Nombre": "Nombre_Vinculacion", "Apellidos": "Apellidos_Vinculacion", "Cédula": "Cédula_Vinculacion"}, inplace=True)
    df_vinculacion.rename(columns={"Nombre Completo": "Nombre_Vinculacion", "Cedula_Vinculcion": "Cédula_Vinculacion"}, inplace=True)

    
    # Fusionar los DataFrames en base al número de página
    df_comparison = pd.merge(df_genesis, df_declaration, on="Página", how="outer", suffixes=("_Génesis", "_Declaración"))
    df_comparison = pd.merge(df_comparison, df_equivalents, on="Página", how="outer")
    df_comparison = pd.merge(df_comparison, df_rut, on="Página", how="outer")
    df_comparison = pd.merge(df_comparison, df_vinculacion, on="Página", how="outer")

    # Llenar valores faltantes con "No encontrado" para evitar errores en la comparación
    df_comparison.fillna("No encontrado", inplace=True)

    # Comparar si los nombres y cédulas coinciden en todos los documentos
    df_comparison["Coincidencia Nombre"] = (
        (df_comparison["Nombre_Génesis"] == df_comparison["Nombre_Declaración"]) & 
        (df_comparison["Nombre_Génesis"] == df_comparison["Nombre_Equivalente"]) & 
        (df_comparison["Nombre_Génesis"] == df_comparison["Nombre_RUT"]) &
        (df_comparison["Nombre_Génesis"] == df_comparison["Nombre_Vinculacion"])
    )

    df_comparison["Coincidencia Cédula"] = (
        (df_comparison["Cédula_Génesis"] == df_comparison["Cédula_Declaración"]) & 
        (df_comparison["Cédula_Génesis"] == df_comparison["Cédula_Equivalente"]) & 
        (df_comparison["Cédula_Génesis"] == df_comparison["Cédula_RUT"]) &
        (df_comparison["Cédula_Génesis"] == df_comparison["Cédula_Vinculacion"])
    )

    return df_comparison
