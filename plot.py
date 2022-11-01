import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import pyodbc

SERVER = os.environ["SERVER"]
DATABASE = os.environ["DATABASE"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DRIVER = os.environ["DRIVER"]

# consulta a la base de datos
with pyodbc.connect('DRIVER=' + DRIVER +';SERVER=tcp:' + SERVER + ';PORT=1433;DATABASE=' + DATABASE +';UID=' + USERNAME + ';PWD=' + PASSWORD) as conn:
    sql_query = f'SELECT * FROM polkadothack.dbo.registro_co2'
    DF = pd.read_sql(sql_query, conn)

DF['DATE_C'] = pd.to_datetime(DF['DATE_C'])
end = max(DF['DATE_C'])
init = end - datetime.timedelta(hours=1)
print(init)

DF = DF[DF['DATE_C'] > init]

fig = go.Figure(data=go.Scatter(x=DF['DATE_C'],
                                y=DF['CO2'][DF['ORIGIN'] == 'Sensor'],
                                name='CO2 (Sensor)',
                                mode='lines',
                                line_color='rgb(230,0,122)'))

template = 'plotly_white'
fig.update_layout(template=template, title="PPM CO2")
# fig.show()

# convert it to JSON
fig_json = fig.to_json()

# a simple HTML template
template = 'var plotly_data = {}'

# write the JSON to the HTML template
with open('templates/plots/new_plot.txt', 'w', encoding='utf-8') as f:
    f.write(template.format(fig_json))
