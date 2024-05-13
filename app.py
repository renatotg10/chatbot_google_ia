from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Caminho para o arquivo JSON
JSON_FILE = "mensagem.json"

# Função para ler o conteúdo do arquivo JSON
def ler_mensagem():
    try:
        with open(JSON_FILE, "r") as file:
            mensagem = json.load(file)
        return mensagem
    except FileNotFoundError:
        # Se o arquivo não existir, retornar uma mensagem vazia e criar o arquivo
        escrever_mensagem({"mensagem": ""})
        return {"mensagem": ""}

# Função para escrever a mensagem no arquivo JSON
def escrever_mensagem(mensagem):
    with open(JSON_FILE, "w") as file:
        json.dump(mensagem, file)

# Rota para servir o formulário HTML
@app.route('/formulario.html')
def formulario():
    return render_template('formulario.html')

# Rota para criar ou atualizar a mensagem
@app.route('/mensagem', methods=['POST'])
def criar_atualizar_mensagem():
    nova_mensagem = request.json
    escrever_mensagem(nova_mensagem)
    return jsonify({"mensagem": "Mensagem criada/atualizada com sucesso"})

# Rota para obter a mensagem
@app.route('/mensagem', methods=['GET'])
def obter_mensagem():
    mensagem = ler_mensagem()
    return jsonify(mensagem)

# Rota para deletar a mensagem
@app.route('/mensagem', methods=['DELETE'])
def deletar_mensagem():
    try:
        os.remove(JSON_FILE)
        return jsonify({"mensagem": "Mensagem deletada com sucesso"})
    except FileNotFoundError:
        return jsonify({"mensagem": "Nenhuma mensagem encontrada para deletar"})

if __name__ == '__main__':
    app.run(debug=True)
