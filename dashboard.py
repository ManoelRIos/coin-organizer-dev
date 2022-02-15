from turtle import width
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

app = Dash(__name__)

#Abrindo base de dados em csv
co_db = pd.read_csv("co_db.csv")

#Somando total recebido
total_recebido = round(co_db['Valor'].where(co_db['Valor'] > 0).sum(), 2)
#Somando total de gastos
total_gasto =round(co_db['Valor'].where( co_db['Valor'] < 0 ).sum() * (-1), 2)
#Sobra do mês
sobra_caixa = total_recebido - total_gasto
#Criando dataframe com dados de gastos totais, ganhos totais e sobras
total = pd.DataFrame({'Total': ['Gasto', 'Ganho','Sobra'],
                      'Valor':[total_gasto, total_recebido, sobra_caixa]})

fig_total_relation_hist = px.histogram(total,
                                       x="Total",
                                       y="Valor",
                                       color="Total",
                                       width=310, height=300)

fig_total_relation_pie = px.pie(total, values='Valor', names='Total', width=310, height=300, title='Total de ganhos e gastos %')

#Plotando gráfico de barra com os dados gerais valor x data
geral_information_bar = px.bar(co_db,
                               x = 'Data',
                               y = 'Valor', 
                               color = 'Categoria',
                               width=1920
                               )

#plotando gráfico de torta com valores x categoria
value_to_categoria_pie = co_db.groupby(by = 'Categoria').sum()

#PLotando gráfico de barra valores x categoria
fig_bar = px.bar(value_to_categoria_pie, 
                 x = value_to_categoria_pie.index,
                 y = 'Valor',
                 color=value_to_categoria_pie.index,
                 title='Gastos por categoria',
                 height=720)

#PLotando gráfico de torta valores x categoria
fig_pie = px.pie(value_to_categoria_pie,
                 values='Valor',
                 names= value_to_categoria_pie.index, 
                 width=310, height=300,
                 title='Gastos por categoria')

value_to_categoria_pie['Color'] = np.where(value_to_categoria_pie['Valor'] > 0, '#2eb873', '#EF553B')



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
                        className="total-values card",
                        children=[
                            html.Div(
                                className="total-gain box-card",
                                children=[
                                    html.P("Ganhos"),
                                    html.P("R$ " + str(total_recebido))   
                                ]
                            ),
                            html.Div(
                                className="total-gasto box-card",
                                children=[
                                    html.P("Gastos"),
                                    html.P("R$" + str(total_gasto))                                    
                                ]                            
                            )
                        ]
                    ),                                                                
                    dcc.Graph(
                        className="fig-total-relation-hist graph-card",                                    
                        figure=fig_total_relation_hist            
                    ),
                    dcc.Graph(
                        className="fig-total-reltion-pie graph-card",
                        figure=fig_total_relation_pie
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
                    
                    dcc.Graph(
                        className="card",
                        config = {'displayModeBar': False},
                        figure={
                            'data': [go.Bar(                                
                                x = value_to_categoria_pie.index,
                                y = value_to_categoria_pie['Valor'], 
                                text = value_to_categoria_pie['Valor'],
                                texttemplate = 'R$' + '%{text:,.0f}',
                                marker = dict(color  = value_to_categoria_pie['Color'] ),
                                width = 0.5,                                
                                textfont = dict(
                                    family = 'Arial Black',
                                    size = 14,
                                    color = 'black',                                
                                ),
                                orientation = 'v',
                                hoverinfo = 'skip'                                                          
                            )],
                            'layout': go.Layout(                                                                                 
                                plot_bgcolor = 'rgba(50,150,200,0.13)',
                                title = {'text': 'Valor x Categoria',
                                         'y': 0.97,
                                         'x': 0.5,
                                         'xanchor':'center',
                                         'yanchor': 'top'},
                                titlefont = {'color': 'black',
                                             'size': 15},  
                                margin = dict(r = 20, t = 50, b = 50),                                
                                xaxis = dict(title = '<br></br>',
                                             visible = True,
                                             color = 'white',
                                             showline=True,                                            
                                             showgrid = False,
                                             showticklabels = True,
                                             linecolor = 'white',
                                             linewidth = 1,
                                             ticks = '',
                                             tickfont = dict(family = 'Arial',
                                                             size = 12,
                                                             color= 'black')                                             
                                ),
                                yaxis = dict(showgrid = False,
                                             linecolor = 'white',
                                             linewidth = 1,
                                             ticks = '',
                                             tickfont = dict(
                                                 family = 'Aial',
                                                 size = 12,
                                                 color = 'white'
                                            )
                                )                                                               
                            )                                     
                        }
                    )                
                ]
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    