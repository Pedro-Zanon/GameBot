from selenium.webdriver.common.by import By #localiza elementos (css, xpath, etc)
from bs4 import BeautifulSoup # parseia o HTML
import time 
import undetected_chromedriver as uc # versão do chrome que evita detecção de bot


def setup_driver():

    try:
        options = uc.ChromeOptions() # configurações do navegador
        options.add_argument('--headless=new') # roda sem interface visual (versão nova, menos detectável)
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

        time.sleep(5) # espera a página carregar
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # rola até o fim para carregar jogos lazy-loaded
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0)") # volta ao topo
        time.sleep(2)

        html = driver.page_source # pega o html completo da página
        soup = BeautifulSoup(html, 'html.parser') # transforma o html em objeto navegável
        return soup 

    except Exception as e: 
        print(f"Erro ao tentar abrir o site {e}")


def extrair_jogos(soup, platform):
    try:
        games = []

        # acha todos os links que apontam para páginas de jogos específicos
        # h.startswith('/game/') → só links de jogos, não de navegação
        # h.count('/') >= 3 → filtra links genéricos como /game/ (precisam ter /game/nome/plataforma/)
        links = soup.find_all('a', href=lambda h: h and h.startswith('/game/') and h.count('/') >= 3)
        
        for link in links:
            # tenta pegar o nome pelo h3, que é o título limpo
            # se não tiver h3, pega a primeira linha do texto do link
            nome = link.find('h3')
            if nome:
                nome = nome.get_text(strip=True)
            else:
                nome = link.get_text(strip=True).split('\n')[0].strip()

            href = link.get('href') # pega o caminho do link ex: /game/zelda/
            
            if nome and href:
                jogo = {
                    'nome': nome,
                    'link': f'https://www.metacritic.com{href}', # monta a url completa
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