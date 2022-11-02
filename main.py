import os
import pyodbc
import uvicorn
from send_tk import sendTk
from get_balance import getBalance
from plot import plotSensor
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

    bal_obj = getBalance()
    w_1 = bal_obj.fit(wallet='5GcDVqDQZ5n2qhUmFSP4stJvqXppcmevVW8dVWrXFQUJKXHD')
    w_2 = bal_obj.fit(wallet='5D2fBKHgezt6pKKuXFo8Xse3sT9hZK5PtkJEyacozZJnVXZ3')

    plotSensor().plot(wallet_1=w_1, wallet_2=w_2)
    print(f'Plot OK!')

    with open('templates/plots/new_plot.txt', 'r', encoding='utf-8') as file:
        plot = file.readlines()
    return templates.TemplateResponse("home_page/index.html", {
        "request": request,
        "plot": str(plot[0])
    })


@app.get('/balance/')
async def balance(wallet_balance: str):
    """
    this function get balance a wallet
    :param wallet_balance: wallet to gert balance
    :return: balance_off
    """

    bal_obj = getBalance()

    balance_off = bal_obj.fit(wallet=wallet_balance)

    return balance_off


@app.get('/send/')
async def send(wallet_send: str, token: str):
    """
    this function send token from main account to any wallet
    :param token:
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
        if co2 > 820:
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
