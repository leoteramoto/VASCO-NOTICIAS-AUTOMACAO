from selenium.webdriver.common.by import By
import time
import requests
import json
from config import URL_PLANILHA
from utils import iniciar_driver

def executar_ge():
    driver = iniciar_driver()
    lista_de_links = []

    try:
        print("\n--- Robô GE Vasco ---")
        driver.get("https://ge.globo.com/futebol/times/vasco/")
        time.sleep(3)

        # Mapeia os 3 destaques
        elementos = driver.find_elements(By.CSS_SELECTOR, "a.bstn-hl-link")
        for el in elementos:
            url = el.get_attribute("href")
            if url and url not in lista_de_links:
                lista_de_links.append(url)
        
        # Entra em cada um e envia
        for i, url in enumerate(lista_de_links[:3], 1):
            try:
                driver.get(url)
                time.sleep(2)
                titulo = driver.title
                paragrafos = driver.find_elements(By.CLASS_NAME, "content-text")
                texto = "\n".join([p.text for p in paragrafos])

                dados = {"titulo": titulo, "link": url, "conteudo": texto}
                requests.post(URL_PLANILHA, data=json.dumps(dados))
                print(f"[{i}] Destaque GE enviado!")

            except Exception as e:
                print(f"Erro no destaque {i}: {e}")

    finally:
        driver.quit()
