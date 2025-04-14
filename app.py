import streamlit as st
import pandas as pd
import datetime
from openai import OpenAI

st.set_page_config(page_title="LinkedInviter Web", layout="centered")
st.title("🚀 LinkedInviter Web")

st.markdown("""
Pega las URLs de LinkedIn (una por línea), completa los datos, y generaremos mensajes automáticos con CTA personalizado.
""")

# Inputs clave
api_key = st.text_input("🔑 Clave API de OpenAI", type="password")
nombre_usuario = st.text_input("👤 Tu nombre")
cargo = st.text_input("💼 Cargo")
ciudad = st.text_input("🌐 Ciudad", value="bogota")
empresa = st.text_input("🏢 Empresa")
tipo_conexion = st.selectbox("🔗 Conexión", ["Todos", "1er grado", "2do grado", "3er grado"])
limite_diario = st.number_input("📊 Límite diario", min_value=1, max_value=100, value=20)
tipo_cta = st.selectbox("🔗 Tipo de CTA", ["WhatsApp", "URL personalizada"])
cta_url = st.text_input("🔗 Enlace de CTA", placeholder="https://wa.me/... o https://tulanding.com")

urls_input = st.text_area("🔗 Perfiles de LinkedIn (una URL por línea)")

# Preparar cliente de OpenAI (v1.0+)
def generar_mensaje(nombre, cargo, ciudad, tipo="inv"):
    client = OpenAI(api_key=api_key)
    prompt = f"""
Eres {nombre}, {cargo} ubicado en {ciudad}. Vas a conectar con un perfil en LinkedIn como parte de una estrategia de networking y prospección comercial.
Genera un mensaje corto y profesional de {tipo}itación de conexión, sin emojis, directo, amable, y agrega al final un llamado a la acción: "Si deseas saber más, escribe aquí {cta_url}".
"""
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content

# Botón para generar mensajes
df = pd.DataFrame(columns=["Perfil", "Mensaje", "Fecha"])

if st.button("✉️ Generar Mensajes"):
    if not api_key:
        st.error("Debes ingresar tu clave API de OpenAI.")
    else:
        perfiles = [url.strip() for url in urls_input.split("\n") if url.strip()][:limite_diario]
        mensajes_generados = []

        with st.spinner("Generando mensajes..."):
            for url in perfiles:
                try:
                    msg = generar_mensaje(nombre_usuario, cargo, ciudad)
                    mensajes_generados.append((url, msg, datetime.date.today()))
                    st.success(f"✅ Generado para {url}")
                except Exception as e:
                    st.error(f"❌ Error con {url}: {e}")

        if mensajes_generados:
            df = pd.DataFrame(mensajes_generados, columns=["Perfil", "Mensaje", "Fecha"])
            archivo = f"campana_{datetime.date.today()}.xlsx"
            df.to_excel(archivo, index=False)
            st.download_button("📥 Descargar Excel", data=open(archivo, "rb"), file_name=archivo)

            st.markdown("---")
            st.markdown("### 🗂️ Resultados")
            st.dataframe(df, use_container_width=True)
