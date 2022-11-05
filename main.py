import os
import pyodbc
import uvicorn
import pandas as pd
from send_tk import sendTk
from get_balance import getBalance
from plot import plotSensor
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/img", StaticFiles(directory="img"), name="img")
templates = Jinja2Templates(directory="templates")

SERVER = os.environ["SERVER"]
DATABASE = os.environ["DATABASE"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DRIVER = os.environ["DRIVER"]
TOKEN = os.environ["TOKEN"]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    this function render front
    :param request:
    :return:
    """

    bal_obj = getBalance()
    w_1, _ = bal_obj.fit(wallet='5GcDVqDQZ5n2qhUmFSP4stJvqXppcmevVW8dVWrXFQUJKXHD')
    w_2, ln = bal_obj.fit(wallet='5D2fBKHgezt6pKKuXFo8Xse3sT9hZK5PtkJEyacozZJnVXZ3')

    plotSensor().plot(wallet_1=w_1, wallet_2=w_2)
    print(f'Plot OK!')

    with open('templates/plots/new_plot.txt', 'r', encoding='utf-8') as file:
        plot = file.readlines()
    return templates.TemplateResponse("home_page/index.html", {
        "request": request,
        "plot": str(plot[0]),
        'ln': ln
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
    this function send data to database and send token if co2 value up 800 ppm
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
            print(f'Invalid token')

        # insert data in db
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


@app.get('/data_co_bici/')
async def data_co(co2: int, origin: str, token: str):
    """
    this function send data to database and send token if co2 value up 800 ppm
    :param co2: int, value of ppm co2
    :param origin: str, is origin of data test or sensor
    :param token: uuid for endpoint
    :return: None
    """

    print(''.center(60, '='))
    print(f'ppm co2: {co2} , origen: {origin}')

    if token == TOKEN:

        # insert data in db
        with pyodbc.connect(
                'DRIVER=' + DRIVER + ';SERVER=tcp:' + SERVER + ';PORT=1433;DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD) as conn:
            with conn.cursor() as cursor:
                count = cursor.execute(
                    f"INSERT INTO polkadothack.dbo.co2_bici (CO2, DATE_C, ORIGIN) VALUES ({co2}, DEFAULT, '{origin}');").rowcount
                conn.commit()
                print(f'Rows inserted: {str(count)}')

        print(''.center(60, '='))

    else:
        print(f'Not valid token {token}')


@app.get('/query_co2_bici/')
async def query_co2_bici(rows: int, token: str):
    """
    this function test database
    :param rows: number of rows to query
    :param token: uuid for endpoint
    :return: json whit rows in rows param
    """
    if token == TOKEN:

        with pyodbc.connect(
                'DRIVER=' + DRIVER + ';SERVER=tcp:' + SERVER + ';PORT=1433;DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD) as conn:
            sql_query = f'SELECT * FROM ( SELECT *, ROW_NUMBER() OVER (ORDER BY DATE_C DESC) AS row FROM polkadothack.dbo.co2_bici ) AS alias WHERE row > 0 AND row <= {rows}'
            DF = pd.read_sql(sql_query, conn)

            json_out_put = DF.to_json()

            print('OK')

    else:
        print(f'Not valid token {token}')

    return json_out_put


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8086)
