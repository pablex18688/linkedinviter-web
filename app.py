import streamlit as st
import openai
import time
import datetime
import pandas as pd

# --- Función para generar el mensaje personalizado ---
def generar_mensaje(nombre, cargo, ciudad, tipo="inv"):
    prompt = f"""
    Eres un experto en marketing profesional en LinkedIn.
    Crea un mensaje corto, respetuoso y persuasivo para invitar a conectar a un profesional que se llama {nombre}, es {cargo} en {ciudad}.
    Tipo de mensaje: {'Invitación de conexión' if tipo == 'inv' else 'Seguimiento después de conectar'}.
    Usa un tono profesional, humano, y sin parecer automatizado.
    """

    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return respuesta.choices[0].message['content']

# --- INTERFAZ DE LA APP ---
st.set_page_config(page_title="LinkedInviter Web", layout="centered")
st.title("🚀 LinkedInviter Web")

st.markdown("""
Pega las URLs de LinkedIn (una por línea) y genera mensajes automáticos personalizados.
""")

# --- Input de la clave API ---
api_key = st.text_input("🔑 Clave API de OpenAI", type="password")

if api_key:
    openai.api_key = api_key

    # --- Filtros ---
    nombre = st.text_input("👤 Nombre del contacto", "Carlos")
    cargo = st.text_input("💼 Cargo del contacto", "Gerente de seguridad y salud en el trabajo")
    ciudadx = st.text_input("🌐 Ciudad", "Bogotá")
    tipo_conexion = st.selectbox("🔗 Conexión", ["Todos", "1er grado", "2do grado"])
    empresa = st.text_input("🏢 Empresa")
    limite = st.number_input("📅 Límite diario", min_value=1, max_value=100, value=20)
    tipo_cta = st.selectbox("📎 Tipo de CTA", ["WhatsApp", "URL personalizada"])

    if tipo_cta == "WhatsApp":
        cta = "https://wa.me/message/Z3OXPSREGEEPB1"
    else:
        cta = st.text_input("🔗 Ingresa tu URL personalizada")

    # --- Ejecutar generación ---
    if st.button("✨ Generar mensaje"):
        with st.spinner("Generando mensaje con IA..."):
            try:
                mensaje = generar_mensaje(nombre, cargo, ciudadx, tipo="inv")
                mensaje_final = f"{mensaje}\n\nCTA: {cta}"
                st.success("Mensaje generado con éxito:")
                st.text_area("📝 Resultado", mensaje_final, height=200)

                # Guardar en log de Excel
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log = pd.DataFrame([{
                    "Fecha": fecha,
                    "Nombre": nombre,
                    "Cargo": cargo,
                    "Ciudad": ciudadx,
                    "Empresa": empresa,
                    "Mensaje": mensaje_final,
                    "CTA": cta
                }])

                try:
                    logs_antiguos = pd.read_csv("mensajes_log.csv")
                    log_total = pd.concat([logs_antiguos, log], ignore_index=True)
                except FileNotFoundError:
                    log_total = log

                log_total.to_csv("mensajes_log.csv", index=False)

            except Exception as e:
                st.error(f"❌ Error al generar mensaje: {e}")

else:
    st.warning("🔐 Por favor ingresa tu clave API de OpenAI para continuar.")
