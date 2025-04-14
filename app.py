import streamlit as st
import openai
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="LinkedInviter Web", layout="centered")
st.title("🚀 LinkedInviter Web")

st.markdown("Pega las URLs de LinkedIn (una por línea) y escribe un mensaje con {nombre}.")

# 👉 Clave API OpenAI
api_key = st.text_input("🔑 Clave API de OpenAI", type="password")
if api_key:
    openai.api_key = api_key

# 👉 Campos de entrada
urls_input = st.text_area("🔗 Perfiles de LinkedIn (una URL por línea)", height=150)
mensaje_base = st.text_area("💬 Mensaje personalizado", "Hola {nombre}, me gustaría conectar contigo.")

# 👉 Opciones avanzadas
limite = st.number_input("📌 Límite diario", min_value=1, value=20)
cta_tipo = st.selectbox("📣 Tipo de CTA", ["WhatsApp", "URL personalizada"])
cta_valor = st.text_input("📍 Enlace CTA (WhatsApp o URL)", "https://wa.me/message/Z3OXPSREGEEPB1")

# 👉 Generar mensajes
if st.button("✉️ Generar Mensajes"):
    if not api_key:
        st.error("Por favor ingresa tu clave API de OpenAI.")
    else:
        perfiles = [url.strip() for url in urls_input.split("\n") if url.strip()]
        resultados = []
        for url in perfiles[:limite]:
            try:
                nombre = url.split("/")[-2].replace("-", " ").title()
                prompt = f"{mensaje_base}\n\nAgrega este llamado a la acción: {cta_valor}"
                respuesta = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un experto en marketing para LinkedIn."},
                        {"role": "user", "content": prompt}
                    ]
                )
                mensaje = respuesta.choices[0].message.content.strip()
                resultados.append({"Nombre": nombre, "URL": url, "Mensaje": mensaje})
                st.success(f"✅ Mensaje generado para {nombre}")
            except Exception as e:
                st.error(f"❌ Error con {url}: {str(e)}")

        # Exportar a Excel
        if resultados:
            df = pd.DataFrame(resultados)
            fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
            nombre_excel = f"mensajes_generados_{fecha}.xlsx"
            df.to_excel(nombre_excel, index=False)
            with open(nombre_excel, "rb") as f:
                st.download_button("📥 Descargar Excel", f, file_name=nombre_excel, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

