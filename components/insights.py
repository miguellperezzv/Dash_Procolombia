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
                    className="col-md-4", style={"margin-left": "auto", "margin-right": "auto"},
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
                        style={"margin-left": "auto", "margin-right": "auto"}
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
                        style={"margin-left": "auto", "margin-right": "auto"}
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
        dbc.Col([
            html.H2("Standards"),
            html.Br(),
            html.P("To take into account, a convention is used for the appointment of promotional activities:"),
            html.Br(),
            html.Li("x1: Agenda comercial de turismo."),
            html.Li("x2: Agendas de cooperación / misiones."),
            html.Li("x3: Capacitaciones y presentaciones de destino."),
            html.Li("x4: Entrega información valor agregado."),
            html.Li("x5: Fam - press trips."),
            html.Li("x6: Feria internacional de turismo."),
            html.Li("x7: Macro ruedas y encuentros comerciales."),
            html.Li("x8: Otras acciones promoción turismo."),
            html.Li("x9: Primera visita.")

        ], lg=4, md=12),
        
        dbc.Col([
            html.H2("The Model", style={"text-align": "center"}),
            html.Br(),
            html.P("In order to know the performance of each of the promotional activities, identify at what point in time they have the greatest impact and the long-term prediction of the arrival of tourists to Colombia, two modeling guidelines were designed:"),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                    [
                    dbc.CardImg(src="assets\\prophet.png", top=True, ),
                    dbc.CardBody([
                    html.H4("Time series model (Prophet):"),
                    html.P("A time series model was programmed using the Prophet that allows the user to choose the country and how many periods ahead he wants to see the influence of promotional activities. Initially, 9 models per country are calculated taking into account the lag, where the percentage gap between the model prediction and the observed data is calculated, all this eliminating at least one of the activities of each model, with this exercise it can be said that the Missing value in the prediction comes from missing activity.", className="card-text")
                    ]),
                    ],
                    style={"width": "18rem"},
)
                ]),
                dbc.Col([

                ]),

                dbc.Col([
                    dbc.Card(
                    [
                    dbc.CardImg(src="assets\\xgboost.png", top=True, style={"size": "20rem"}),
                    dbc.CardBody([
                    html.H4("Prediction models (Gradient Boosting and Xgboost):"),
                    html.P("For this model it was necessary to automate the training and the choice of the model in such a way that the user interaction is minimal. Therefore, four types of models with two types of vision were created, that is, four analysis models per axis and four analysis models per country, which were designed as follows: One that trains a gradient-enhancing regressor in search of optimizing the parameters using GridSearchCV and using K-Fold to improve its learning, in addition to searching by period (forward) for the influence of promotional activities on the flow of travelers by hub or city , this will generate as many models as periods forward are taken, so if the user advances five periods, the five models of this class will be obtained. It is important to clarify that the only variables that are carried out are promotional activities.", className="card-text")
                    ]),
                    ],
                    style={"width": "30rem"},
)
                ]),
                dbc.Col([

                ]),

            ])
        ], lg=8, md=12 )


        
    ]),
    html.Hr(),
    dbc.Row([

    ])
],  style = {'margin-left' : "30px"} )