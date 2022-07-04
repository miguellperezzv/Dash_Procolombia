import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output, State
from components import summary
import plotly.express as px
from assets import style
from logica import controlador



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
    
    
] ,className="dropdowns")


content = html.Div(
    [
        
        html.H2('Predicción de visitantes por País ', style={"text-align":"center"}, id = "lblVisitors"),
        html.Hr(),
        dbc.Row([
        dropdowns,
        dbc.Col([
           dcc.Graph(id="graph_prophet"),
            #dcc.Dropdown(['Enero', 'Febrero', 'Marzo'],id="dropdown-inner")
        ], lg =8, md = 12),
        ]
            
        ),
        
        html.Hr(),
        html.H2('Actividades de Promoción Turística: Nivel de Influencia por país', style={"text-align":"center"}, id = "lblInfluence"),
        dbc.Col([
            
            summary.details_table
        ],lg=9, md=12),
        html.Hr(),
        html.H2('Resumen General por país', style={"text-align":"center"}, id="lblGeneralSummary"),
          
        summary.general_summary
        
       
    ],
    className="contentDiv"
    #style=style.CONTENT_STYLE
)



@callback(
    Output("graph_prophet", "figure"), 
    Input("dropdown_country", "value")
    )

def displayProphet(country):
    print(country)
    print("Displaying prophet")
    fig = controlador.prophet(country, 2)
    return fig

@callback(
    Output("dropdown_country", "options"),
    Output("dropdown_country", "value"),
    Input("dropdown_region", "value")
)
def loadDropdownCountries(region):
    options = controlador.getCountriesByRegion(region)
    return options, options[0]

@callback(
    Output("lblGeneralSummary", "children"),
    Output("lblVisitors", "children"),
    Output("lblInfluence", "children"),
    Input("dropdown_country", "value"),
    Input("dropdown_region", "value")
)
def reloadTitles(country, region):
    return "Resumen General "+ "("+ country+")",  "Predicción de visitantes (" + country+")",  "Actividades de Promoción Turística: Nivel de Influencia en (" + country+")"