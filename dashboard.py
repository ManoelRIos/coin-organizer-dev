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
                 y = 'Valor', color=value_to_categoria_pie.index, title='Gastos por categoria')

#PLotando gráfico de barra valores x categoria
fig_pie = px.pie(value_to_categoria_pie,
                 values='Valor', names= value_to_categoria_pie.index, title='Gastos por categoria')

#Somando total recebido
total_recebido = co_db['Valor'].where(co_db['Valor'] > 0).sum()
#Somando total de gastos
total_gasto = co_db['Valor'].where( co_db['Valor'] < 0 ).sum() * (-1)

#Criando html do dashboard html-doc: https://dash.plotly.com/dash-html-components
app.layout = html.Div([
    html.Header(
        children=[
            html.Div(
                className="logo",
                children=[
                    html.Span("Coin"),
                    html.Span("Organize.")
                ]
            )
        ]
    ),
    
    html.Main(
        className="",
        children=[
            
            html.Div(
                className="total-values-cards",
                children=[
                    
                    html.Div(
                        className="total-gain card",
                        children=[
                            html.P("Ganhos"),
                            html.P("R$ " + str(total_recebido))                        
                        ]
                    ),
                    
                    html.Div(
                        className="total-gasto card",
                        children=[
                            html.P("Gastos"),
                            html.P("R$" + str(total_gasto))
                            
                        ]
                    )                                        
                ]            
            ),
            html.Div(
                className=("graph-cards"),
                children=[
                    dcc.Graph(
                        className="card",
                        id="bar-graph",
                        figure=geral_information_bar
                    ),
                    dcc.Graph(
                        className="card",
                        id="pie-graph",
                        figure=fig_bar
                    ),
                ]
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
