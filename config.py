import os

# O .strip() remove qualquer espaço ou "Enter" que possa vir do GitHub Secrets
URL_PLANILHA = os.getenv("URL_PLANILHA", "").strip()
