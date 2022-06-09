import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.express as px
from app.style import style




'''
controls = dbc.FormGroup(
    [
        html.P('Dropdown', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            }, {
                'label': 'Value Two',
                'value': 'value2'
            },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1'],  # default value
            multi=True
        ),
        html.Br(),
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='range_slider',
            min=0,
            max=20,
            step=0.5,
            value=[5, 15]
        ),
        html.P('Check Box', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        html.Br(),
        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value='value1',
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)
'''

table = [
    html.Thead(html.Tr([html.Th("Country"), html.Th("Visitors")]))
]

row1 = html.Tr([html.Td("Brasil"), html.Td("30")])
row2 = html.Tr([html.Td("Canada"), html.Td("25")])
row3 = html.Tr([html.Td("Mexico"), html.Td("20")])


table_body = [html.Tbody([row1, row2, row3])]

table_top_countries = dbc.Table(table + table_body, bordered=True)

summary = dbc.FormGroup(
    [
        
         html.P(html.B('Top Countries'), style={
            'text-align': 'center', 
            'color': '#FFFFFF',
        }),
    
    
    dbc.Card(
        [
            table_top_countries
        ]
    ),

    html.Hr(),
    html.P(html.B('Predictions / Behavior'), style={
            'textAlign': 'center',
            'color': '#FFFFFF',
        }),
    html.Div(
        [
            html.H6("Visitors per Month"),
            html.H6("4444", style={ 'textAlign': 'center'}),
            html.P('Country Behavior', style={ 'textAlign': 'center'}),
            html.Div([
                dcc.Dropdown(
                id='dropdown_country',
                options=[{
                    'label': 'Brasil',
                    'value': 'Brasil'
                }, {
                    'label': 'Argentina',
                    'value': 'Argentina'
                },{
                    'label': 'Mexico',
                    'value': 'Mexico'
                }
                ],
                value=['Brasil'],  # default value
                multi=False,
                
            ),
            ],
            style = {'margin-left' : '10px','margin-right' : '10px',}
            ),
            
            html.H3('+ 80 visitors ', style={ 'textAlign': 'center'}),
        ],
        style={'background-color' :style.PROCOLOMBIA_COLORS["clearer_red"], 'textAlign' : 'center' }
    )

    ]
    

)


sidebar = html.Div(
    [
        html.H2('Campaign Name', style=style.SIDEBAR_TEXT),
        html.Hr(),
        summary, 
        #controls
    ],
    style=style.SIDEBAR_STYLE,
)