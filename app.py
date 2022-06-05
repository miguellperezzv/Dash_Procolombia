import dash
from dash import dcc
from dash import html
#import dash_core_components as dcc
#import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    html.H1(children = "Hello Dash world",
        style = {
            'textAlign' : "center",
            'color' : "#456FBV"
        }
    ),
    html.Div(children = "Dash !!!!!!!!!!!- product!",
        style = {
            'textAlign' : "center",
            'color' : "#456FBV"
        }
    
    ),

    dcc.Graph(
        id = "Simple Graph",
        figure = {
            'data' : [
                {'x' : [5,6,7], 'y': [12,15,18], 'type' : 'bar', 'name': 'First Chart'},
                {'x' : [5,6,7], 'y': [2,12,10], 'type' : 'bar', 'name': 'First Chart'}
            ],
            'layout': {
                'title' : "Simple Bar Chart"
            }
        }
        
    )
])



if __name__ == '__main__':
    app.run_server(port= 5050, debug=True)