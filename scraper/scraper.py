from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc

def setup_driver():
    try:
        options = uc.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        driver = uc.Chrome(options=options, version_main=None)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar driver {e}")
        return None

def scrape_metacritic(url, driver):
    try:
        driver.get(url)
        try:
            accept_button = driver.find_elements(By.XPATH, "//button[text()='I Accept']")
            accept_button[0].click()
        except:
            pass
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except Exception as e:
        print(f"Erro ao tentar abrir o site {e}")

def extrair_jogos(soup, platform):
    try:
        games = []
        links = soup.find_all('a', href=lambda h: h and h.startswith('/game/') and h.count('/') >= 3)
        for link in links:
            nome = link.find('h3')
            if nome:
                nome = nome.get_text(strip=True)
            else:
                nome = link.get_text(strip=True).split('\n')[0].strip()
            href = link.get('href')
            if nome and href:
                jogo = {
                    'nome': nome,
                    'link': f'https://www.metacritic.com{href}',
                    'tipo': 'jogo'
                }
                games.append(jogo)
        return games
    except Exception as e:
        print(f"erro ao buscar o jogo: {e}")
        return []

if __name__ == '__main__':
    url = 'https://www.metacritic.com/browse/games/'
    print("Iniciando...")
    driver = setup_driver()
    if driver is None:
        print("Driver falhou, sai do programa")
        exit(1)
    print("Driver iniciado")
    soup = scrape_metacritic(url, driver)
    if soup is None:
        print("Scraping falhou")
        driver.quit()
        exit(1)
    print("Página carregada")
    jogos = extrair_jogos(soup, 'general')
    print(f"Encontrados {len(jogos)} jogos")
    for jogo in jogos[:10]:
        print(f"- {jogo['nome']}")
    driver.quit()