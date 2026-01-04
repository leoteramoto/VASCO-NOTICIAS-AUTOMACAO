# Importamos a função de execução do arquivo dentro da pasta scrapers
from scrapers.netvasco_noticias import executar_netvasco
from scrapers.ge_noticias import executar_ge


# Esta é a função que dá o 'start' em tudo
def iniciar_projeto():
    print("=== SISTEMA DE AUTOMAÇÃO DE NOTÍCIAS (VASCO) ===")

    try:
        # Chama o robô do Netvasco
        executar_netvasco()

        # No futuro, você pode adicionar outros aqui, como:
        executar_ge()

    except Exception as erro_geral:
        print(f"Ocorreu um erro inesperado ao rodar o app: {erro_geral}")

    print("\nAutomação concluída com sucesso!")


# Este comando garante que o código só rode se você executar este arquivo main.py
if __name__ == "__main__":
    iniciar_projeto()
