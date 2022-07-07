import dash_bootstrap_components as dbc
from dash import html

content = html.Div([

    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg( 
                        src="assets\\team_76.JPG",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("TEAM 76", className="card-title"),
                            html.P(
                                "This project was made by Team 76  "
                                "below as a natural lead-in to additional "
                                "content. This content is a bit longer.",
                                className="card-text",
                            ),
                            html.Small(
                                
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px"},
)
        ]),



    dbc.Col([
            dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg( 
                        src="assets\\C1.webp",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Correlation One", className="card-title"),
                            html.P(
                                "During the development of the Data Science course - Correlation One (Cohort 6 - 2022).",
                                className="card-text",
                            ),
                            html.Small(
                                
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px"},
)
        ]),
    

    dbc.Col([
            dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg( 
                        src="assets\\procolombia.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Procolombia", className="card-title"),
                            html.P(
                                "The objective of this project is to apply the knowledge learned in the course, developing a methodology to identify and predict the impact that each of its promotional activities in different countries have on the arrival of tourists to Colombia",
                                className="card-text",
                            ),
                            html.Small(
                                
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px"},
)
        ])
    
    ]),
    html.Hr(),
    dbc.Row([
        html.P("This application has 3 sections:"),
        html.Li("Load: Here you must attach the necessary files for loading, exploration, cleaning, identification of correlations and training of the model, this must be provided by ProColombia. It should be considered to keep updated the databases referring to control variables such as currency information, IPC, fairs and carnivals."),
        html.Li("Visualization: Here you can see the information according to the region and the country that is selected, graphs with the numbers of tourists predicted in different periods. Also, the impact of carrying out the campaigns in the country can be observed."),
        html.Li("Featured countries: Relevant countries for Procolombia")
    ]),
    html.Hr(),
    dbc.Row([
        html.P("To take into account, a convention is used for the appointment of promotional activities:"),
        html.Br(),
        html.Li("x1: Agenda comercial de turismo"),
        html.Br(),
        html.Li("x2: Agendas de cooperación / misiones"),
        html.Br(),
        html.Li("x3: Capacitaciones y presentaciones de destino"),
        html.Br(),
        html.Li("x4: Entrega información valor agregado"),
        html.Br(),
        html.Li("x5: Fam - press trips"),
        html.Br(),
        html.Li("x6: Feria internacional de turismo"),
        html.Br(),
        html.Li("x7: Macro ruedas y encuentros comerciales"),
        html.Br(),
        html.Li("x8: Otras acciones promoción turismo"),
        html.Br(),
        html.Li("x9: Primera visita")
        
    ])
],  style = {'margin-left' : "30px"} )