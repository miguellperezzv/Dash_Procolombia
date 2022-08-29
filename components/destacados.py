import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output
from logica.controlador import  actividades
from logica import controlador, controlador_pais_destacado
from dash import dash_table
from datetime import datetime as dt, date


dropdowns = dbc.Col([


    dbc.Col([
        html.P(html.B("Seleccione un país: ")),  
    ]),
    
    dbc.Col([
        dcc.Dropdown(
                #options=[{'label': t, 'value': t} for t in test], 
                #value = graficos.getCountries()[0],  
                options = ["estados_unidos", "espa��a", "chile", "mexico", "panama"],
                value = "estados_unidos",
                clearable=False,
                id='dropdown_country_destacado',
            ),
    ], lg=10, md=12),
    html.Br(),
    
    
] ,className="dropdowns")


content = html.Div(
    [
        
        
        dropdowns,
        
        
        html.Hr(),
        html.H2('Actividades de Promoción Turística: Nivel de Influencia por país', style={"text-align":"center"}, id = "lblInfluenceDestacado"),
        
       dcc.Loading(
                    id="ls-loading-2_region",
                    children=[
                html.Hr(),

                dbc.Row([
                    html.H4('Principales actividades de promoción', style={"text-align":"center"}),
                    html.P("La tabla muestra al usuario en que mes se espera que las actividades de promoción tengan efecto, ordenado de mayor a menor siendo la primera la actividad de promoción que más impacto tiene en el país junto con el período respectivo", style={'margin-left' : "100px",'margin-right' : "100px"  }),
                dbc.Col([

                ],lg=5, md=12, id="influence_table2_destacado", style={'margin-left' : "15px"})
                ], justify="center"),
        html.Br(),
        html.Hr(),
        html.Br(),

                dbc.Row([
                    
                   html.H4('Nivel de impacto y tiempos de efecto', style={"text-align":"center"}),
                    html.P("La tabla muestra al usuario en que mes se espera que las actividades de promoción tengan efecto, además de que muestra en orden las actividades de promoción que tienen mayor impacto", style={'margin-left' : "100px",'margin-right' : "100px"  }),
                    dbc.Col([
                        
                        #summary.details_table
                ],lg=5, md=12, id="influence_table_destacado", style={'margin-left' : "15px"}),
                ], justify="center" ),

                
            
                
                ],
                    type="circle",
                ),


        html.Hr(),
        html.H2('Resumen General por', style={"text-align":"center"}, id="lblGeneralSummaryDestacado"),
          
        html.Div([
    dbc.Row([
        dbc.Col([dcc.Graph(id="graph_barplot_destacado")], lg=9, md=12 ),
        dbc.Col([
            dbc.Row(html.P(html.B("Seleccione las actividades de promoción: "))),
       
            dcc.Dropdown(
                options=controlador.actividades,
                value=controlador.actividades[0]["value"],
                #options=controlador.getActividades(),
                #value=controlador.getActividades(),
                clearable=False,
                id="dropdown_promotion_activity_destacado",
                multi=True
            ),
        dbc.Row(html.P(html.B("Seleccione rango inicial - final: "))),
        dbc.Row([
            dbc.Col([
                dcc.DatePickerRange(
                id = "datapicker_destacado",
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
        dbc.Col([dcc.Graph(id="graph_pasajeros_pais_destacado")]),
        dbc.Col([ dcc.Graph(id="graph_hub_destacado")])
    ])
])
        
       
        
    ],
    className="contentDiv"
    #style=style.CONTENT_STYLE
)


'''
@callback(
    Output("graph_prophet_destacado", "figure"), 
    Input("dropdown_country_destacado", "value"),
    )

def displayProphet(country):
    table_activities, mejor_rezago = controlador_pais_destacado.tablas_actividades_destacadas(country)
    rezagos = int(mejor_rezago.numero)
    fig, table1, table2 = controlador.prophet(country, rezagos)

    return fig
'''

@callback(
    Output("influence_table_destacado", "children"),
    Output("influence_table2_destacado", "children"),
    
    Input("dropdown_country_destacado", "value"),
    #Input("slider_pais_destacado", "value")
)
def display_influence_table(pais):
    table_activities, mejor_rezago = controlador_pais_destacado.tablas_actividades_destacadas(pais)
    rezagos = int(mejor_rezago.numero)
    table = controlador_pais_destacado.tablas_importancia_pais_destacado_rezagos(pais,rezagos)
    
    return dash_table.DataTable(table.to_dict('records'), [{"name": i, "id": i} for i in table.columns]), dash_table.DataTable(table_activities.to_dict('records'), [{"name": i, "id": i} for i in table_activities.columns])


@callback(
    Output("lblGeneralSummaryDestacado", "children"),
    #Output("lblVisitorsDestacado", "children"),
    Output("lblInfluenceDestacado", "children"),
    Input("dropdown_country_destacado", "value"),
)
def reloadTitles(country):
    return "Resumen General "+ "("+ country.capitalize()+")",    "Actividades de promoción turística: Nivel de Influencia en (" + country.capitalize()+")"

@callback(
    Output("graph_hub_destacado", "figure"),
    Output("graph_pasajeros_pais_destacado", "figure"),
    Output("graph_barplot_destacado", "figure"),
    #Input ('dropdown_region', 'value'),
    Input ('dropdown_country_destacado', 'value'),
    Input('dropdown_promotion_activity_destacado', "value"),
    Input('datapicker_destacado', 'start_date'),
    Input('datapicker_destacado', 'end_date')
)
def generateGeneralGraphs(pais, actividades,inicio,fin):
    #start_date = dt(2012, 1, 1)
    #end_date = dt(2020, 12, 1)
    print(actividades)
    start_date = dt.strptime(inicio, '%Y-%m-%d')
    end_date = dt.strptime(fin, '%Y-%m-%d')
    region = controlador.getRegion(pais)
    print("REGION "+ region+ "fin ")
    #return controlador.display_map_single_country(start_date,end_date, region), controlador.display_time_series(None,[pais], start_date,end_date), controlador.display_barplot([pais],actividades, start_date,end_date)
    return  controlador.display_map_single_country(start_date,end_date, pais),controlador.display_time_series([pais], start_date,end_date), controlador.display_barplot([pais],actividades, start_date,end_date)