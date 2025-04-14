import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

st.set_page_config(page_title="LinkedInviter Automático", layout="centered")
st.title("🤖 LinkedInviter Automático")

st.markdown("""
Esta versión inicia sesión en tu cuenta de LinkedIn y envía invitaciones automáticamente. 
Pega las URLs una por línea, escribe el mensaje personalizado, y la app lo hará por ti.
""")

email = st.text_input("Correo de LinkedIn")
password = st.text_input("Contraseña de LinkedIn", type="password")
urls_input = st.text_area("Perfiles de LinkedIn (uno por línea)", height=150)
mensaje_base = st.text_area("Mensaje personalizado", "Hola {nombre}, me gustaría conectar contigo para compartir oportunidades.")

def iniciar_sesion(email, password):
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    return driver

def enviar_invitacion(driver, url, mensaje):
    try:
        driver.get(url)
        time.sleep(3)
        conectar = driver.find_element(By.XPATH, '//button[contains(text(),"Conectar")]')
        conectar.click()
        time.sleep(2)
        agregar_nota = driver.find_element(By.XPATH, '//button[contains(text(),"Agregar nota")]')
        agregar_nota.click()
        time.sleep(1)
        cuadro = driver.find_element(By.ID, 'custom-message')
        cuadro.send_keys(mensaje)
        time.sleep(1)
        enviar = driver.find_element(By.XPATH, '//button[contains(text(),"Enviar")]')
        enviar.click()
        st.success(f"✅ Invitación enviada a {url}")
    except Exception as e:
        st.error(f"❌ Error con {url}: {e}")

if st.button("Iniciar y Enviar Invitaciones"):
    if not email or not password:
        st.warning("Debes ingresar tus credenciales de LinkedIn.")
    else:
        perfiles = [url.strip() for url in urls_input.split("\n") if url.strip()]
        if not perfiles:
            st.warning("Debes ingresar al menos un perfil.")
        else:
            st.info("Iniciando sesión en LinkedIn...")
            driver = iniciar_sesion(email, password)
            for url in perfiles:
                nombre = url.split("/")[-2].replace("-", " ").title()
                mensaje = mensaje_base.replace("{nombre}", nombre)
                enviar_invitacion(driver, url, mensaje)
            driver.quit()
            st.success("🎉 Proceso completado.")
