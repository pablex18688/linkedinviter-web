import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

# Configuración de la página
st.set_page_config(page_title="LinkedInviter Real", layout="centered")
st.title("🚀 LinkedInviter Real desde el navegador")

# Datos del usuario
correo = st.text_input("📧 Correo de LinkedIn")
clave = st.text_input("🔒 Contraseña de LinkedIn", type="password")
palabra_clave = st.text_input("🔍 Palabra clave de búsqueda")
ciudad = st.text_input("🌍 Ciudad")
empresa = st.text_input("🏢 Empresa (opcional)")
limite = st.number_input("📤 Límite de invitaciones", min_value=1, max_value=50, value=5)

if st.button("✅ Iniciar envíos reales"):
    st.success("Iniciando navegador...")

    # Configurar Chrome en modo visible
    options = Options()
    options.add_experimental_option("detach", True)  # Deja el navegador abierto

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.linkedin.com/login")

    # Login
    sleep(2)
    driver.find_element(By.ID, "username").send_keys(correo)
    driver.find_element(By.ID, "password").send_keys(clave)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    sleep(5)

    # Buscar
    query = f"{palabra_clave} {empresa if empresa else ''} {ciudad}"
    driver.get(f"https://www.linkedin.com/search/results/people/?keywords={query.replace(' ', '%20')}")
    sleep(5)

    enviados = 0
    perfiles = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label^="Conectar"]')

    for boton in perfiles:
        if enviados >= limite:
            break
        try:
            boton.click()
            sleep(2)
            enviar_btn = driver.find_element(By.XPATH, '//button[@aria-label="Enviar ahora"]')
            enviar_btn.click()
            st.write(f"✅ Invitación enviada #{enviados + 1}")
            enviados += 1
            sleep(3)
        except Exception as e:
            st.warning(f"⚠️ Error al enviar: {str(e)}")
            continue

    st.success(f"Proceso finalizado: {enviados} invitaciones enviadas.")
