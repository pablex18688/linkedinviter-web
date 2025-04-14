import streamlit as st
import time
import os
import json
import datetime
import openai

# Configuración inicial
st.set_page_config(page_title="LinkedInviter PRO", layout="wide")
st.title("🤖 LinkedInviter PRO – Simulación, Guardado y Ejecución de Campañas")

# Clave API de OpenAI
clave_api = st.text_input("🔑 Clave API de OpenAI", type="password")
if clave_api:
    openai.api_key = clave_api

# Archivo de campañas
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

# Panel de campañas
st.subheader("📂 Campañas guardadas")
modo = st.radio("¿Qué desea hacer?", ["Cargar campaña existente", "Crear nueva campaña"])

if modo == "Cargar campaña existente":
    nombre_sel = st.selectbox("Selecciona una campaña", listar_campanias())
    if nombre_sel:
        datos = cargar_campania(nombre_sel)
        st.success(f"Campaña '{nombre_sel}' cargada correctamente")
        st.session_state.update(datos)
else:
    nombre_nueva = st.text_input("📝 Nombre de la campaña nueva")
    if nombre_nueva:
        st.session_state['nombre_campania'] = nombre_nueva

# Formulario editable
st.subheader("⚙️ Configuración")
email = st.text_input("📧 Correo de LinkedIn", value=st.session_state.get('email', ''))
password = st.text_input("🔒 Contraseña", type="password", value=st.session_state.get('password', ''))
palabra_clave = st.text_input("🔍 Palabra clave", value=st.session_state.get('palabra_clave', ''))
ciudad = st.text_input("🌍 Ciudad", value=st.session_state.get('ciudad', ''))
nivel_conexion = st.selectbox("🔗 Conexión", ["Todos", "1er grado", "2do grado", "3er grado"],
                              index=["Todos", "1er grado", "2do grado", "3er grado"].index(st.session_state.get('nivel_conexion', 'Todos')))
empresa = st.text_input("🏢 Empresa", value=st.session_state.get('empresa', ''))
limite_dia = st.number_input("📤 Límite diario", min_value=1, max_value=50, value=st.session_state.get('limite_dia', 20))
tipo_cta = st.selectbox("🔗 Tipo de CTA", ["WhatsApp", "URL personalizada"],
                        index=["WhatsApp", "URL personalizada"].index(st.session_state.get('tipo_cta', 'WhatsApp')))
link_cta = st.text_input("Enlace del CTA", value=st.session_state.get('link_cta', 'https://wa.me/message/Z3OXPSREGEEPB1'))
activar_post = st.checkbox("📩 Mensaje post conexión con IA", value=st.session_state.get('activar_post', True))
modo_simulacion = st.checkbox("🧪 Ejecutar en modo simulación (no enviar mensajes reales)", value=False)

# Guardar campaña
if modo == "Crear nueva campaña" and nombre_nueva:
    if st.button("💾 Guardar campaña"):
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
        st.success(f"✅ Campaña '{nombre_nueva}' guardada exitosamente")

# Generador de mensajes
@st.cache_data(show_spinner=False)
def generar_mensaje(nombre, cargo, ciudad, tipo="inv"):
    prompt = f"Escribe un mensaje profesional y cálido para {tipo} a {nombre}, {cargo} en {ciudad}, sobre soluciones en SST."
    respuesta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    mensaje = respuesta.choices[0].message.content.strip()
    cta_final = f"\n\n👉 Si quieres hablar directamente, escríbeme aquí: {link_cta}"
    return mensaje + cta_final

# Simulación de envío
def ejecutar_campania():
    st.success("✅ Simulación iniciada" if modo_simulacion else "✅ Campaña real iniciada")
    for i in range(min(limite_dia, 5)):
        nombre = f"Contacto{i+1}"
        cargo = "Gerente SST"
        ciudadx = ciudad
        mensaje = generar_mensaje(nombre, cargo, ciudadx, tipo="inv")
        if modo_simulacion:
            st.markdown(f"**[Simulado]** Mensaje a *{nombre}*:\n```{mensaje}```")
        else:
            st.markdown(f"**[Real]** Mensaje enviado a *{nombre}* (simulado en esta versión)")

if st.button("🚀 Ejecutar campaña"):
    if clave_api:
        ejecutar_campania()
    else:
        st.error("❌ Debes ingresar tu clave API de OpenAI.")
