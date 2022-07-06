import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output, State
from components import summary
import plotly.express as px
from assets import style
from logica import controlador
import time
from dash import dash_table
import seaborn as sns



dropdowns = dbc.Col([

    dbc.Col([
        html.P(html.B("Seleccione una región: ")),  
    ]),
    
    dbc.Col([
        dcc.Dropdown(
                id="dropdown_region",
                options = [{'label': t, 'value': t} for t in controlador.getRegions()],
                value = controlador.getRegions()[0],
                clearable=False,  
            ),
    ],lg=10, md=12),
    html.Br(),

    dbc.Col([
        html.P(html.B("Seleccione un país: ")),  
    ]),
    
    dbc.Col([
        dcc.Dropdown(
                #options=[{'label': t, 'value': t} for t in test], 
                #value = graficos.getCountries()[0],  
                options = [{'label': t, 'value': t} for t in controlador.getCountries()],
                value = controlador.getCountries()[0],
                clearable=False,
                id='dropdown_country',
            ),
    ], lg=10, md=12),

    dbc.Col([
        html.P(html.B("Elija cantidad de rezagos: ")),  
    ]),
    dbc.Col([
        dcc.Slider(0, 20, 1,
               value=5,
               id='slider_pais'
    )
    ]
    )
    
    
] ,className="dropdowns")


content = html.Div(
    [
        
        html.H2('Predicción de visitantes por País ', style={"text-align":"center"}, id = "lblVisitors"),
        html.Hr(),
        dbc.Row([
        dropdowns,
        dbc.Col([

            dcc.Loading(
                    id="ls-loading-2",
                    children=[dcc.Graph(id="graph_prophet"),],
                    type="circle",
                ),
            #dcc.Dropdown(['Enero', 'Febrero', 'Marzo'],id="dropdown-inner")
        ], lg =8, md = 12),
        ]
            
        ),
        
        html.Hr(),
        html.H2('Actividades de Promoción Turística: Nivel de Influencia por país', style={"text-align":"center"}, id = "lblInfluence"),

        
        
        dcc.Loading(
                    id="ls-loading-2",
                    children=[
                dbc.Row([
                    html.H3('Primeros 24 meses', style={"text-align":"center"}),
                    dbc.Col([
            
                        #summary.details_table
                ],lg=12, md=12, id="influence_table_head", style={'margin-left' : "15px"}),
                html.Br(),
                html.Hr(),
                html.H3('Ultimos 24 meses', style={"text-align":"center"}),
                dbc.Col([

                ],lg=12, md=12, id="influence_table_tail", style={'margin-left' : "15px"})
                ])
                
                ],
                    type="circle",
                ),
        
        
        html.Hr(),
        html.H2('Resumen General por país', style={"text-align":"center"}, id="lblGeneralSummary"),
          
        summary.general_summary
        
       
    ],
    className="contentDiv"
    #style=style.CONTENT_STYLE
)



@callback(
    Output("graph_prophet", "figure"), 
    Output("influence_table_head", "children"),
    Output("influence_table_tail", "children"),
    Input("dropdown_country", "value"),
    Input("slider_pais", "value")
    )

def displayProphet(country, slider):
    print("Displaying prophet")
    fig,table_head, table_tail = controlador.prophet(country, slider)
    
    #return fig, sns.heatmap(table_head, annot=True), sns.heatmap(table_tail, annot=True)

    return fig, dash_table.DataTable(table_head.to_dict('records'), [{"name": i, "id": i} for i in table_head.columns]),dash_table.DataTable(table_tail.to_dict('records'), [{"name": i, "id": i} for i in table_tail.columns]),

@callback(
    Output("dropdown_country", "options"),
    Output("dropdown_country", "value"),
    Input("dropdown_region", "value")
)
def loadDropdownCountries(region):
    options = controlador.getCountriesByRegion(region)
    return options, options[0]



@callback(
    Output("influence_table", "children"),
    Output("influence_table2", "children"),
    Input("dropdown_region", "value")
)
def display_influence_table(hub):
    table, table_activities = controlador.tabla_influencia_variable(hub, 2) 
    return dash_table.DataTable(table.to_dict('records'), [{"name": i, "id": i} for i in table.columns]), dash_table.DataTable(table_activities.to_dict('records'), [{"name": i, "id": i} for i in table_activities.columns])

@callback(
    Output("lblGeneralSummary", "children"),
    Output("lblVisitors", "children"),
    Output("lblInfluence", "children"),
    Input("dropdown_country", "value"),
    Input("dropdown_region", "value")
)
def reloadTitles(country, region):
    return "Resumen General "+ "("+ country+")",  "Predicción de visitantes (" + country+")",  "Actividades de Promoción Turística: Nivel de Influencia en (" + country+")"