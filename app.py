import dash
from dash import dcc
from dash import html
import numpy as np
import plotly.grapgh.objs as go
#import dash_core_components as dcc
#import dash_html_components as html

app = dash.Dash()

np.random.seed(50)
x_rand = np.random.randint(1,61,60)
y_rand = np.random.randint(1,61,60)

colors = {
    'text' : "#ff0000",
    'plot_color' : "#D3D3D3",
    'papel_color' : "#D3D3D3",
}

app.layout = html.Div([
    html.H1(children = "Hello Dash world",
        style = {
            'textAlign' : "center",
            'color' : colors["text"]
        }
    ),
    html.Div(children = "Dash !!!!!!!!!!!- product!",
        style = {
            'textAlign' : "center",
            'color' : colors["plot_color"]
        }
    
    ),

    #BAR CHART 
    dcc.Graph(
        id = "Simple Graph",
        figure = {
            'data' : [
                {'x' : [5,6,7], 'y': [12,15,18], 'type' : 'bar', 'name': 'First Chart'},
                {'x' : [5,6,7], 'y': [2,12,10], 'type' : 'bar', 'name': 'First Chart'}
            ],
            'layout': {
                'plot_bgcolor' : colors["plot_color"],
                'paper_bgcolor': "#D3D3D3",
                'font' : {
                    'color' : "ff0000",
                },
                'title' : "Simple Bar Chart"
            }
        }
        
    ),

    #scatter 
    dcc.Graph(
        id = 'scatter_chart',
        figure={
            'data' : 
            [
                go.Scatter(
                    x = x_rand,
                    y = y_rand,
                    mode = "marker"
                )
            ],
            'layout' : go.Layout(
                title = "Scatterplot random",
                xasis = {'title': 'Random x'},
                yasis = {'title': 'Random y'}
            )
        }
        
    )


])



if __name__ == '__main__':
    app.run_server(port= 5050, debug=True)