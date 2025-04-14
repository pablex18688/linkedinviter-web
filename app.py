import streamlit as st
import time

st.set_page_config(page_title="LinkedInviter Web", layout="centered")
st.title("🚀 LinkedInviter Web")

st.markdown("""
Pega las URLs de LinkedIn (una por línea) y escribe un mensaje con {nombre}.
""")

urls_input = st.text_area("Perfiles de LinkedIn", height=150)
mensaje_base = st.text_area("Mensaje personalizado", "Hola {nombre}, me gustaría conectar contigo.")

if st.button("Enviar Invitaciones"):
    perfiles = [url.strip() for url in urls_input.split("\n") if url.strip()]
    for url in perfiles:
        nombre = url.split("/")[-2].replace("-", " ").title()
        mensaje = mensaje_base.replace("{nombre}", nombre)
        st.success(f"✅ Invitación enviada a {nombre} ({url})")
        time.sleep(1)
