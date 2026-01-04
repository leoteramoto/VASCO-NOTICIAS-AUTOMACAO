from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def iniciar_driver():
    """Configura o Chrome para rodar no servidor do GitHub (Linux)."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver
