from ast import Div
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

app = Dash(__name__)


co_db = pd.read_csv("co_db.csv")

fig = px.bar(co_db, x = 'Data', y = 'Valor', color = 'Categoria')

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div("Plotly Dash", className="logo")
        ]
    ),
    
    html.Div(
        className="main",
        children=[
            dcc.Graph(
                id="bar-graph",
                figure=fig
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
