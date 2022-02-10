from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

#Abrindo base de dados em csv
co_db = pd.read_csv("co_db.csv")

#Plotando gráfico de barra com os dados gerais valor x data
geral_information_bar = px.bar(co_db, x = 'Data', y = 'Valor', color = 'Categoria')


#plotando gráfico de torta com valores x categoria
value_to_categoria_pie = co_db.groupby(by = 'Categoria').sum() 

fig_bar = px.bar(value_to_categoria_pie, x = value_to_categoria_pie.index,
                 y = 'Valor', color=value_to_categoria_pie.index, title='Gastos por categoria'
                 )
fig_pie = px.pie(value_to_categoria_pie, values='Valor', names= value_to_categoria_pie.index, title='Gastos por categoria')

#Criando html do dashboard
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
                figure=geral_information_bar
            ),
            dcc.Graph(
                id="pie-graph",
                figure=fig_bar
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
