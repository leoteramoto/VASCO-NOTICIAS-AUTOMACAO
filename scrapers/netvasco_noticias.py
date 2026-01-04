from selenium.webdriver.common.by import By
import time
import requests
import json
from config import URL_PLANILHA
from utils import iniciar_driver

def executar_netvasco():
    driver = iniciar_driver()
    links_noticias = []

    try:
        print("\n--- Robô Netvasco ---")
        driver.get("https://www.netvasco.com.br/")
        
        # Coleta os links
        destaques = driver.find_elements(By.CSS_SELECTOR, ".titulo-destaque-grande, .titulo-destaque-menor")
        for d in destaques:
            url = d.find_element(By.TAG_NAME, "a").get_attribute("href")
            if url not in links_noticias:
                links_noticias.append(url)

        # Processa e envia direto para a planilha
        for i, url in enumerate(links_noticias[:5], 1): # Limitado a 5 para teste
            try:
                driver.get(url)
                time.sleep(2)
                titulo = driver.title
                conteudo = driver.find_element(By.CLASS_NAME, "corpo").text

                dados = {"titulo": titulo, "link": url, "conteudo": conteudo}
                
                # Envio para o Google
                resposta = requests.post(URL_PLANILHA, data=json.dumps(dados))
                
                if resposta.status_code == 200:
                    print(f"[{i}] Enviado com sucesso!")
                else:
                    print(f"[{i}] Erro no Google: {resposta.status_code}")

            except Exception as e:
                print(f"Erro na notícia {i}: {e}")

    finally:
        driver.quit()
