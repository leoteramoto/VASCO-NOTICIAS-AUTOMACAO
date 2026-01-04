from selenium.webdriver.common.by import By
import time
import requests
import json
import os

# Importamos a URL centralizada e nossas funções de ajuda
from config import URL_PLANILHA
from utils import iniciar_driver, garantir_pasta_dados


def executar_netvasco():
    """Função principal que roda o robô do Netvasco."""

    # 1. Preparamos o navegador e a pasta de destino
    driver = iniciar_driver()
    pasta = garantir_pasta_dados("dados")
    caminho_arquivo = os.path.join(pasta, "noticias_vasco.txt")

    links_noticias = []

    try:
        print("\n--- Iniciando Robô: Netvasco ---")
        # Entra no site principal
        driver.get("https://www.netvasco.com.br/")

        # Busca os elementos que contêm os links das notícias
        print("Coletando links das notícias principais...")
        destaques = driver.find_elements(
            By.CSS_SELECTOR, ".titulo-destaque-grande, .titulo-destaque-menor"
        )

        # Extrai o endereço (URL) de cada link encontrado
        for d in destaques:
            url = d.find_element(By.TAG_NAME, "a").get_attribute("href")
            # Só adiciona na lista se o link ainda não estiver lá (evita duplicados)
            if url not in links_noticias:
                links_noticias.append(url)

        # 2. Abre o arquivo TXT para escrita ('w' limpa o arquivo antigo)
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            for i, url in enumerate(links_noticias, 1):
                try:
                    # Entra na página individual da notícia
                    driver.get(url)
                    time.sleep(2)  # Espera 2 segundos para o site carregar bem

                    # Pega o título da página e o texto do corpo da notícia
                    titulo = driver.title
                    conteudo = driver.find_element(By.CLASS_NAME, "corpo").text

                    # Salva as informações formatadas no seu arquivo TXT
                    arquivo.write(
                        f"TÍTULO: {titulo}\nLINK: {url}\n{conteudo}\n" + "=" * 50 + "\n"
                    )

                    # 3. Organiza os dados para enviar para o Google Sheets via API
                    dados_para_enviar = {
                        "titulo": titulo,
                        "link": url,
                        "conteudo": conteudo,
                    }

                    # Envia os dados usando o método POST para a URL que está no config.py
                    resposta = requests.post(
                        URL_PLANILHA, data=json.dumps(dados_para_enviar)
                    )

                    # Verifica se o Google recebeu os dados com sucesso (status 200)
                    if resposta.status_code == 200:
                        print(f"[{i}] Sucesso: Notícia enviada para a planilha!")
                    else:
                        print(f"[{i}] Erro: Falha ao enviar para o Google Sheets.")

                except Exception as e:
                    print(f"Erro ao processar notícia {i}: {e}")

        print("Finalizado: Todas as notícias do Netvasco foram processadas.")

    finally:
        # Fecha o navegador no final, mesmo que ocorra algum erro no meio
        driver.quit()
