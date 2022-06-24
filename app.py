import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from app import sidebar
from components import content, navbar
from logica import  controlador
import plotly.express as px
from assets import style
import numpy as np



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.config['suppress_callback_exceptions'] = False



app.layout = html.Div([
    navbar.navbar,
    content.content,
    

], className="principalDiv")



"""
###En dado caso que no funcione el callback en el archivo content
@app.callback(
    Output("graph-inner", "figure"), 
    #Input("dropdown-country", "value"))
    Input("dummy", "children"))

def displayProphet(country):
    print(country)
    print("Displaying prophet")
    fig = graficos.prophet(country)
    return fig
"""

@app.callback(
    Output('lblGeneralSummary', 'children'),
    Input("select-country", "value")
)
def selectedCountry(country):
    print(country)
    return "General Summary ("+str(country)+")"


@app.callback(
    Output("dropdown-country", "options"),
    Output("dropdown-country", "value"),
    Input("dropdown-region", "value")
)
def loadDropdownCountries(region):
    options = controlador.getCountriesByRegion(region)
    return options, options[0]


if __name__ == '__main__':
    app.run_server(port= 5050, debug=True)