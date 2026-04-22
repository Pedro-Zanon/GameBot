# 🎮 Gamebot

Bot para Discord que indica jogos com base em pesquisas dos usuários. O bot retorna nota, preço e informações do jogo pesquisado, além de sugerir jogos parecidos ou da mesma categoria, tudo com dados coletados automaticamente do Metacritic.

> 🚧 Projeto em desenvolvimento --- atual em fase inicial
## 🎯 Objetivo

Além de ser um bot funcional, esse projeto é usado como ambiente de estudo e especialização em:

- **API** — construção de APIs REST com Python
- **Selenium** — web scraping e automação de navegador
- **Docker** — containerização e deploy de aplicações

## 📁 Estrutura do Projeto

    gamebot/
    ├── api/
    ├── db_config/
    │   └── db.py
    ├── scraper/
    │   ├── scraper.py
    │   ├── requirements.txt
    │   └── dockerfile
    └── .venv/

## 🕷️ Scraper

Coleta automaticamente dados de jogos do Metacritic, como nome e link, para popular o banco de dados do bot.

### Como funciona

1. Abre o Chrome em modo headless usando `undetected-chromedriver` para evitar detecção de bot
2. Aceita o banner de cookies automaticamente
3. Rola a página para carregar todos os jogos
4. Extrai nome e link de cada jogo

### Tecnologias

- `undetected-chromedriver` — versão do Chrome que evita detecção de bot
- `selenium` — automação do navegador
- `beautifulsoup4` — parse do HTML
- `requests` — requisições HTTP

## ⚙️ Como rodar

### Pré-requisitos

- Python 3.12+
- Google Chrome instalado
- Docker instalado

### Instalação

    git clone <url-do-repo>
    cd gamebot

    python3 -m venv .venv

    source .venv/bin/activate.fish

    pip install -r scraper/requirements.txt

### Executar o scraper

    python3 scraper/scraper.py

### Exemplo de output

    Iniciando...
    Driver iniciado
    Página carregada
    Encontrados 33 jogos
    - Diablo IV: Lord of Hatred
    - Tides of Tomorrow
    - Vampire Crawlers
    - Pragmata
    - Mouse: P.I. for Hire

## 🗺️ Roadmap

- [x] Scraper do Metacritic
- [ ] Banco de dados com jogos, notas e preços
- [ ] API REST para consulta dos jogos
- [ ] Sugestão de jogos similares por categoria
- [ ] Bot do Discord
- [ ] Containerização completa com Docker