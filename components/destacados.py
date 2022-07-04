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
        html.P(html.B("Select a Country: ")),  
    ]),
    
    dbc.Col([
        dcc.Dropdown(
                #options=[{'label': t, 'value': t} for t in test], 
                #value = graficos.getCountries()[0],  
                options = ["usa", "españa", "chile", "mexico", "panama"],
                value = "usa",
                clearable=False,
                id='dropdown_country_destacado',
            ),
    ], lg=10, md=12),
    
    
] ,className="dropdowns")


content = html.Div(
    [
        
        html.H2('Visitors Predicitions (by Country)', style={"text-align":"center"}, id = "lblVisitorsDestacado"),
        html.Hr(),
        dbc.Row([
        dropdowns,
        dbc.Col([
           dcc.Graph(id="graph_prophet_destacado"),
            #dcc.Dropdown(['Enero', 'Febrero', 'Marzo'],id="dropdown-inner")
        ], lg =8, md = 12),
        ]
            
        ),
        
        html.Hr(),
        html.H2('Touristic promotion activities: Level of Influence by Country', style={"text-align":"center"}, id = "lblInfluenceDestacado"),
        dbc.Col([
            
            details_table
        ],lg=9, md=12),
        html.Hr(),
        html.H2('General Summary by country', style={"text-align":"center"}, id="lblGeneralSummaryDestacado"),
          
        dbc.Row([
    dbc.Col([
        #html.P(html.B("Select a promotion activity: "))
        dbc.Row([
            dcc.Graph(id="graph-inner"),
        ])

    ],lg=9, md=9, id="col_summary"), 
    dbc.Col([
        dbc.Row(html.P(html.B("Select a promotion activity: "))),
       
            dcc.Dropdown(
                options=['Agenda comercial de turismo', 'Agendas de Cooperación', 'Capacitaciones y presentaciones de destino', 'FAM - PRESS Trips', 'Feria internacional de Turismo', 'Macrorruedas y Encuentros Comerciales', 'Primera Visita', 'Entrega informacion valor agregado', 'Otras Acciones promocion turismo', 'Preparación y adecuación '],
                value="Agendas de Cooperación",
                clearable=False,
                id="dropdown_promotion_activity_destacado",
                multi=True
            ),
        
    ],lg=3, md=3),
])
        
        #content_first_row,
        #content_second_row,
        #content_third_row,
        #content_fourth_row,
        
    ],
    className="contentDiv"
    #style=style.CONTENT_STYLE
)



@callback(
    Output("graph_prophet_destacado", "figure"), 
    Input("dropdown_country_destacado", "value")
    )

def displayProphet(country):
    print(country)
    print("Displaying prophet")
    fig = controlador.prophet(country)
    return fig



@callback(
    Output("lblGeneralSummaryDestacado", "children"),
    Output("lblVisitorsDestacado", "children"),
    Output("lblInfluenceDestacado", "children"),
    Input("dropdown_country_destacado", "value"),
)
def reloadTitles(country):
    return "General Summary "+ "("+ country+")",  "Visitors Predicitions (" + country+")",  "Touristic promotion activities: Level of Influence in (" + country+")"

