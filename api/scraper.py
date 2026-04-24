from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc


def setup_driver():
    try:
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        driver = uc.Chrome(options=options, version_main=None)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar driver {e}")
        return None


def aceitar_cookies(driver):
    try:
        # tenta vários textos possíveis do botão
        for texto in ["I Accept", "Accept", "Accept All", "Aceitar"]:
            botoes = driver.find_elements(By.XPATH, f"//button[text()='{texto}']")
            if botoes:
                botoes[0].click()
                #print("Cookie aceito")
                time.sleep(1)
                return
    except:
        pass


def formatar_slug(nome):
    return nome.strip().lower().replace(' ', '-')


def extrair_jogo(nome_jogo, driver):
    try:
        slug = formatar_slug(nome_jogo)
        url = f'https://www.metacritic.com/game/{slug}/'
        #print(f"Acessando: {url}")

        driver.get(url)
        time.sleep(6)
        aceitar_cookies(driver)
        time.sleep(3)

        # salva HTML para debug
        html = driver.page_source
        with open('debug.html', 'w', encoding='utf-8') as f:
            f.write(html)

        soup = BeautifulSoup(html, 'html.parser')

        # nome
        try:
            nome = soup.find('h1').get_text(strip=True)
        except:
            nome = nome_jogo

        # metascore — busca pelo label "METASCORE" e pega o número próximo
        nota = "N/A"
        try:
            elemento = soup.find('span', attrs={'data-testid': 'global-score-value'})
            if elemento:
                nota = elemento.get_text(strip=True)
        except:
            pass

        print(f"\n=== Resultado ===")
        print(f"Jogo:  {nome}")
        print(f"Metascore: {nota}")

        return {'nome': nome, 'nota': nota}

    except Exception as e:
        print(f"Erro geral: {e}")
        return None


if __name__ == '__main__':
    jogo = input("Digite o nome do jogo: ")
    print("Iniciando...")
    driver = setup_driver()
    if driver is None:
        print("Driver falhou")
        exit(1)
    print("Driver iniciado")
    extrair_jogo(jogo, driver)
    driver.quit()