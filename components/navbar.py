import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import os 
import plotly.express as px
from assets import style



PROCOLOMBIA_LOGO = "https://procolombia.co/sites/all/themes/proexport/reskin/images/logo_proco_res.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    style = style.NAVBAR_STYLE,

    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


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




