import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import os 
import plotly.express as px
from assets import style




"""
navbar = dbc.Navbar([
    dbc.Row([
        dbc.Col(['Column 1']),
        dbc.Col(['Column 2']),
        dbc.Col(['Column 3']),
    ])
]),
"""    

navbar= dbc.Navbar(
    [

        dbc.Col(
            [
                html.A(
                html.Img(src=style.DS4A, height="50px"),
                href="https://www.correlation-one.com/data-science-for-all-empowerment",
                style={'textAlign': 'center', 'margin-right': '5%', "margin-bottom":"10px"}
                ),
            ],
            width=0.5,
        ),
        dbc.Col(
            [
            html.A(
            html.Img(src=style.PROCOLOMBIA_LOGO, height="50px"),
            href="https://procolombia.co/",
            style={'textAlign': 'center','margin-left': '5%',}
                ),
            ],
            width=0.5,
        ),
        dbc.Col(
            [
            dbc.Col( html.H3("TEAM 76", className="titulo"))
            ],
            width=4,
        ),

        dbc.Col(
            [dbc.NavbarBrand("Dashboard de actividades de Promoción turística", className="ms-2")],
            width=4,
        ),
        
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
               # search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
    
    ],
    #brand="DS4A Project - Team  76",
    color=style.PROCOLOMBIA_COLORS["clear_blue"],
    dark=True,
    #className="mb-2",
) 
    

    







