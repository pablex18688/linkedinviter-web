import streamlit as st
import time
import os
import json
import datetime
import openai

st.set_page_config(page_title="LinkedInviter PRO", layout="wide")
st.title("🤖 LinkedInviter PRO con GPT-4o")

# API key desde input
api_key = st.text_input("🔑 Clave API de OpenAI", type="password")
if api_key:
    openai.api_key = api_key

# Archivo donde se guardan las campañas
CAMPAIGN_FILE = "campanias_guardadas.json"
if not os.path.exists(CAMPAIGN_FILE):
    with open(CAMPAIGN_FILE, "w") as f:
        json.dump({}, f)

def guardar_campania(nombre, data):
    with open(CAMPAIGN_FILE, "r") as f:
        campañas = json.load(f)
    campañas[nombre] = data
    with open(CAMPAIGN_FILE, "w") as f:
        json.dump(campañas, f)

def cargar_campania(nombre):
    with open(CAMPAIGN_FILE, "r") as f:
        campañas = json.load(f)
    return campañas.get(nombre, {})

def listar_campanias():
    with open(CAMPAIGN_FILE, "r") as f:
        campañas = json.load(f)
    return list(campañas.keys())

# Panel para seleccionar o crear campaña
st.subheader("📂 Campañas guardadas")
modo = st.radio("Acción:", ["Cargar campaña existente", "Crear nueva campaña"])

if modo == "Cargar campaña existente":
    nombre_sel = st.selectbox("Selecciona una campaña", listar_campanias())
    if nombre_sel:
        datos = cargar_campania(nombre_sel)
        st.success(f"Campaña '{nombre_sel}' cargada")
        st.session_state.update(datos)
else:
    nombre_nueva = st.text_input("📅 Nombre de la nueva campaña")
    if nombre_nueva:
        st.session_state['nombre_campania'] = nombre_nueva

# Formulario editable
st.subheader("⚙️ Configuración de la campaña")
email = st.text_input("📧 Correo de LinkedIn", value=st.session_state.get('email', ''))
password = st.text_input("🔐 Contraseña", type="password", value=st.session_state.get('password', ''))
palabra_clave = st.text_input("🔍 Palabra clave", value=st.session_state.get('palabra_clave', ''))
ciudad = st.text_input("🌍 Ciudad", value=st.session_state.get('ciudad', ''))
nivel_conexion = st.selectbox("🔗 Conexión", ["Todos", "1er grado", "2do grado", "3er grado"],
                              index=["Todos", "1er grado", "2do grado", "3er grado"].index(st.session_state.get('nivel_conexion', 'Todos')))
empresa = st.text_input("🏢 Empresa", value=st.session_state.get('empresa', ''))
limite_dia = st.number_input("📤 Límite diario", min_value=1, max_value=50, value=st.session_state.get('limite_dia', 20))
tipo_cta = st.selectbox("🔗 Tipo de CTA", ["WhatsApp", "URL personalizada"],
                        index=["WhatsApp", "URL personalizada"].index(st.session_state.get('tipo_cta', 'WhatsApp')))
link_cta = st.text_input("Enlace del CTA", value=st.session_state.get('link_cta', 'https://wa.me/message/Z3OXPSREGEEPB1'))
activar_post = st.checkbox("📩 Mensaje post conexión con GPT", value=st.session_state.get('activar_post', True))
modo_simulacion = st.checkbox("🧪 Simular sin enviar", value=False)

# Guardar campaña nueva
if modo == "Crear nueva campaña" and nombre_nueva:
    if st.button("📀 Guardar campaña"):
        datos_guardar = {
            'email': email,
            'password': password,
            'palabra_clave': palabra_clave,
            'ciudad': ciudad,
            'nivel_conexion': nivel_conexion,
            'empresa': empresa,
            'limite_dia': limite_dia,
            'tipo_cta': tipo_cta,
            'link_cta': link_cta,
            'activar_post': activar_post
        }
        guardar_campania(nombre_nueva, datos_guardar)
        st.success(f"✅ Campaña '{nombre_nueva}' guardada")

# Generador de mensajes con GPT-4o
def generar_mensaje(nombre, cargo, ciudad, tipo="inv"):
    prompt = f"Escribe un mensaje profesional y cálido para {tipo} a {nombre}, {cargo} en {ciudad}, sobre soluciones en SST."
    try:
        respuesta = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        mensaje = respuesta.choices[0].message.content.strip()
        return mensaje + f"\n\n👉 Contáctame: {link_cta}"
    except Exception as e:
        return f"[Error al generar mensaje: {str(e)}]"

# Botón ejecutar campaña
if st.button("🚀 Ejecutar campaña"):
    st.info("Procesando mensajes...")
    for i in range(min(limite_dia, 5)):
        nombre = f"Contacto{i+1}"
        cargo = "Gerente SST"
        ciudadx = ciudad
        mensaje = generar_mensaje(nombre, cargo, ciudadx, tipo="inv")
        if modo_simulacion:
            st.markdown(f"**[Simulado]** A *{nombre}*:\n```{mensaje}```")
        else:
            st.markdown(f"**[Enviado]** A *{nombre}*:\n```{mensaje}```")
