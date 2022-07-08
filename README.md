
# Evaluation of Performance measurement and prediction for tourism strategic activities

Given the pandemic impact over diverse economic sectors, 
it’s a focal point for Procolombia to take a look at their own area, that is, Tourism, which was affected by recent events aforementioned. 

Procolombia as the main tourism, foreign investment and export promotion organism has been taking advantage of the recent economic and stability, by elaborating Campaigns and Strategies aiming to highlight best and proven-effective practices of the past and define future actions of the company.


## Authors
- TEAM 76 (Correlation One - 2022 Cohort )
![Logo](https://i.ibb.co/WPM0v5y/team-76.jpg)

  - [Claudia Agudelo](mailto:cjohana031@outlook.com)
  - [Maher Herrera](mailto:maherstehisy@gmail.com)
  - [Gabriel Celis](mailto:gabocp@yahoo.co)
  - [Johan Sebastián Ayala](mailto:jsaj360@gmail.com)
  - [Javier Rodriguez](mailto:javier.rodriguezb@gmail.com)
  - [Pablo Verbel](mailto:pabloverbel@live.com)
  - [Miguel Pérez](mailto:miguellperezzv@gmail.com)


## Run Locally

#### Before deploy the application you have to set the respective joblibs inside folder. See this tree

```
.
└── Dash_Procolombia/
    ├── assets
    ├── components
    ├── data/
    │   └──final.csv
    ├── logica
    ├── modelos/
    │   ├── alianzapacifico_retrazos_0.joblib
    │   ├── ... .joblib
    │   └── ... .joblib
    ├── modelos_pais_destacado/
    │   ├── chile_retrazos_0.joblib
    │   ├── ... .joblib
    │   └── ... .joblib
    ├── app.py
    └── requirements.txt
```
Now clone the project!

```bash
  git clone https://github.com/miguellperezzv/Dash_Procolombia.git
```
You have to create a virtual enviroment (pip or conda, we sugest you conda!)

```bash
    conda create -n entornoDash python=3.8 anaconda
    conda activate entornoDash
```
```bash
    python3 -m venv /path/
    cd path\to\venv\Scripts\activate.bat
```

Go to the project directory

```bash
  cd Dash_Procolombia
```

Install dependencies

```bash
  pip install requirements.txt
```

Start the server

```bash
  python app.py
```


## Demo

![Alt Text](https://media.giphy.com/media/etWq74S1OZXKlfnnPU/giphy.gif)
![ALt Text](https://media.giphy.com/media/HNuzSBXk5HdPSKTsaJ/giphy.gif)


## Environment Variables

No needed environment variables in this project, but you have to load the joblibs, for the correct deployment of the application




## Accessing to the web application

Access to the [web application](http://team76ds4a.gq:9000/)


    
![Logo](https://i.ibb.co/WPM0v5y/team-76.jpg)

