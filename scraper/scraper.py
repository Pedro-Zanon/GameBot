# Selenium: usado para controlar o navegador de forma programática
# By: define como localizar elementos (xpath, css, id, etc)
from selenium.webdriver.common.by import By
# WebDriverWait: espera um elemento aparecer antes de interagir
from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions: define a condição de espera (ex: elemento clicável)
from selenium.webdriver.support import expected_conditions as EC
# BeautifulSoup: parseia o HTML retornado pelo Selenium de forma mais simples
from bs4 import BeautifulSoup
# time: usado para pausas manuais enquanto a página carrega
import time
# undetected_chromedriver: versão do Chrome que evita detecção de bot pelo site
import undetected_chromedriver as uc


def setup_driver():
    # inicializa o navegador com as configurações necessárias
    try:
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')         # necessário para rodar como root
        options.add_argument('--disable-dev-shm-usage') # evita erros de memória no Docker
        options.add_argument('--disable-gpu')        # desativa GPU, necessário sem interface gráfica
        # version_main=None: detecta automaticamente a versão do Chrome instalado
        driver = uc.Chrome(options=options, version_main=None)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar driver {e}")
        return None


def aceitar_cookies(driver):
    # separada em função própria para poder ser reutilizada em diferentes momentos da navegação
    try:
        # tenta vários textos possíveis pois o botão pode variar dependendo do idioma ou versão do site
        for texto in ["I Accept", "Accept", "Accept All", "Aceitar"]:
            botoes = driver.find_elements(By.XPATH, f"//button[text()='{texto}']")
            if botoes:
                botoes[0].click()
                time.sleep(1) # pequena pausa para o modal fechar antes de continuar
                return
    except:
        pass # se não encontrar o botão, ignora e segue normalmente


def formatar_slug(nome):
    # o Metacritic usa slugs no formato "portal-2" na URL
    # strip() remove espaços nas bordas, lower() deixa minúsculo, replace() troca espaços por hífen
    return nome.strip().lower().replace(' ', '-')


def extrair_jogo(nome_jogo, driver):
    try:
        slug = formatar_slug(nome_jogo)
        # monta a URL diretamente em vez de navegar pela busca
        # isso é mais rápido e evita problemas de clicar no elemento certo nos resultados
        url = f'https://www.metacritic.com/game/{slug}/'

        driver.get(url)
        time.sleep(6) # aguarda o carregamento inicial da página e do JavaScript

        aceitar_cookies(driver)
        time.sleep(3) # aguarda o modal de cookie fechar completamente

        # salva o HTML para facilitar debug caso o seletor não funcione
        html = driver.page_source
        with open('debug.html', 'w', encoding='utf-8') as f:
            f.write(html)

        # BeautifulSoup é usado aqui pois é mais simples para navegar no HTML estático
        # após o Selenium já ter carregado o JavaScript
        soup = BeautifulSoup(html, 'html.parser')

        # pega o nome oficial do jogo direto do H1 da página
        try:
            nome = soup.find('h1').get_text(strip=True)
        except:
            nome = nome_jogo # fallback para o nome digitado caso o H1 não seja encontrado

        # busca o metascore pelo data-testid que é mais estável que classes CSS
        # classes CSS podem mudar com atualizações do site, data-testid tende a ser mais permanente
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

        # retorna dicionário para facilitar o uso dos dados em outras partes do código no futuro
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
    driver.quit() # encerra o navegador ao final para liberar memória