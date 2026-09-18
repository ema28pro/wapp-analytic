import streamlit as st

st.set_page_config(page_title="Solo TXT", page_icon="📝", layout="centered")

st.title("📝 Subir Archivo TXT")
st.write("Esta página únicamente permite cargar y previsualizar archivos de texto plano (`.txt`).")

# Límite de tamaño: 5 MB
TAMANO_MAXIMO_MB = 5
TAMANO_MAXIMO_BYTES = TAMANO_MAXIMO_MB * 1024 * 1024

archivo_txt = st.file_uploader(
    label="Selecciona un archivo TXT",
    type=["txt"],
    help=f"Solo archivos de texto plano (.txt). Máximo {TAMANO_MAXIMO_MB} MB."
)

if archivo_txt is not None:
    # 1. Validación estricta de extensión
    if not archivo_txt.name.lower().endswith(".txt"):
        st.error("Tipo de archivo no permitido. Solo se aceptan archivos .txt")
        st.stop()

    # 2. Validación de tamaño
    if archivo_txt.size > TAMANO_MAXIMO_BYTES:
        st.error(f"El archivo supera el tamaño máximo permitido de {TAMANO_MAXIMO_MB} MB.")
        st.stop()

    # 3. Lectura y decodificación
    try:
        contenido_bytes = archivo_txt.getvalue()
        texto = contenido_bytes.decode("utf-8")
        
        st.success(f"Archivo cargado exitosamente: **{archivo_txt.name}** ({archivo_txt.size / 1024:.1f} KB)")
        
        # Métricas rápidas del texto
        lineas = texto.splitlines()
        palabras = len(texto.split())
        caracteres = len(texto)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Líneas", len(lineas))
        col2.metric("Palabras", palabras)
        col3.metric("Caracteres", caracteres)
        
        st.subheader("Contenido:")
        st.text_area(
            label="Visualizador de texto",
            value=texto,
            height=350,
            disabled=True
        )

    except UnicodeDecodeError:
        st.error("El archivo no tiene una codificación UTF-8 válida o es un archivo binario.")
