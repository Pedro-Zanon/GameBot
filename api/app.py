import flask
import sqlite3
from flask import request, jsonify, Blueprint

app = flask.Flask(__name__)

@app.route('/api/app', methods=['POST'])
def add_produto():
    try:

        data = request.get_json()
        titulo = data.get('titulo')
        preco = data.get('preco')
        url = data.get('url')
        created_at = data.get('data')

        with sqlite3.connect('test.db') as conn:
            c = conn.cursor()
            c.execute('''
                 INSERT INTO test (titulo, preco, url, created_at)  VALUES (?, ?, ?, ?)
            ''', (titulo, preco, url, created_at))
            conn.commit()

        return jsonify ({'message': 'Produto adicionado com sucesso!'}), 201

    except Exception as e:
        print(f"Erro ao adicionar o produto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/app', methods=['GET'])
def verificar_produto():
    try:
        with sqlite3.connect('test.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT id,titulo, preco, url, created_at FROM test''')
            produtos = c.fetchall()
        return jsonify ({'produtos': produtos}), 200

    except Exception as e:
        print(f"Erro ao adicionar o produto: {e}")
        return jsonify({'error': str(e)}), 500
