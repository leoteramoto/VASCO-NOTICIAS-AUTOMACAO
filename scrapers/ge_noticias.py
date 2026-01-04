from selenium.webdriver.common.by import By
import time
import requests
import json
import os

# Importamos as configurações e ferramentas padrão do projeto
from config import URL_PLANILHA
from utils import iniciar_driver, garantir_pasta_dados


def executar_ge():
    """Função para buscar os 3 destaques principais do Vasco no GE."""

    driver = iniciar_driver()
    pasta = garantir_pasta_dados("dados")
    caminho_arquivo = os.path.join(pasta, "noticias_ge.txt")

    # Lista para guardar apenas os endereços (URLs) antes de começar a abrir as notícias
    lista_de_links = []

    try:
        print("\n--- Robô GE Vasco: Buscando Destaques do Topo ---")
        driver.get("https://ge.globo.com/futebol/times/vasco/")
        time.sleep(3)  # Tempo para garantir que o JavaScript carregou os destaques

        # 1. COLETANDO OS LINKS
        # O seletor 'a.bstn-hl-link' é o mais estável para os blocos de destaque do topo
        elementos_destaque = driver.find_elements(By.CSS_SELECTOR, "a.bstn-hl-link")

        for elemento in elementos_destaque:
            url = elemento.get_attribute("href")
            if url and url not in lista_de_links:
                lista_de_links.append(url)

        # Queremos apenas os 3 primeiros destaques da página inicial
        links_para_processar = lista_de_links[:3]
        print(f"Encontrados {len(links_para_processar)} destaques principais.")

        # 2. PROCESSANDO CADA NOTÍCIA
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            for i, url in enumerate(links_para_processar, 1):
                try:
                    print(f"Processando destaque {i} de 3...")
                    driver.get(url)
                    time.sleep(2)  # Espera o texto da matéria carregar

                    titulo = driver.title

                    # No GE, o texto da notícia fica em elementos com a classe 'content-text'
                    paragrafos = driver.find_elements(By.CLASS_NAME, "content-text")
                    texto_da_materia = "\n".join([p.text for p in paragrafos])

                    # Grava no arquivo TXT local
                    arquivo.write(
                        f"DESTAQUE {i}\nTÍTULO: {titulo}\nLINK: {url}\n{texto_da_materia}\n"
                    )
                    arquivo.write("=" * 50 + "\n")

                    # Envia para a Planilha do Google
                    dados = {
                        "titulo": titulo,
                        "link": url,
                        "conteudo": texto_da_materia,
                    }

                    resposta = requests.post(URL_PLANILHA, data=json.dumps(dados))

                    if resposta.status_code == 200:
                        print(f"   -> Sucesso: Destaque '{titulo[:30]}...' enviado!")
                    else:
                        print(f"   -> Erro ao enviar para a planilha.")

                except Exception as e:
                    print(f"Erro ao processar o link {url}: {e}")

        print("\nProcesso dos destaques do GE concluído!")

    finally:
        driver.quit()
