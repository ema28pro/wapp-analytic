import streamlit as st
import pdfplumber

st.set_page_config(page_title="Ejemplo File Uploader", page_icon="📁", layout="centered")

st.title("Subir Archivo")
# st.write("Usa `st.file_uploader` para permitir al usuario subir archivos.")

st.subheader("Sube tu material")

archivo = st.file_uploader(
    label="Selecciona un archivo",
    type=['pdf', 'md', 'txt'],
    help="PDF, Markdown o TXT"
)

# with open(f"uploads/{archivo.name}", "wb") as f:
#     f.write(archivo.getbuffer())

# Configuración de límites y tipos permitidos
TAMANO_MAXIMO_MB = 10
TAMANO_MAXIMO_BYTES = TAMANO_MAXIMO_MB * 1024 * 1024
EXTENSIONES_PERMITIDAS = (".pdf", ".md", ".txt")

if archivo:
    nombre = archivo.name.lower()
    
    # 1. Validación de tamaño
    if archivo.size > TAMANO_MAXIMO_BYTES:
        st.error(f"El archivo supera el tamaño máximo permitido de {TAMANO_MAXIMO_MB} MB.")
        st.stop()
        
    # 2. Validación de extensión permitida
    if not nombre.endswith(EXTENSIONES_PERMITIDAS):
        st.error(f"Tipo de archivo no permitido. Solo se aceptan: {', '.join(EXTENSIONES_PERMITIDAS)}")
        st.stop()

    # 3. Validación de Magic Bytes para PDF (evitar ejecutables o archivos falsificados)
    contenido_bytes = archivo.getvalue()
    if nombre.endswith(".pdf"):
        if not contenido_bytes.startswith(b"%PDF-"):
            st.error("Archivo inválido: tiene extensión .pdf pero no contiene una cabecera PDF válida.")
            st.stop()
            
    st.success(f"Archivo válido: **{archivo.name}** ({archivo.size / 1024:.1f} KB)")

    # 4. Procesamiento según el tipo
    if nombre.endswith(".pdf"):
        try:
            with pdfplumber.open(archivo) as pdf:
                for i, page in enumerate(pdf.pages):
                    texto = page.extract_text()
                    st.write(f"**Página {i + 1}:**")
                    st.write(texto if texto else "_[Página sin texto detectable]_")
        except Exception as e:
            st.error(f"Error al leer el PDF: {e}")

    elif nombre.endswith(".md"):
        try:
            texto = contenido_bytes.decode("utf-8")
            st.markdown(texto)
        except UnicodeDecodeError:
            st.error("El archivo Markdown no tiene una codificación UTF-8 válida.")

    elif nombre.endswith(".txt"):
        try:
            texto = contenido_bytes.decode("utf-8")
            st.text_area("Contenido del archivo:", texto, height=250)
        except UnicodeDecodeError:
            st.error("El archivo de texto no tiene una codificación UTF-8 válida.")

archivos_multiples = st.file_uploader(
    "Selecciona varios archivos",
    accept_multiple_files=True, type=['pdf', 'md', 'txt'],
    help="PDF, Markdown o TXT"
)

if archivos_multiples:
    st.write(f"Has subido {len(archivos_multiples)} archivos:")
    for f in archivos_multiples:
        st.write(f"- 📄 **{f.name}** ({f.size} bytes)")
