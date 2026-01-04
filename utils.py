from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Roda sem abrir janela
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def garantir_pasta_dados(nome_pasta="dados"):
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)
    return nome_pasta