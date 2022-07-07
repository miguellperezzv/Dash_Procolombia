import dash_bootstrap_components as dbc
from dash import html,  callback, dash_table, dcc
import pandas as pd
from dash.dependencies import Input, Output
from logica import controlador
from datetime import datetime as dt, date


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
details_table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
#details_table = controlador.tabla_influencia_variable()



general_summary = html.Div([
    dbc.Row([
        dbc.Col([dcc.Graph(id="graph_hub")], lg=9, md=12 ),
        dbc.Col([
            dbc.Row(html.P(html.B("Seleccione las actividades de promoción: "))),
       
            dcc.Dropdown(
                options=controlador.actividades,
                value=controlador.actividades[0]["label"],
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
        ], lg=3, md=12)
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id="graph_pasajeros_pais")]),
        dbc.Col([ dcc.Graph(id="graph_barplot")])
    ])
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
    return controlador.display_map_single_country(start_date,end_date, region), controlador.display_time_series(None,[pais], start_date,end_date), controlador.display_barplot([pais],actividades, start_date,end_date)

