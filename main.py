import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()  # Carga variables del archivo .env

# Se usará la clave de API configurada en el entorno
llm = ChatOpenAI(model="gpt-5", openai_api_key=os.getenv("OPENAI_API_KEY"))

def leer_pdf(ruta):
    from PyPDF2 import PdfReader
    reader = PdfReader(ruta)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto

def leer_docx(ruta):
    from docx import Document  # Esto funciona solo si tienes 'python-docx' instalado
    doc = Document(ruta)
    texto = ""
    for para in doc.paragraphs:
        texto += para.text + "\n"
    return texto

def generar_contenido_unidad(llm, indice, recomendaciones, numero_unidad):
    prompt = (
        f"Como un creador de contenidos experto usa el siguiente índice de curso y las recomendaciones para desarrollar el contenido de la unidad de aprendizaje {numero_unidad}.\n\n"
        f"Índice del curso:\n{indice}\n\n"
        f"Recomendaciones:\n{recomendaciones}\n\n"
        f"Desarrolla los contenidos de la unidad de aprendizaje {numero_unidad} de forma detallada y estructurada."
    )
    respuesta = llm.invoke(prompt)
    return respuesta.content if hasattr(respuesta, "content") else respuesta

def guardar_html(contenido, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"<html><body><pre>{contenido}</pre></body></html>")

def contar_unidades_con_regex(texto):
    # 1. Convert the entire text to lowercase for case-insensitivity
    texto_lower = texto.lower()
    
    # 2. Define the Regular Expression pattern:
    # 'unidad\s+de\s+aprendizaje'
    #   - \s+ matches one or more occurrences of any whitespace character (space, tab, newline, etc.)
    pattern = r'unidad\s+de\s+aprendizaje'
    
    # 3. Find all non-overlapping matches
    matches = re.findall(pattern, texto_lower)
    
    # 4. Return the count of matches
    return len(matches)

if __name__ == "__main__":
    ruta_indice = "data\\IFCT0050.pdf"
    ruta_recomendaciones = "data\\guia_elaboracion_online_EEFF.docx"

    indice = leer_pdf(ruta_indice)
    recomendaciones = leer_docx(ruta_recomendaciones)

    unidades = contar_unidades_con_regex(indice)
    print(f"Se han extraído {unidades} unidades de aprendizaje.")
    curso_completo = ""

    carpeta_resultados = "resultados"
    os.makedirs(carpeta_resultados, exist_ok=True)

    for i in range(1, unidades + 1):
        print(f"Generando contenido para la unidad {i}...")
        contenido_unidad = generar_contenido_unidad(llm, indice, recomendaciones, i)
        curso_completo += f"\n\n--- Unidad {i} ---\n\n{contenido_unidad}\n"
        ruta_html = os.path.join(carpeta_resultados, f"unidad{i}.html")
        guardar_html(contenido_unidad, ruta_html)
        # Si quieres guardar PDF, añade aquí la función guardar_pdf

    # Opcional: guardar el curso completo en un solo archivo
    ruta_html_curso = os.path.join(carpeta_resultados, "curso_completo.html")
    guardar_html(curso_completo, ruta_html_curso)
