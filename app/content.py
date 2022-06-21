import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.express as px
from app.style import style
from graficos import graficos



content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Card Title 1'], className='card-title',
                                style=style.CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Sample text.'], style=style.CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('Card Title 2', className='card-title', style=style.CARD_TEXT_STYLE),
                        html.P('Sample text.', style=style.CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Card Title 3', className='card-title', style=style.CARD_TEXT_STYLE),
                        html.P('Sample text.', style=style.CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Card Title 4', className='card-title', style=style.CARD_TEXT_STYLE),
                        html.P('Sample text.', style=style.CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=3
    )
])


content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1' ),
            md=6,
        ),
        dbc.Col([
            dcc.Graph(id='graph_histogram'), 
            html.P("Mean:"),
            dcc.Slider(id="mean", min=-3, max=3, value=0,  marks={-3: '-3', 3: '3'}),
            html.P("Standard Deviation:"),
            dcc.Slider(id="std", min=1, max=3, value=1,  marks={1: '1', 3: '3'}),
            
        ],
        md=6,
        ),
        
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_6'), md=6
        )
    ]
)

dropdowns = html.Div([

    dbc.Row([
        dbc.Col(
            html.Div([html.P(html.B("Select a campaign: ")),  dcc.Dropdown(
                ['Agenda comercial de turismo', 'Agendas de Cooperación', 'Capacitaciones y presentaciones de destino', 'FAM - PRESS Trips', 'Feria internacional de Turismo', 'Macrorruedas y Encuentros Comerciales', 'Primera Visita', 'Entrega informacion valor agregado', 'Otras Acciones promocion turismo', 'Preparación y adecuación '],
                'Primera Visita',
                clearable=False,
                id="dropdown_campaign"
            )]),
        ),
        dbc.Col(
            html.Div([html.P(html.B("Select a Period: ")),  dcc.Dropdown(
                ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                'Enero',
                clearable = False ,
                
                id = "dropdown_period"

            )]), 
        ),
        dbc.Col(
            dcc.Dropdown(
                    id="dropdown",
                    options=[
                        {"label": "GOLD", "value": "gold"},
                        {"label": "SILVER", "value": "silver"},
                        {"label": "BRONZE", "value": "bronze"},
                    ],
                    value=['gold', 'silver', 'bronze'],
                    multi = True
                ),
        )
    ]
    )

      
    
] )


content = html.Div(
    [
        
        html.H2('Analytics Dashboard Template', style=style.CONTENT_TEXT),
        html.Hr(),
        dropdowns,
        html.Hr(),
        #content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row
    ],
    style=style.CONTENT_STYLE
)