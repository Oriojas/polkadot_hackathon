import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import pyodbc

server = 'esp8266.cnwuu2sdaqvk.us-east-1.rds.amazonaws.com'
database = 'esp8266'
username = 'admin'
password = 'Esp_8266*'
driver= '{ODBC Driver 17 for SQL Server}'

# consulta a la base de datos
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    sql_query = f'SELECT * FROM dbo.registro_h_t'
    DF = pd.read_sql(sql_query, conn)

DF['FECHA'] = pd.to_datetime(DF['FECHA'])
end = max(DF['FECHA'])
init = end - datetime.timedelta(hours=1)
print(init)

DF = DF[DF['FECHA'] > init]

fig = make_subplots(2, 1)
fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['HUMEDAD'][DF['ORIGEN'] == 'Sensor1'],
                         name='Humedad (Sensor1)',
                         mode='lines+markers'), 1, 1)
fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['TEMPERATURA'][DF['ORIGEN'] == 'Sensor1'],
                         name='Temperatura (Sensor1)',
                         mode='lines+markers',
                         marker=dict(size=8,
                                     symbol='hourglass')), 1, 1)

fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['HUMEDAD'][DF['ORIGEN'] == 'Sensor2'],
                         name='Humedad (Sensor2)',
                         mode='lines+markers'), 2, 1)
fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['TEMPERATURA'][DF['ORIGEN'] == 'Sensor2'],
                         name='Temperatura (Sensor2)',
                         mode='lines+markers',
                         marker=dict(size=8,
                                     symbol='hourglass')), 2, 1)

template = 'plotly_white'
fig.update_layout(template=template, title="Temperatura C, Humedad %")
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
            <h2>Datos sensores, una hora atrás</h2>
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
