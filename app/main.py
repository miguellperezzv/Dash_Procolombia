import dash 
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    html.H1("Hello Dash world"),
    html.Div("Dash !!!!!!!!!!!- product!"),

    dcc.Graph(
        id = "Simple Graph",
        figure = {
            'data' : [
                {'x' : [5,6,7], 'y': [12,15,18], 'type' : 'bar', 'name': 'First Chart'}
            ],
            'layout': {
                'title' : "SImple Bar Chart"
            }
        }
        
    )
])



if __name__ == '__main__':
    app.run_server(port= 5050)