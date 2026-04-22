import flask
import sqlite3
from flask import request, jsonify, Blueprint

app = flask.Flask(__name__)

@app.route('/api/jogos', methods=['POST'])
def add_jogo():
    try:
        data = request.get_json()
        nome = data.get('nome')
        preco = data.get('preco')
        desconto = data.get('desconto')
        avaliacao = data.get('avaliacao')
        genero = data.get('genero')
        link = data.get('link')
        tipo = data.get('tipo')
        created_at = data.get('created_at')

        with sqlite3.connect('test.db') as conn:
            c = conn.cursor()
            c.execute('''
                 INSERT INTO jogos (nome, preco, desconto, avaliacao, genero, link, tipo, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, preco, desconto, avaliacao, genero, link, tipo, created_at))
            conn.commit()

        return jsonify({'message': 'Jogo adicionado com sucesso!'}), 201

    except Exception as e:
        print(f"Erro ao adicionar o jogo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jogos', methods=['GET'])
def get_jogos():
    try:
        with sqlite3.connect('test.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT id, nome, preco, desconto, avaliacao, genero, link, tipo, created_at FROM jogos''')
            jogos = c.fetchall()
        return jsonify({'jogos': jogos}), 200

    except Exception as e:
        print(f"Erro ao buscar jogos: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jogos/<int:jogo_id>', methods=['GET'])
def get_jogo_by_id(jogo_id):
    try:
        with sqlite3.connect('test.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT id, nome, preco, desconto, avaliacao, genero, link, tipo, created_at FROM jogos WHERE id = ?''', (jogo_id,))
            jogo = c.fetchone()
        if jogo:
            return jsonify({'jogo': jogo}), 200
        return jsonify({'error': 'Jogo nao encontrado'}), 404

    except Exception as e:
        print(f"Erro ao buscar jogo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jogos/<int:jogo_id>', methods=['PUT'])
def update_jogo(jogo_id):
    try:
        data = request.get_json()
        nome = data.get('nome')
        preco = data.get('preco')
        desconto = data.get('desconto')
        avaliacao = data.get('avaliacao')
        genero = data.get('genero')
        link = data.get('link')
        tipo = data.get('tipo')

        with sqlite3.connect('test.db') as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE jogos
                SET nome = ?, preco = ?, desconto = ?, avaliacao = ?, genero = ?, link = ?, tipo = ?
                WHERE id = ?
            ''', (nome, preco, desconto, avaliacao, genero, link, tipo, jogo_id))
            conn.commit()

        return jsonify({'message': 'Jogo atualizado com sucesso!'}), 200

    except Exception as e:
        print(f"Erro ao atualizar jogo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jogos/<int:jogo_id>', methods=['DELETE'])
def delete_jogo(jogo_id):
    try:
        with sqlite3.connect('test.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM jogos WHERE id = ?', (jogo_id,))
            conn.commit()

        return jsonify({'message': 'Jogo deletado com sucesso!'}), 200

    except Exception as e:
        print(f"Erro ao deletar jogo: {e}")
        return jsonify({'error': str(e)}), 500
