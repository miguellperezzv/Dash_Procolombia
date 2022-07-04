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
#details_table = controlador.tabla_influencia_variable()

actividades = [         {'label':'Agenda comercial de turismo' , 'value' : 'x1'}, 
                        {'label' : 'Agendas de Cooperación', 'value' :'x2'}, 
                        {'label' : 'Capacitaciones y presentaciones de destino' , 'value' : 'x3'}, 
                        {'label': 'FAM - PRESS Trips','value' : 'x4'}, 
                        {'label':'Feria internacional de Turismo' , 'value' :'x5'}, 
                        {'label':'Macrorruedas y Encuentros Comerciales' ,'value' : 'x6'},
                        {'label':'Primera Visita', 'value' :'x7'}, 
                        {'label':'Entrega informacion valor agregado' ,'value' : 'x8'}, 
                        {'label':'Otras Acciones promocion turismo' ,'value' : 'x9'}, 
                        {'label':'Preparación y adecuación ','value' : 'x10'}]

general_summary = dbc.Row([
    dbc.Col([
        dbc.Row([
            dcc.Graph(id="graph_hub"),
        ]),
        dbc.Row([
            dcc.Graph(id="graph_pasajeros_pais"),
        ]),
        dbc.Row([
            dcc.Graph(id="graph_barplot"),
        ]),

    ],lg=9, md=9), 
    dbc.Col([
        dbc.Row(html.P(html.B("Seleccione las actividades de promoción: "))),
       
            dcc.Dropdown(
                options=actividades,
                value=actividades[0]["label"],
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
    Output("graph_pasajeros_pais", "figure"),
    Output("graph_barplot", "figure"),
    Input ('dropdown_region', 'value'),
    Input ('dropdown_country', 'value'),
    Input('dropdown_promotion_activity', "value"),
    Input('datapicker', 'start_date'),
    Input('datapicker', 'end_date')
)
def generateGeneralGraphs(region,pais, actividades,inicio,fin):
    #start_date = dt(2012, 1, 1)
    #end_date = dt(2020, 12, 1)
    start_date = dt.strptime(inicio, '%Y-%m-%d')
    end_date = dt.strptime(fin, '%Y-%m-%d')
    return controlador.display_map_single_country(start_date,end_date, region), controlador.display_time_series(None,[pais]), controlador.display_barplot([pais],actividades)

