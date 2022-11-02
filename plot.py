import os
import pyodbc
import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


SERVER = os.environ["SERVER"]
DATABASE = os.environ["DATABASE"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DRIVER = os.environ["DRIVER"]


class plotSensor:

    def __init__(self):
        """
        this class request database co2 info
        """

        with pyodbc.connect(
                'DRIVER=' + DRIVER + ';SERVER=tcp:' + SERVER + ';PORT=1433;DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD) as conn:
            sql_query = f'SELECT * FROM polkadothack.dbo.registro_co2'
            DF = pd.read_sql(sql_query, conn)

        DF['DATE_C'] = pd.to_datetime(DF['DATE_C'])
        end = max(DF['DATE_C'])
        init = end - datetime.timedelta(hours=1)
        print(init)

        self.DF = DF[DF['DATE_C'] > init]

    def plot(self, wallet_1, wallet_2):
        DF = self.DF

        balance_w = [wallet_1, wallet_2]
        names = ['grant', 'stake']

        fig = make_subplots(1, 2)

        fig.add_trace(go.Scatter(x=DF['DATE_C'],
                                 y=DF['CO2'][DF['ORIGIN'] == 'Sensor'],
                                 name='CO2 (Sensor)',
                                 mode='lines',
                                 line_color='rgb(230,0,122)'), 1, 1)

        fig.add_trace(go.Bar(name='Grant',
                             x=names,
                             y=balance_w,
                             marker_color='rgb(230,0,122)'), 1, 2)

        template = 'plotly_white'
        fig.update_layout(template=template, title="PPM CO2 and WALLET STATUS")
        # fig.show()

        # convert it to JSON
        fig_json = fig.to_json()

        # a simple HTML template
        template = 'var plotly_data = {}'

        # write the JSON to the HTML template
        with open('templates/plots/new_plot.txt', 'w', encoding='utf-8') as f:
            f.write(template.format(fig_json))


#if __name__ == '__main__':
#    plotSensor().plot(12, 5)
