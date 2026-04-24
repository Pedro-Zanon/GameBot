from flask import Flask, request, jsonify
from scraper import setup_driver, extrair_jogo
app = Flask(__name__)

@app.route('/')
def home():
    return "API do Scraper está rodando!"

@app.route('/scrape')
def scraper():
    jogo = request.args.get('jogo')
    if not jogo:
        return jsonify({'erro': 'Nome do jogo não fornecido'}), 400

    driver = setup_driver()
    if driver is None:
        return jsonify ({'eroo': 'Falha ao inicar o Chrome'}), 500

    resultado = extrair_jogo(jogo, driver)
    driver.quit()

    if resultado:
        return jsonify({'resultado': resultado})
    return jsonify ({'eroo': 'Jogo não encontrado'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
