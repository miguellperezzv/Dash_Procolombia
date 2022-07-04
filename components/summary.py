from subprocess import call
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
import pandas as pd
from dash import html,  callback
from dash.dependencies import Input, Output
from logica import controlador
from datetime import datetime as dt
from datetime import date

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
details_table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])



general_summary = dbc.Row([
    dbc.Col([
        dbc.Row([
            dcc.Graph(id="graph_hub"),
        ])

    ],lg=9, md=9), 
    dbc.Col([
        dbc.Row(html.P(html.B("Seleccione las actividades de promoción: "))),
       
            dcc.Dropdown(
                options=['Agenda comercial de turismo', 'Agendas de Cooperación', 'Capacitaciones y presentaciones de destino', 'FAM - PRESS Trips', 'Feria internacional de Turismo', 'Macrorruedas y Encuentros Comerciales', 'Primera Visita', 'Entrega informacion valor agregado', 'Otras Acciones promocion turismo', 'Preparación y adecuación '],
                value="Agendas de Cooperación",
                #options=controlador.getActividades(),
                #value=controlador.getActividades(),
                clearable=False,
                id="dropdown_promotion_activity",
                multi=True
            ),
        dbc.Row(html.P(html.B("Seleccione rango inicial - final: "))),
        dbc.Row([
            dbc.Col([
                dcc.DatePickerRange(
                id = "datapicker",
                start_date = date(2012, 1, 1), 
                end_date=date(2022, 6, 1),
                min_date_allowed="2012-01",
                display_format='YYYY-MM',
                start_date_placeholder_text='YYYY-MM'
            )], style={"width":"30px" ,"height":"","font-size":"10px"}),       
            
            
        ]),
        
        
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

@callback(
    Output("graph_hub", "figure"),
    Input ('dropdown_region', 'value'),
    Input('datapicker', 'start_date'),
    Input('datapicker', 'end_date')
)
def generateGraphHub(region,inicio,fin):
    #start_date = dt(2012, 1, 1)
    #end_date = dt(2020, 12, 1)
    start_date = dt.strptime(inicio, '%Y-%m-%d')
    end_date = dt.strptime(fin, '%Y-%m-%d')
    return controlador.display_map_single_country(start_date,end_date, region)
