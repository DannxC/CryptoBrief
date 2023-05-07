import client

# Definindo o token_uid para o token NEWSCoin (reputação)
token_uid = "00ac58b0d9a9f86e1ccdfcd4286d3258f486b843313979440b48b99c04c0f1f1"

# Lista de analistas com id, nome, endereço e votos
analysts_data = [
    {'id' : '1', 'name': 'Lisa', 'address': 'WRsDBWppk1auSTVR9EW3XtX7pCRZBp6vCg', 'votes': 0},
    #{'id' : '2', 'name': 'Ferroca', 'address': 'endereço 2', 'votes': 0}
    #{'id' : '3', 'name': 'Filé', 'address': 'endereço 3', 'votes': 0},
    # ...
]

# Lista de endereços de usuários que já votaram
user_that_voted = []



def get_balance(data, wallet_id):
    # Encontra o analista pelo ID fornecido
    analyst_id = data.get('id')
    analyst = find_analyst(analyst_id)

    if analyst:
        # Se o analista for encontrado, consulta o saldo do endereço do analista
        analyst_address = analyst['address']
        address_info = client.get_address_info(wallet_id, analyst_address, token_uid)
        balance = address_info.get('balance', 0)
        return {'analyst_balance' : balance}
    else:
        # Se o analista não for encontrado, retorna sucesso como False
        return {'success': False}



def get_analysts():
    # Retorna a lista de analistas
    return analysts_data



def reset_votes():
    # Limpa a lista de usuários que votaram e reseta a contagem de votos dos analistas
    user_that_voted.clear()
    for analyst in analysts_data:
        analyst['votes'] = 0
    return {'success': True, 'message': 'Votos resetados'}



def has_voted(user_address):
    # Verifica se o usuário já votou
    for user_add in user_that_voted:
        if user_add == user_address: return True
    return False

def find_analyst(id):
    # Encontra o analista pelo ID fornecido e retorna o objeto analista se encontrado, caso contrário retorna None
    for analyst in analysts_data:
        if analyst['id'] == id:
            return analyst
    return None

def vote_analyst(data, wallet_id):
    # Verifica se o usuário já votou
    user_address = data.get('user_address')
    if has_voted(user_address):
        return {'success': False, 'message': 'Usuário já votou'}

    # Encontra o analista pelo ID fornecido
    analyst_id = data.get('id')
    vote_value = 1
    analyst = find_analyst(analyst_id)

    # Se o analista for encontrado, adiciona um voto e faz mint de tokens NEWSCoin
    if analyst:
        # Faz mint de tokens NEWSCoin
        analyst_address = analyst['address']
        response = client.mint_token(wallet_id, analyst_address, 1, token_uid)
        # Atualiza a contagem de votos do analista e adiciona o usuário à lista de votantes
        analyst['votes'] += vote_value
        user_that_voted.append()
        
        return {'success': True, 'message': f'Analista votado com sucesso: {analyst}'}
    else:
        return {'success': False, 'message': 'Analista não encontrado'}
