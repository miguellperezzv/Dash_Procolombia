from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
import pandas as pd
from dash import html,  callback
from dash.dependencies import Input, Output
from logica import controlador

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
details_table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])



general_summary = dbc.Row([
    dbc.Col([
        #html.P(html.B("Select a promotion activity: "))
        dbc.Col([
            #dcc.Graph(id="graph_1"),
            
        ])

    ],lg=9, md=9, id="col_summary"), 
    dbc.Col([
        dbc.Row(html.P(html.B("Select a promotion activity: "))),
       
            dcc.Dropdown(
                options=['Agenda comercial de turismo', 'Agendas de Cooperación', 'Capacitaciones y presentaciones de destino', 'FAM - PRESS Trips', 'Feria internacional de Turismo', 'Macrorruedas y Encuentros Comerciales', 'Primera Visita', 'Entrega informacion valor agregado', 'Otras Acciones promocion turismo', 'Preparación y adecuación '],
                value="Agendas de Cooperación",
                clearable=False,
                id="dropdown_promotion_activity",
                multi=True
            ),
        
    ],lg=3, md=3),
])


@callback(
    Output('col_summary', 'children'),
    Input('dropdown_promotion_activity', 'value'),
    Input('dropdown_country', 'value'),
)
def generateGeneralStats(activities, country):
    print(activities)
    print(country)
    #graficos
