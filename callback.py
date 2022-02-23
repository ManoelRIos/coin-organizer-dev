from turtle import color
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
df = pd.read_csv("db/db.csv")



app.layout = html.Div([
  
  html.Div([
    dcc.Dropdown(
      df["Categoria"].unique(),
      'recebido',
     id = "x_column"
    ),
  
    dcc.Graph(id="graphic")
  
    ])
])



@app.callback(Output("graphic", "figure"),
              Input("x_column", "value"))

def update_graph(x_column):
  
  fig = px.scatter(x = df[df['Categoria'] == x_column['Value']], y = 'Valor', color = x_column)
  
  
  
  return fig


if __name__ == '__main__':
    app.run_server(debug=True)
