import dash
import os
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from components import content, destacados, region, navbar, insights
import dash_uploader as du

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([

    navbar.navbar,
    html.Br(),
    dbc.Col([
        dcc.Tabs(id="tabs", value='tab_load', children=[
           

        dcc.Tab(label='Visualización por Hubs', value='tab_hubs'),
        dcc.Tab(label='Visualización por países', value='tab_paises'),
        dcc.Tab(label='Países destacados', value='tab_destacados'),
        dcc.Tab(label='Dataset', value='tab_load'),
        dcc.Tab(label='Entrenamiento', value=''),     
        dcc.Tab(label="About", value = 'tab_insights')

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
    elif tab == "tab_insights":
        return insights.content
    else:
        return layout
        
UPLOAD_FOLDER_ROOT = os.path.dirname(__file__)+r"/modelos"

du.configure_upload(app, UPLOAD_FOLDER_ROOT,use_upload_id=False)

def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        max_files=100
    )

layout = html.Div(
        [
            html.H1('Joblibs'),
            
            html.Div(
                [
                    html.H4('Decargar el archivo para generar los joblist'),
                    dcc.Link('Descarga', href='assets/entrenar.py', target='_blank'),
                    get_upload_component(id='dash-uploader'),
                    html.Div(id='callback-output'),
                ],
                style={  # wrapper div style
                    'textAlign': 'center',
                    'width': '600px',
                    'padding': '10px',
                    'display': 'inline-block'
                }),
        ],
        style={
            'textAlign': 'center',
        },
    )

@du.callback(
    output=Output("callback-output", "children"),
    id="dash-uploader",
)
def callback_on_completion(status: du.UploadStatus):
    return html.Ul([html.Li(str(x)) for x in status.uploaded_files])            


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port= 7000, debug=True)