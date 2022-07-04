from os import lseek
import pandas as pd
#import seaborn as sns
#simport matplotlib.pyplot as plt
import statsmodels.api as sm ### Sarimax
import numpy as np
import statsmodels.formula.api as smf
import prophet as prp
from dash import Dash, dcc, html, Input, Output, callback
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objects as go
import plotly.express as px


#campañas=pd.read_csv('D:\Descargas\\campañas.csv') 
campañas=pd.read_csv('data\\campañas.csv', sep = '|') 
vuelos=pd.read_csv('data\\vuelos.csv', sep = '|') 
#vuelos=pd.read_csv('D:\Descargas\\vuelos.csv') 
oficinas = pd.read_csv('data\\oficinas_comerciales.csv')



countries = vuelos['pais_ori'].unique()
finalCSV = pd.read_csv('data\\final.csv', sep = "|")
df = pd.read_csv('data\\final.csv', sep = "|")

"""
def prophet(country):
    
    a=vuelos.groupby(['llave','pais_ori']).sum().reset_index()
    a=a[['llave','pais_ori','pasajeros']]
    m1 = prp.Prophet()
    #country = country
    b=a[a['pais_ori']=='mexico']

    c=b[['llave','pasajeros']]
    c.columns = ['ds', 'y']
    c['ds']= pd.to_datetime(c['ds'])

    variable=campañas[['llave','pais_empresa','servicio']].groupby(['llave','pais_empresa','servicio']).size().reset_index()
    variable.columns=['llave', 'pais_empresa', 'servicio', 'total']

    prueba=variable[(variable['pais_empresa']=='mexico')]
    pais=prueba.pivot(index='llave', columns='servicio', values='total').reset_index().fillna(0)
    pais.columns=['ds','x1','x2','x3','x4','x5','x6','x7','x8']
    pais['ds']= pd.to_datetime(pais['ds'])

    a=vuelos.groupby(['llave','pais_ori']).sum().reset_index()
    a=a[['llave','pais_ori','pasajeros']]

    ejercicio=pd.merge(c, pais, on='ds',how='left').fillna(0)

    m1.add_regressor('x1')
    m1.add_regressor('x2')
    m1.add_regressor('x3')
    m1.add_regressor('x4')
    m1.add_regressor('x5')
    m1.add_regressor('x6')
    m1.add_regressor('x7')
    m1.fit(ejercicio)

    future = m1.make_future_dataframe(periods=365)
    future['x1']=ejercicio['x1']
    future['x2']=ejercicio['x2']
    future['x3']=ejercicio['x3']
    future['x4']=ejercicio['x4']
    future['x5']=ejercicio['x5']
    future['x6']=ejercicio['x6']
    future['x7']=ejercicio['x7']
    future=future.fillna(0)

    forecast = m1.predict(future)
    #forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    #fig1 = m1.plot(forecast)
    
    figFinal = plot_plotly(m1, forecast)
    print("Prophet for country: "+country)
    return figFinal

"""

def display_map_single_country(start_date,end_date, hub): 
    f_start_date = start_date.date()
    start_date = pd.to_datetime(f_start_date)
    f_end_date = end_date.date()
    end_date = pd.to_datetime(f_end_date)
    
    df["llave"] = pd.to_datetime(df["llave"], format="%Y-%m")
    dff= df[(df['llave'] >= start_date) & (df['llave'] <= end_date)]
    
    #Should create a new column to map called "codigo_pais"
    espana_key=df.iloc[2670]['pais']
    country_codes={'alemania': 'DEU', 'antigua_y_barbuda': 'ATG', 'argentina': 'ARG','aruba': 'ABW', 'australia': 'AUS', 'austria': 'AUT', 'azerbaiyan': 'AZE', 'bahrein': 'BHR', 'barbados': 'BRB', 'belgica': 'BEL', 'bolivia': 'BOL', 'brasil': 'BRA', 'bulgaria': 'BGR', 'canada': 'CAN', 'chile': 'CHL', 'china': 'CHN', 'chipre': 'CYP', 'costa_rica': 'CRI', 'croacia': 'HRV', 'cuba': 'CUB', 'dinamarca': 'DNK', 'ecuador': 'ECU', 'egipto': 'EGY', 'el_salvador':'SLV', espana_key: 'ESP', 'estados_unidos': 'USA', 'estonia': 'EST', 'filipinas': 'PHL', 'finlandia': 'FIN', 'francia': 'FRA', 'granada': 'GRD', 'grecia': 'GRC', 'guatemala': 'GTM', 'guyana': 'GUY', 'hungria': 'HUN', 'india': 'IND', 'indonesia': 'IDN', 'islas_caiman': 'CYM', 'israel': 'ISR', 'italia': 'ITA', 'jamaica': 'JAM', 'japon': 'JPN', 'kuwait': 'KWT','letonia': 'LVA','lituania': 'LTU', 'luxemburgo': 'LUX', 'malasia': 'MYS', 'malta': 'MLT', 'mexico': 'MEX', 'monaco': 'MCO', 'nicaragua': 'NIC', 'noruega': 'NOR', 'nueva_zelanda': 'NZL','paises_bajos': 'NLD', 'panama': 'PAN', 'paraguay': 'PRY', 'peru': 'PER', 'polonia': 'POL', 'portugal': 'PRT', 'puerto_rico': 'PRI', 'reino_unido': 'GBR','republica_dominicana': 'DOM', 'rumania': 'ROU', 'rusia': 'RUS', 'santa_lucia': 'LCA','singapur': 'SGP','sri_lanka': 'LKA', 'suecia': 'SWE', 'suiza': 'CHE', 'surinam': 'SUR', 'tailandia': 'THA', 'taiwan': 'TWN', 'turquia': 'TUR', 'ucrania': 'UKR', 'venezuela': 'VEN', 'albania': 'ALB', 'qatar': 'QAT', 'republica_checa': 'CZE'}
    dff = dff.copy()
    dff['codigo_pais'] = dff['pais'].map(country_codes)
    
    
    dff = dff.groupby(["pais", "codigo_pais", "hub"]).sum().reset_index()

    fig = go.Figure(data=go.Choropleth(
        #locations = dff['codigo_pais'],
        #locations = dff[dff['hub'] == hub]['codigo_pais'],
        locations=dff[dff['hub'] == hub]['codigo_pais'],
        #zoom=("united states of america", "canada", "mexico"),
        
        z = dff[dff['hub'] == hub]['pasajeros'],
        text = dff[dff['hub'] == hub]['codigo_pais'],
        colorscale = 'Viridis',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Pasajeros',
    ))

    fig.update_layout(
        title_text='Pasajeros por país de la región en el rango de fechas seleccionado',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            landcolor = 'lightgray',
            showland = False,
            showcountries = True,
            countrycolor = 'gray',
            countrywidth = 0.5,
    ))
    return fig

def display_time_series(hub,selected_countries):
    dff=df[df['pais'].isin(selected_countries)]
    dff=dff.groupby(['pais','llave']).sum().reset_index()
    fig=px.line(dff,x="llave",
                y="pasajeros", 
                color="pais", 
                title='Pasajeros por mes en el país',
                labels={"llave":"fecha"})
    fig.update_xaxes(
        dtick="M6",
        tickformat="%b\n%Y")
    return fig


def display_barplot(selected_countries,selected_activities):
    dff=df[df['pais'].isin(selected_countries)]
    dff=dff.groupby(['pais']).sum().reset_index()

    fig = px.bar(dff, x="pais",
                 y=selected_activities,
                 text_auto=True,
                 title="Total actividades de promoción por en el país",
                 labels={"variable":"actividad","value":"cantidad"})
    return fig


def rezagos_pais(final,pais,rezagos):
    if rezagos==0:
        verificacion=final[final['pais']==pais]
    else:
        datos=final[final['pais']==pais]
        datos.set_index('llave',inplace = True)
        d=pd.DataFrame([])
        c=datos[['x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9', 'trm', 'estaciones', 'ipc', 'carnavales', 'holiday']]
        c=c.shift(periods=rezagos)
        d=pd.concat([d,c])
        d = d.dropna(how='all')
        d=d.reset_index()
        datos=datos.drop(['pais','x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9', 'trm', 'estaciones', 'ipc', 'carnavales', 'holiday'], axis=1)
        datos=datos.reset_index()
        verificacion=pd.merge(datos,d, on= ['llave'],how='inner')        
        verificacion=verificacion[['llave','x1','x2','x3','x4','x5','x6','x7','x8','x9', 'trm', 'estaciones', 'ipc', 'carnavales', 'holiday']]
        verificacion.columns=['ds','x1','x2','x3','x4','x5','x6','x7','x8','x9', 'trm', 'estaciones', 'ipc', 'carnavales', 'holiday']
        verificacion['ds']= pd.to_datetime(verificacion['ds'])
        
        
        "poner las extras a la serie"
        c=final[final['pais']==pais][['llave','pasajeros']]
        c.columns = ['ds', 'y']
        c['ds']= pd.to_datetime(c['ds'])
        ejercicio=pd.merge(c, verificacion, on='ds',how='left').fillna(0)
    return ejercicio


def prophet(pais, numRezagos):
    b=rezagos_pais(finalCSV,pais,numRezagos)
    dif = pd.DataFrame()
    dif['llave'] = b['ds']
    var = ['x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9']
    for v in var:
        m1 = prp.Prophet()
        for k in var:
            if(v != k):
                m1.add_regressor(k)
        m1.add_regressor('trm')
        m1.add_regressor('estaciones')
        m1.add_regressor('ipc')
        m1.add_regressor('carnavales')
        m1.add_regressor('holiday')
        m1.fit(b)
        future = m1.make_future_dataframe(periods=365)
        for l in var:
            if(v != l):
                future[l]=b[l]
        future['trm']=b['trm']
        future['estaciones']=b['estaciones']
        future['ipc']=b['ipc']
        future['carnavales']=b['carnavales']
        future['holiday']=b['holiday']
        future=future.fillna(0)
        dif[v] = round(((b['y']*100)/(m1.predict(future).iloc[: , -1]))-100,2)
        del m1  
#Eliminar las filas de rezagos a no tener en cuenta 
    dif.drop(dif.head(2).index , inplace=True)
    #dif
    
    varT = ['x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9','trm','estaciones','ipc','carnavales','holiday']
    mF = prp.Prophet()
    for x in var:
        mF.add_regressor(x)       
    mF.fit(b)
    futureF = mF.make_future_dataframe(periods=365)
    for y in var:
        futureF[y]=b[y]
    futureF=futureF.fillna(0)

    forecast = mF.predict(futureF)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail() 

    figFinal = plot_plotly(mF, forecast)
    print("Prophet for country: "+pais)
    return figFinal

def getCountries():
    return finalCSV["pais"].unique()

def getCountriesByRegion(region):
    return finalCSV[finalCSV["hub"] == region]["pais"].unique()
    

def getRegions():
    return finalCSV["hub"].unique()

def getActividades():

    return finalCSV[""]