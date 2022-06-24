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



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config['suppress_callback_exceptions'] = True



app.layout = html.Div([

    navbar.navbar,
    html.Br(),
    dbc.Col([
        dcc.Tabs(id="tabs", value='tab_option', children=[
        dcc.Tab(label='Visualization', value='tab_visualization'),
        dcc.Tab(label='Load', value='tab_load'),
    ]),
    ]),
    dbc.Col([
        html.Div(id='tab_general')
    ]),
    #content.content,

    

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





@app.callback(Output('tab_general', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab_visualization':
        return content.content
    elif tab == 'tab_load':
        return dbc.Col(["Hola Mundo"])

if __name__ == '__main__':
    app.run_server(port= 5050, debug=True)