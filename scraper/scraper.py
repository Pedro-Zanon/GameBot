from selenium.webdriver.common.by import By #localiza elementos (css, xpath, etc)
from bs4 import BeautifulSoup # parseia o HTML
import time 
import undetected_chromedriver as uc # versão do chrome que evita detecção de bot


def setup_driver():

    try:
        options = uc.ChromeOptions() # configurações do navegador
        #options.add_argument('--headless=new') # roda sem interface visual (versão nova, menos detectável)
        options.add_argument('--no-sandbox') # necessário para rodar como root
        options.add_argument('--disable-dev-shm-usage') # evita erros de memória no Docker
        options.add_argument('--disable-gpu') # desativa GPU, necessário em ambientes sem interface gráfica
        driver = uc.Chrome(options=options, version_main=None) # inicia o chrome com as configurações
        return driver
    
    except Exception as e:
        print(f"Erro ao iniciar driver {e}")
        return None

def scrape_metacritic(url, driver):

    try:
        driver.get(url) # abre a url no navegador

        try:
            # tenta achar e clicar no botão de aceitar cookies
            accept_button = driver.find_elements(By.XPATH, "//button[text()='I Accept']")
            accept_button[0].click()
        except:
            pass # se não achar o botão, ignora e continua

        time.sleep(8) # espera a página carregar
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0)") # volta ao topo
        time.sleep(3)

        html = driver.page_source # pega o html completo da página
        with open('debug_metacritic.html', 'w', encoding='utf-8') as f:
            f.write(html)
        soup = BeautifulSoup(html, 'html.parser') # transforma o html em objeto navegável
        return soup 

    except Exception as e: 
        print(f"Erro ao tentar abrir o site {e}")


def extrair_jogos(soup, platform):
    try:
        games = []

        # busca pelo container principal da lista de jogos
        # O Metacritic usa um elemento com data-testid nos cards
        cards = soup.find_all('div', attrs={'data-testid': 'browse-product-card'})

        #  busca pela section/main content, ignora nav/header/footer
        if not cards:
            main = soup.find('main') or soup.find('div', attrs={'id': 'main_content'})
            if main:
                cards = main.find_all('a', href=lambda h: h and h.startswith('/game/') and h.count('/') >= 3)
            else:
                cards = []

        for card in cards:
            # Se veio da estratégia 1 (div card), pega o link dentro dele
            if card.name == 'div':
                link = card.find('a', href=lambda h: h and h.startswith('/game/'))
            else:
                link = card  # já é o <a> da estratégia 2

            if not link:
                continue

            href = link.get('href', '')

            # Ignora links que são só /game/ sem slug (links de nav genéricos)
            parts = href.strip('/').split('/')
            if len(parts) < 2:
                continue

            # Pega o nome: tenta h3, depois h2, depois texto do link
            nome_tag = link.find(['h3', 'h2']) or card.find(['h3', 'h2'])
            if nome_tag:
                nome = nome_tag.get_text(strip=True)
            else:
                nome = link.get_text(strip=True).split('\n')[0].strip()

            if nome and href and len(nome) > 1:
                jogo = {
                    'nome': nome,
                    'link': f'https://www.metacritic.com{href}',
                    'tipo': 'jogo'
                }
                # Evita duplicatas
                if not any(j['link'] == jogo['link'] for j in games):
                    games.append(jogo)

            if len(games) >= 50:
                break

        return games
    except Exception as e:
        print(f"erro ao buscar o jogo: {e}")
        return []

if __name__ == '__main__':
    url = 'https://www.metacritic.com/browse/game/'
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