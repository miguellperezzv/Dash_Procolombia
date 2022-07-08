import base64
import os
#from urllib.parse import quote as urlquote
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import subprocess




UPLOAD_DIRECTORY = os.path.dirname(os.path.dirname(__file__))+"/data"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


layout = html.Div(
    [
        html.H2("Construccion Archivo FINAL.CSV", style={"text-align":"center"}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Card([

        html.Div(
        children=[
        html.H2("Viajeros.xlsb"),
        dcc.Upload(
            id="viajeros",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-viajeros",
            type="default",
            children=[]
        )
        ]),
        html.Div(
        children=[
        html.H2("frecuencias.csv"),
        dcc.Upload(
            id="frecuencias",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-frecuencias",
            type="default",
            children=[]
        )
        ]),
        html.Div(
        children=[
        html.H2("carnavales.xlsx"),
        dcc.Upload(
            id="carnavales",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-carnavales",
            type="default",
            children=[]
        )
        ]),
        
        html.Div(
        children=[
        html.H2("TRM.xlsx"),
        dcc.Upload(
            id="TRM",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-TRM",
            type="default",
            children=[]
        )
        ]),
        
        html.Div(
        children=[
        html.H2("IPC.csv"),
        dcc.Upload(
            id="IPC",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-IPC",
            type="default",
            children=[]
        )
        ]),
        
        html.Div(
        children=[
        html.H2("clima.xlsx"),
        dcc.Upload(
            id="clima",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-clima",
            type="default",
            children=[]
        )
        ]),
        
        html.Div(
        children=[
        html.H2("campanas.xlsx"),
        dcc.Upload(
            id="campanas",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-campanas",
            type="default",
            children=[]
        )
        ]),
        
        html.Div(
        children=[
        html.H2("hubs.csv"),
        dcc.Upload(
            id="hubs",
            children=html.Button('Upload File'),
            ),
        dcc.Loading(
            id="loading-hubs",
            type="default",
            children=[]
        )
        ]),
        ], className="six columns")
            ])]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
        html.H2("File List"),
        html.Ul(id="file-list"), 
        html.Div(children=[
                       html.Div([            
                       html.Button('Generate Final.csv', id='apply-button', n_clicks=0),
                       dcc.Loading(
                            id="output-container-button",
                            type="default",
                            children='Hit the button to generate.'
                        ),
                      ])
                ]),
        ], className="six columns")])]),
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ) 
          
           
    ],
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    #location = UPLOAD_DIRECTORY+"/download/{}".format(urlquote(filename))
    location = UPLOAD_DIRECTORY+"/"+filename

    return html.A(filename, href=location)


@callback(
    Output("loading-viajeros", "children"),
    [Input("viajeros", "id"),Input("viajeros", "filename"), Input("viajeros", "contents")],
)

@callback(
    Output("loading-frecuencias", "children"),
    [Input("frecuencias", "id"),Input("frecuencias", "filename"), Input("frecuencias", "contents")],
)
@callback(
    Output("loading-carnavales", "children"),
    [Input("carnavales", "id"),Input("carnavales", "filename"), Input("carnavales", "contents")],
)
@callback(
    Output("loading-TRM", "children"),
    [Input("TRM", "id"),Input("TRM", "filename"), Input("TRM", "contents")],
)
@callback(
    Output("loading-IPC", "children"),
    [Input("IPC", "id"),Input("IPC", "filename"), Input("IPC", "contents")],
)
@callback(
    Output("loading-clima", "children"),
    [Input("clima", "id"),Input("clima", "filename"), Input("clima", "contents")],
)

@callback(
    Output("loading-campanas", "children"),
    [Input("campanas", "id"),Input("campanas", "filename"), Input("campanas", "contents")],
)
@callback(
    Output("loading-hubs", "children"),
    [Input("hubs", "id"),Input("hubs", "filename"), Input("hubs", "contents")],
)

def update_output(id, filename, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""
    #good = dbc.Alert(f"{filename} Saved as {name}", color="success"),
    fail = dbc.Alert("There was an error processing this file.", color="danger"),
    
    
    if filename is not None and uploaded_file_contents is not None:
        try:
                if id == 'viajeros':
                    name= 'viajeros.xlsb'
                    save_file(name, uploaded_file_contents)
                elif id == 'frecuencias':
                    name= 'frecuencias.csv'                    
                    save_file(name, uploaded_file_contents)
                elif id == 'carnavales':
                    name= 'carnavales.xlsx'                    
                    save_file(name, uploaded_file_contents)
                elif id == 'TRM':
                    name= 'TRM.xlsx'                    
                    save_file(name, uploaded_file_contents)
                elif id == 'IPC':
                    name= 'IPC.csv'                    
                    save_file(name, uploaded_file_contents)
                elif id == 'clima':
                    name= 'clima.xlsx'                    
                    save_file(name, uploaded_file_contents)
                elif id == 'campanas':
                    name= 'campanas.xlsx'                    
                    save_file(name, uploaded_file_contents)
                elif id == 'hubs':
                    name= 'hubs.csv'                    
                    save_file(name, uploaded_file_contents)
                else:
                    return Exception
                
                return dbc.Alert(f"{filename} Saved as {name}", color="success")
        except Exception as e:
            print(e)
            return fail
        
        
        
@callback(
    Output('output-container-button', 'children'),
    [Input('apply-button', 'n_clicks')])

def run_script_onClick(n_clicks):
    #print('[DEBUG] n_clicks:', n_clicks)
    
    if not n_clicks:
        #raise dash.exceptions.PreventUpdate
        raise PreventUpdate

    # without `shell` it needs list ['/full/path/python', 'script.py']           
    #result = subprocess.check_output( ['/usr/bin/python', 'script.py'] )  

    # with `shell` it needs string 'python script.py'
    result = subprocess.check_output('python '+os.path.dirname(os.path.dirname(__file__))+'/assets/datasetclean.py', shell=True)  

    # convert bytes to string
    result = result.decode(encoding='cp1252')   
    
    return result


@callback(Output('file-list', 'children'),
    Input('interval-component', 'n_intervals'))
def uploaded_files(n):
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
            
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]