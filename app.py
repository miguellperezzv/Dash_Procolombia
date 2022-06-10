import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from app import sidebar, content, navbar

import plotly.express as px
from app.style import style
import numpy as np


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div( [
    html.Div([navbar.navbar]),
    html.Div([
         sidebar.sidebar,
         content.content
        ]),
    #html.Div([footer.footer]),
    
])


  

@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    return 'Card Tile 1 change by call back'


@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    return 'Card text change by call back'

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

if __name__ == '__main__':
    app.run_server(port= 5050, debug=True)