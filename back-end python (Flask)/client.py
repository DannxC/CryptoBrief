import requests
from urllib.parse import urljoin
from time import sleep

BASE_URL = 'http://localhost:8000'

def get_status(wallet_id: str) -> int:
    '''
        // State constants:
        CLOSED = 0;
        CONNECTING = 1;
        SYNCING = 2;
        READY = 3;
        ERROR = 4;
        PROCESSING = 5;
    '''
    response = requests.get(urljoin(BASE_URL, '/wallet/status'), headers={'x-wallet-id': wallet_id})
    data = response.json()
    return data.get('statusCode')


def wait_until_ready(wallet_id: str):
    while True:
        status = get_status(wallet_id)
        if status == 3 or status == 4:
            break
        sleep(1)


def start_wallet(wallet_id: str, seed_key: str) -> bool:
    '''
        Start a wallet then wait until it is ready
    '''
    response = requests.post(urljoin(BASE_URL, '/start'), data={'wallet-id': wallet_id, 'seedKey': seed_key})
    data = response.json()
    if data.get('success'):
        wait_until_ready(wallet_id)
    return data


def get_address_info(wallet_id: str, address: str, token: str = '00') -> dict:
    response = requests.get(
        urljoin(BASE_URL, '/wallet/address-info'),
        headers={ 'x-wallet-id': wallet_id },
        params={ 'address': address, 'token': token }
    )
    data = response.json()
    return data


def get_address_index(wallet_id: str, address: str) -> dict:
    response = requests.get(
        urljoin(BASE_URL, '/wallet/address-index'),
        headers={ 'x-wallet-id': wallet_id },
        params={ 'address': address }
    )
    data = response.json()
    return data


def get_addresses(wallet_id: str) -> dict:
    response = requests.get(
        urljoin(BASE_URL, '/wallet/addresses'),
        headers={ 'x-wallet-id': wallet_id },
    )
    data = response.json()
    return data


def get_tx_history(wallet_id: str, limit: int = None):
    params = {}
    if limit:
        params['limit'] = limit
    response = requests.get(
        urljoin(BASE_URL, '/wallet/tx-history'),
        headers={ 'x-wallet-id': wallet_id },
        params=params,
    )
    data = response.json()
    return data

def get_wallet_balance(wallet_id: str, token: str = '00') -> dict:
    response = requests.get(
        urljoin(BASE_URL, '/wallet/balance'),
        headers={ 'x-wallet-id': wallet_id },
        params={ 'token': token }
    )
    data = response.json()
    return data


def create_custom_token(wallet_id: str, name: str, symbol: str, amount: int, destination: str = None):
    body = {
        'name': name,
        'symbol': symbol,
        'amount': amount,
    }
    if destination:
        body['address'] = destination

    response = requests.post(
        urljoin(BASE_URL, '/wallet/create-token'),
        headers={ 'x-wallet-id': wallet_id },
        json=body,
    )
    data = response.json()
    return data

def mint_token(wallet_id: str, token_uid: str, address: str, amount: int):
    response = requests.post(
        urljoin(BASE_URL, '/wallet/mint-tokens'),
        headers={ 'x-wallet-id': wallet_id },
        json={
            'token': token_uid,
            'address': address,
            'amount': amount,
        },
    )
    data = response.json()
    return data

def melt_token(wallet_id: str, token_uid: str, amount: int):
    response = requests.post(
        urljoin(BASE_URL, '/wallet/melt-tokens'),
        headers={ 'x-wallet-id': wallet_id },
        json={
            'token': token_uid,
            'amount': amount,
        },
    )
    data = response.json()
    return data

def simple_send_tokens(wallet_id: str, address: str, value: int, token: str = '00') -> dict:
    response = requests.post(
        urljoin(BASE_URL, '/wallet/simple-send-tx'),
        headers={ 'x-wallet-id': wallet_id },
        json={
            'address': address,
            'value': value,
            'token': token,
        },
    )
    data = response.json()
    return data