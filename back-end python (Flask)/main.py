from flask import Flask, request, jsonify
import analysts
from client import start_wallet

# Iniciando a carteira com um ID e uma seed_key padrões
wallet_id = "def"
seed_key = "default"
response = start_wallet(wallet_id, seed_key)

# Verificando se a carteira foi iniciada com sucesso
if response.get("success"):
    print("Carteira iniciada com sucesso")
else:
    print("Erro ao iniciar a carteira:", response.get("message"))


# Iniciando o aplicativo Flask
app = Flask(__name__)

# Rota para obter o saldo de NEWSCoins de um analista específico
@app.route('/analyst/get_balance', methods=['GET'])
def get_balance():
    """
        INPUTS (JSON)
            'id'                id relativo ao analista que deseja-se saber o balance total de NEWSCoins
    """
    data = request.json
    result = analysts.get_balance(data, wallet_id)
    return jsonify(result)

# Rota para obter a lista de analistas
@app.route('/analyst/get_analysts', methods=['GET'])
def get_analysts():
    """
        NÃO HÁ INPUTS
    """
    data = request.json
    result = analysts.get_analysts(data, wallet_id)
    return jsonify(result)

# Rota para votar em um analista, atribuindo-lhe um NEWSCoin
@app.route('/analyst/vote_analyst', methods=['POST'])
def vote_analyst():
    """
        INPUTS (JSON)
            'user_address'      endereço do usuário que está tentando votar
            'id'                id relativo ao analista que foi escolhido para o voto
    """
    data = request.json
    result = analysts.vote_analyst(data, wallet_id)
    return jsonify(result)

# Rota para redefinir os votos e o saldo dos analistas
@app.route('/analyst/reset_votes', methods=['GET'])
def reset_votes():
    """
        NÃO HÁ INPUTS
    """
    data = request.json
    result = analysts.reset_votes(data, wallet_id)
    return jsonify(result)



# Inicializa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)