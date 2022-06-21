import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from app import sidebar, content, navbar
from graficos import  graficos
import plotly.express as px
from app.style import style
import numpy as np



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div( [
    html.Div([navbar.navbar]),
    html.Div([dcc.Graph(id="graph")]),
    html.Div([
         sidebar.sidebar,
         content.content
        ]),
    
    #html.Div([footer.footer]),
    
])

 


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

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))

def displayProphet(cols):
    cols = cols
    print("Displaying prophet")
    fig = graficos.prophet()
    return fig
"""  #por si no da el prophet
def filter_heatmap(cols):

    df = px.data.medals_wide(indexed=True)
    fig = px.imshow(df[cols])
    print("tipo ")
    print(type(fig))
    return fig
"""




if __name__ == '__main__':
    app.run_server(port= 5050, debug=True)