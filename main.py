import os
import uvicorn
from fastapi import FastAPI
from send_tk import sendTk
from substrateinterface import SubstrateInterface, Keypair

app = FastAPI()


@app.get('/balance/')
async def balance(wallet_balance: str):
    """
    this function get balance a wallet
    :param wallet_balance: wallet to gert balance
    :return: balance_off
    """

    try:
        substrate = SubstrateInterface(
            url="wss://westend-rpc.polkadot.io",
            ss58_format=42,
            type_registry_preset='westend')

        print("😀 local Substrate node running")

    except ConnectionRefusedError:
        print("⚠️ No local Substrate node running, try running 'start_local_substrate_node.sh' first")
        exit()

    result = substrate.query(
        module='System',
        storage_function='Account',
        params=[wallet_balance]
    )

    print(result)
    balance_off = int(result.value['data']['free'] / 10 ** 8) / 10000

    print(balance_off)

    return balance_off


@app.get('/send/')
async def send(wallet_send: str):
    """
    this function send token from main account to any wallet
    :param wallet_send: wallet destination
    :return: if transaction is ok True
    """

    amount = 0.1
    tx = sendTk().send(wallet_to_send=wallet_send, amount=amount)
    print(f'Tx is: {tx}')

    return tx

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)

