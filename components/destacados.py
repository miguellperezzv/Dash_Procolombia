import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output, State
from logica.controlador import  actividades

import plotly.express as px
from assets import style
from logica import controlador
from dash import dash_table



dropdowns = dbc.Col([


    dbc.Col([
        html.P(html.B("Seleccione un país: ")),  
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
        
        html.H2('Predicción de visitantes', style={"text-align":"center"}, id = "lblVisitorsDestacado"),
        html.Hr(),
        dbc.Row([
        dropdowns,
        dbc.Col([

            dcc.Loading(
                    id="ls-loading-2_destacado",
                    children=[dcc.Graph(id="graph_prophet_destacado"),],
                    type="circle",
                ),
            #dcc.Dropdown(['Enero', 'Febrero', 'Marzo'],id="dropdown-inner")
        ], lg =8, md = 12),
        ]
            
        ),
        
        html.Hr(),
        html.H2('Actividades de Promoción Turística: Nivel de Influencia por país', style={"text-align":"center"}, id = "lblInfluenceDestacado"),
        
        dcc.Loading(
                    id="ls-loading-2_destacado",
                    children=[
                        dbc.Col([
            
                        #summary.details_table
                ],lg=9, md=12, id="influence_table_destacado"),
                    ],
                    type="circle",
                ),


        html.Hr(),
        html.H2('Resumen General por', style={"text-align":"center"}, id="lblGeneralSummaryDestacado"),
          
        dbc.Row([
    dbc.Col([
        #html.P(html.B("Select a promotion activity: "))
        dbc.Row([
            dcc.Graph(id="graph-inner"),
        ])

    ],lg=9, md=9, id="col_summary"), 
    dbc.Col([
        dbc.Row(html.P(html.B("Seleccione un grupo de actividades de promoción: "))),
       
            dcc.Dropdown(
                options=actividades,
                value=actividades[0]["label"],
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
    fig = controlador.prophet(country, 2)

    return fig

@callback(
    Output("influence_table_destacado", "children"),
    Input("dropdown_region_destacado", "value")
)
def display_influence_table(hub):
    table, table_activities = controlador.tabla_influencia_variable(hub, 2) 
    return dash_table.DataTable(table.to_dict('records'), [{"name": i, "id": i} for i in table.columns]), dash_table.DataTable(table_activities.to_dict('records'), [{"name": i, "id": i} for i in table_activities.columns])


@callback(
    Output("lblGeneralSummaryDestacado", "children"),
    Output("lblVisitorsDestacado", "children"),
    Output("lblInfluenceDestacado", "children"),
    Input("dropdown_country_destacado", "value"),
)
def reloadTitles(country):
    return "Resumen General "+ "("+ country+")",  "Predicción de visitantes (" + country+")",  "Actividades de promoción turística: Nivel de Influencia en (" + country+")"

