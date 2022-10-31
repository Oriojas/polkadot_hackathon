import os
import pyodbc
import uvicorn
from send_tk import sendTk
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from substrateinterface import SubstrateInterface

app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")
templates = Jinja2Templates(directory="templates")

SERVER = os.environ["SERVER"]
DATABASE = os.environ["DATABASE"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DRIVER = os.environ["DRIVER"]
TOKEN = os.environ["TOKEN"]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home_page/index.html", {
        "request": request
    })


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

        print("😀 last node running")

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
async def send(wallet_send: str, token: str):
    """
    this function send token from main account to any wallet
    :param wallet_send: wallet destination
    :return: if transaction is ok True
    """
    if token == TOKEN:
        amount = 0.1
        tx = sendTk().send(wallet_to_send=wallet_send, amount=amount)
        print(f'Tx is: {tx}')
    else:
        print(f'Not valid token {token}')
        tx = False

    return tx


@app.get('/data_co/')
async def data_co(co2: int, origin: str, wallet_send: str, token: str):
    """
    this function send data to data base and send token if co2 value up 800 ppm
    :param co2: int, value of ppm co2
    :param origin: str, is origin of data test or sensor
    :param wallet_send: str, wallet to send tokens
    :param token: uuid for endpoint
    :return: None
    """

    print(''.center(60, '='))
    print(f'ppm co2: {co2} , origen: {origin}')

    if token == TOKEN:
        if co2 > 800:
            amount = 0.1
            tx = sendTk().send(wallet_to_send=wallet_send, amount=amount)
            print(f'🤑 send {amount} to {wallet_send} is: {tx}')
        else:
            print(f'Valid token')

        # incert data in db
        with pyodbc.connect(
                'DRIVER=' + DRIVER + ';SERVER=tcp:' + SERVER + ';PORT=1433;DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD) as conn:
            with conn.cursor() as cursor:
                count = cursor.execute(
                    f"INSERT INTO polkadothack.dbo.registro_co2 (CO2, DATE_C, ORIGIN) VALUES ({co2}, DEFAULT, '{origin}');").rowcount
                conn.commit()
                print(f'Rows inserted: {str(count)}')

        print(''.center(60, '='))

    else:
        print(f'Not valid token {token}')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8086)
