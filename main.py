import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()  # Carga variables del archivo .env

# Se usará la clave de API configurada en el entorno
llm = ChatOpenAI(model="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"))

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

def generar_contenido_unidad1(llm, indice, recomendaciones):
    prompt = (
        f"Como un creador de contenidos experto usa el siguiente índice de curso y las recomendaciones para desarrollar el contenido de la unidad de aprendizaje 1.\n\n"
        f"Índice del curso:\n{indice}\n\n"
        f"Recomendaciones:\n{recomendaciones}\n\n"
        f"Desarrolla los contenidos de la unidad de aprendizaje 1 de forma detallada y estructurada."
    )
    respuesta = llm.invoke(prompt)
    return respuesta.content if hasattr(respuesta, "content") else respuesta

def guardar_html(contenido, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"<html><body><pre>{contenido}</pre></body></html>")

if __name__ == "__main__":
    ruta_indice = "data\\IFCT0050.pdf"  # Cambia por la ruta real de tu índice
    ruta_recomendaciones = "data\\guia_elaboracion_online_EEFF.docx"  # Cambia por la ruta real de tus recomendaciones

    indice = leer_pdf(ruta_indice)
    recomendaciones = leer_docx(ruta_recomendaciones)

    contenido_unidad1 = generar_contenido_unidad1(llm, indice, recomendaciones)
    print("Unidad de aprendizaje 1 generada:\n")
    print(contenido_unidad1)

    # Guardar resultados en HTML y PDF
    carpeta_resultados = "resultados"
    os.makedirs(carpeta_resultados, exist_ok=True)
    ruta_html = os.path.join(carpeta_resultados, "unidad1.html")
    ruta_pdf = os.path.join(carpeta_resultados, "unidad1.pdf")
    guardar_html(contenido_unidad1, ruta_html)
