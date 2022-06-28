import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output, State
from components.summary import details_table, general_summary

import plotly.express as px
from assets import style
from logica import controlador



dropdowns = dbc.Col([

    dbc.Col([
        html.P(html.B("Select a Region: ")),  
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
        html.P(html.B("Select a Country: ")),  
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
    html.P("alemania", id="dummy"),
    
] ,className="dropdowns")


content = html.Div(
    [
        
        html.H2('Visitors Predicitions (by Region)', style={"text-align":"center"}, id = "lblVisitors"),
        html.Hr(),
        dbc.Row([
        dropdowns,
        dbc.Col([
           dcc.Graph(id="graph-inner"),
            #dcc.Dropdown(['Enero', 'Febrero', 'Marzo'],id="dropdown-inner")
        ], lg =8, md = 12),
        ]
            
        ),
        
        html.Hr(),
        html.H2('Touristic promotion activities: Level of Influence by region', style={"text-align":"center"}, id = "lblInfluence"),
        dbc.Col([
            
            details_table
        ],lg=9, md=12),
        html.Hr(),
        html.H2('General Summary by country', style={"text-align":"center"}, id="lblGeneralSummary"),
          
        general_summary,
        
        #content_first_row,
        #content_second_row,
        #content_third_row,
        #content_fourth_row,
        
    ],
    className="contentDiv"
    #style=style.CONTENT_STYLE
)



@callback(
    Output("graph-inner", "figure"), 
    #Input("dropdown-country", "value"))
    Input("dummy", "children"))

def displayProphet(country):
    print(country)
    print("Displaying prophet")
    fig = controlador.prophet(country)
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
    return "General Summary "+ "("+ country+")",  "Visitors Predicitions (" + region+")",  "Touristic promotion activities: Level of Influence in (" + region+")"