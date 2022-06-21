import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import os 
import plotly.express as px
from assets import style





navbar = dbc.Navbar([

        dbc.Col(
            [
                html.A(
                html.Img(src=style.DS4A, height="50px"),
                href="https://www.correlation-one.com/data-science-for-all-empowerment",
                style={'textAlign': 'center', 'margin-right': '5%',}
                ),
                
                html.A(
                html.Img(src=style.PROCOLOMBIA_LOGO, height="50px"),
                href="https://procolombia.co/",
                style={'textAlign': 'center','margin-left': '5%',}
                ),
               
            ]
            
        ),
        dbc.Col(
            [
             html.H3("Team 76"),
             dbc.Col(dbc.NavbarBrand("Touristic campaigns management", className="ms-2",style=style.NAVBAR_TEXT)),
            ]
            
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
    className="mb-2",
)



"""
navbar = html.Div([
    
    dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PROCOLOMBIA_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("Touristic campaigns management", className="ms-2",style=style.NAVBAR_TEXT)),
                    ],
                    align="center",
                    className="g-0",
                    style = style.NAVBAR_STYLE,

                ),
                href="https://procolombia.co/",
                style=style.NAVBAR_STYLE,
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
               # search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        style = style.NAVBAR_STYLE,

    ),
    
    style = style.NAVBAR_STYLE,

)

    

],
style = style.NAVBAR_STYLE,

)
"""



