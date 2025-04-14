import streamlit as st
import time
import os
import json
from datetime import datetime

st.set_page_config(page_title="LinkedInviter PRO - Sin GPT", layout="wide")
st.title("🤖 LinkedInviter PRO - Sin GPT")

# Archivo local para campañas
CAMPAIGN_FILE = "campanias_v2.json"
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

st.subheader("📁 Gestión de campañas")
modo = st.radio("¿Qué deseas hacer?", ["Cargar campaña existente", "Crear nueva campaña"])

if modo == "Cargar campaña existente":
    nombre_sel = st.selectbox("Selecciona una campaña", listar_campanias())
    if nombre_sel:
        datos = cargar_campania(nombre_sel)
        st.session_state.update(datos)
        st.success(f"✅ Campaña '{nombre_sel}' cargada")
else:
    nombre_nueva = st.text_input("📝 Nombre de la campaña nueva")
    if nombre_nueva:
        st.session_state['nombre_campania'] = nombre_nueva

# Formulario
st.subheader("🧩 Configura tu campaña")
email = st.text_input("📧 Correo de LinkedIn", value=st.session_state.get('email', ''))
password = st.text_input("🔒 Contraseña", type="password", value=st.session_state.get('password', ''))
palabra_clave = st.text_input("🔍 Palabra clave", value=st.session_state.get('palabra_clave', ''))
ciudad = st.text_input("🌍 Ciudad", value=st.session_state.get('ciudad', ''))
nivel_conexion = st.selectbox("🔗 Conexión", ["Todos", "1er grado", "2do grado", "3er grado"],
                              index=["Todos", "1er grado", "2do grado", "3er grado"].index(st.session_state.get('nivel_conexion', 'Todos')))
empresa = st.text_input("🏢 Empresa", value=st.session_state.get('empresa', ''))
limite_dia = st.number_input("📤 Límite diario de invitaciones", min_value=1, max_value=50, value=st.session_state.get('limite_dia', 20))
mensaje_inv = st.text_area("✉️ Mensaje de invitación", value=st.session_state.get('mensaje_inv', "Hola {nombre}, me gustaría conectar contigo."))
mensaje_post = st.text_area("📨 Mensaje post conexión", value=st.session_state.get('mensaje_post', "Gracias por aceptar. ¡Quedo atento a conversar!"))
link_cta = st.text_input("🔗 CTA: WhatsApp o URL personalizada", value=st.session_state.get('link_cta', 'https://wa.me/message/Z3OXPSREGEEPB1'))
modo_simulacion = st.checkbox("🧪 Simulación (sin envío real)", value=True)

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
            'mensaje_inv': mensaje_inv,
            'mensaje_post': mensaje_post,
            'link_cta': link_cta
        }
        guardar_campania(nombre_nueva, datos_guardar)
        st.success(f"💾 Campaña '{nombre_nueva}' guardada")

# Simular ejecución
if st.button("🚀 Ejecutar campaña"):
    st.success("✅ Simulación iniciada" if modo_simulacion else "✅ Campaña real iniciada")
    for i in range(min(limite_dia, 5)):
        nombre = f"Contacto{i+1}"
        cargo = "Gerente SST"
        inv_mensaje = mensaje_inv.replace("{nombre}", nombre)
        post_mensaje = mensaje_post.replace("{nombre}", nombre) + f"\n📌 {link_cta}"
        if modo_simulacion:
            st.markdown(f"**[Simulado]** Invitación a *{nombre}*:\n```{inv_mensaje}```")
            st.markdown(f"**[Simulado]** Mensaje post-conexión:\n```{post_mensaje}```")
        else:
            st.markdown(f"**[Real]** Invitación enviada a *{nombre}* (esto es un ejemplo, no envío real)")
        time.sleep(0.5)
