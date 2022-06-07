import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.express as px
from app.style import style



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
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
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


content = html.Div(
    [
        html.H2('Analytics Dashboard Template', style=style.TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row
    ],
    style=style.CONTENT_STYLE
)