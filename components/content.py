import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output
from components import summary
from logica import controlador
from dash import dash_table


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
    html.Br(),
    
    
    
] ,className="dropdowns")


content = html.Div(
    [
        
        dropdowns,
        
        
        html.Hr(),
        html.H2('Resumen General por país', style={"text-align":"center"}, id="lblGeneralSummary"),
        summary.general_summary,
        
        
        
          
        
        
       
    ],
    className="contentDiv"
    #style=style.CONTENT_STYLE
)



@callback(
    #Output("graph_prophet", "figure"), 
    Output("influence_table_tail", "children"),
    Input("dropdown_country", "value"),
    )

def displayProphet(country):
    print("Displaying prophet")
    rezagos = 6
    fig,table_head, table_tail = controlador.prophet(country, rezagos)
    
    #return fig, sns.heatmap(table_head, annot=True), sns.heatmap(table_tail, annot=True)

    return dash_table.DataTable(table_tail.to_dict('records'), [{"name": i, "id": i} for i in table_tail.columns]),

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
    #Output("lblVisitors", "children"),
    #Output("lblInfluence", "children"),
    Input("dropdown_country", "value"),
    Input("dropdown_region", "value")
)
def reloadTitles(country, region):
    return "Resumen General "+ "("+ country.capitalize()+")"