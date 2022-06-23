import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from app import sidebar
from components import content, navbar
from logica import  graficos
import plotly.express as px
from assets import style
import numpy as np



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.config['suppress_callback_exceptions'] = False

"""
app.layout = html.Div( [
    html.Div([navbar.navbar]),
    html.Div([dcc.Graph(id="graph")]),
    html.Div([
         sidebar.sidebar,
         content.content
        ]),
    
    #html.Div([footer.footer]),
    
])

""" 

app.layout = html.Div([
    navbar.navbar,
    content.content,
    html.P("alemania", id="dummy"),
    html.Div([
        dcc.Dropdown(
                id='select_country',
                options=graficos.getCountries(),
                value = graficos.getCountries()[0],   
                clearable=False,
                
            ),
    ])
        
    
])

"""
@app.callback(
    Output("dropdown-country", "options"),
    Input("dropdown-region", "value"))
def getCountries(region):
    countries=graficos.getCountries()
    print(countries)
    return countries
"""



"""
@app.callback(
    Output('lbl_campaign_name', 'children'),
    Output('lbl_period', "children"),
    Input('dropdown_campaign', 'value'),
    Input('dropdown_period', 'value')
    
)
def update_features_campaign_period(campaign, period):
    print(campaign)
    print(period.upper())
    return campaign , period.upper()


@app.callback(
    Output("graph_histogram", "figure"), 
    Input("mean", "value"), 
    Input("std", "value")
    )
def display_histogram(mean,std):
   data = np.random.normal(mean, std, size=500) # replace with your own data source
   fig = px.histogram(data, range_x=[-10, 10])
   return fig
"""
""" 
@app.callback(
    Output("graph-inner", "figure"), 
    Input("dropdown-country", "value"))

def displayProphet(cols):
    cols = cols
    print("Displaying prophet")
    fig = graficos.prophet()
    return fig
  #por si no da el prophet


def filter_heatmap(cols):

    df = px.data.medals_wide(indexed=True)
    fig = px.imshow(df[cols])
    print("tipo ")
    print(type(fig))
    return fig
"""

@app.callback(
    Output("graph-inner", "figure"), 
    #Input("dropdown-country", "value"))
    Input("dummy", "children"))

def displayProphet(country):
    print(country)
    print("Displaying prophet")
    fig = graficos.prophet(country)
    return fig


@app.callback(
    Output('lblGeneralSummary', 'children'),
    Input("select-country", "value")
)
def selectedCountry(country):
    print(country)
    return "General Summary ("+str(country)+")"


if __name__ == '__main__':
    app.run_server(port= 5050, debug=True)