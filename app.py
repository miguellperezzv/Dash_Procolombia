import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from app import sidebar
from components import content, destacados, navbar, region
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
        dcc.Tab(label='Visualización por países', value='tab_paises'),
        dcc.Tab(label='Visualización por Hubs', value='tab_hubs'),
        dcc.Tab(label='Países destacados', value='tab_destacados'),
        dcc.Tab(label='Load', value='tab_load'),
        

    ]),
    ]),
    dbc.Col([
        html.Div(id='tab_general')
    ]),
    #content.content,

    

], className="principalDiv")






@app.callback(Output('tab_general', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab_paises':
        return content.content
    elif tab == 'tab_load':
        return dbc.Col(["Hola Mundo"])
    elif tab == "tab_destacados":
        return destacados.content
    elif tab == "tab_hubs":
        return region.content

if __name__ == '__main__':
    #app.run_server(port= 5050, debug=True)
    
    app.run_server(host='0.0.0.0', port= 9000, debug=True)