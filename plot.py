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

fig = make_subplots(1, 1)
fig.add_trace(go.Scatter(x=DF['DATE_C'],
                         y=DF['CO2'][DF['ORIGIN'] == 'Sensor'],
                         name='CO2 (Sensor)',
                         mode='lines+markers'), 1, 1)

template = 'plotly_white'
fig.update_layout(template=template, title="PPM CO2")
#fig.show()

# convert it to JSON
fig_json = fig.to_json()

# a simple HTML template
template = """<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>Datos ESP8266</title>
</head>
<body>
    <br>
    <div class="container px-4">
        <div class="mb-3 border rounded" style='padding: 16px;'>
            <h2>Datos sensor, una hora</h2>
        </div>
        <div class="mb-3 border rounded" style='padding: 16px;'>
            <div id='divPlotly'></div>
            <script>
                var plotly_data = {}
                Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
            </script>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
</body>
</html>"""

# write the JSON to the HTML template
with open('templates/new_plot.html', 'w') as f:
    f.write(template.format(fig_json))
