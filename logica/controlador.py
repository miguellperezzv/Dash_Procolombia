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
import joblib
import os
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import xgboost as xgb

from sklearn.metrics import mean_squared_error #MSE
from sklearn.metrics import mean_absolute_error #MAE


#campañas=pd.read_csv('D:\Descargas\\campañas.csv') 
campañas=pd.read_csv('data\\campañas.csv', sep = '|') 
vuelos=pd.read_csv('data\\vuelos.csv', sep = '|') 
#vuelos=pd.read_csv('D:\Descargas\\vuelos.csv') 
oficinas = pd.read_csv('data\\oficinas_comerciales.csv')



countries = vuelos['pais_ori'].unique()
finalCSV = pd.read_csv('data\\final.csv', sep = "|")
df = pd.read_csv('data\\final.csv', sep = "|")



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


def rezagos(final,hub,rezagos):
    if rezagos==0:
        verificacion=final[final['hub']==hub]
        verificacion['pais']=verificacion['pais'].astype('category')
        verificacion['pais']=verificacion['pais'].cat.codes
        #verificacion.set_index('llave',inplace = True)
    else:
        datos=final[final['hub']==hub]
        datos['pais']=datos['pais'].astype('category')
        datos['pais']=datos['pais'].cat.codes
        datos.set_index('llave',inplace = True)
        d=pd.DataFrame([])
        for f in list(datos['pais'].unique()):
            c=datos[datos['pais']==f]
            c=c[['pais','x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9']]
            c=c.shift(periods=rezagos)
            d=pd.concat([d,c])
        d = d.dropna(how='all')
        d=d.reset_index()
        datos=datos.drop(['x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9'], axis=1)
        datos=datos.reset_index()
        verificacion=pd.merge(datos,d, on= ['llave','pais'],how='inner')
        #verificacion.set_index('llave',inplace = True)
        
        
    return verificacion

def tabla_influencia_variable(hub, rez):

    ### leer los joblib del gradient
    directorio = 'modelos/'
    contenido = os.listdir(directorio)
    contador=0
    name=hub+'_retrazos_'
    name1=hub+'_retrazos_total'
    gradients=[]
    xgboost=[]
    for a,fichero in enumerate(contenido):
        if os.path.isfile(os.path.join(directorio, fichero)) and fichero.startswith(name):
            modelo_hub=os.path.join(directorio, fichero)
            if fichero.startswith(name1):
                modelo_hub=os.path.join(directorio, fichero)
                gradient_total=joblib.load(modelo_hub)
            else:
                globals()[f"gradient{contador}"] =joblib.load(modelo_hub)
                gradients.append(globals()[f"gradient{contador}"])
            contador=contador+1
    ### leer los joblib del xgboost    
    rename=hub+'_xbost_retrazos_'
    rename1=hub+'_xbost_retrazos_total'
    contador=0
    ##xgboost
    for a,fichero in enumerate(contenido):
        if os.path.isfile(os.path.join(directorio, fichero)) and fichero.startswith(rename):
            modelo_hub=os.path.join(directorio, fichero)
            if fichero.startswith(rename1):
                modelo_hub=os.path.join(directorio, fichero)
                xgboost_total=joblib.load(modelo_hub)
            else:
                globals()[f"xgboost{contador}"] =joblib.load(modelo_hub)
                xgboost.append(globals()[f"xgboost{contador}"])
            contador=contador+1


    ### mejor modelo de rezagos
    resultados=pd.DataFrame()
    lista=[]
    numero=[]
    modeling=[]
    reales=['pais', 'cantidad_ciudades','educacion','eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo','transito', 'vacaciones', 
            'x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9', 'trm','estaciones','ipc','carnavales','holiday']
    for a,c in enumerate(gradients):
        verificacion=rezagos(finalCSV,hub,a)
        X_train, X_test, y_train, y_test = train_test_split(verificacion[reales],verificacion[['pasajeros']], test_size=0.2, random_state=100, shuffle=True)
        predicciones = c.predict(X = X_test)
        rmse = mean_squared_error(
                y_true  = y_test,
                y_pred  = predicciones,
                squared = False
            )
        lista.append(rmse)
        numero.append(a)
        modeling.append('gradients')
    for a,c in enumerate(xgboost):
        verificacion=rezagos(finalCSV,hub,a)
        X_train, X_test, y_train, y_test = train_test_split(verificacion[reales],verificacion[['pasajeros']], test_size=0.2, random_state=100, shuffle=True)
        predicciones = c.predict(X = X_test)
        rmse = mean_squared_error(
                y_true  = y_test,
                y_pred  = predicciones,
                squared = False
            )
        lista.append(rmse)
        numero.append(a)
        modeling.append('xgboost')
    resultados['metrica']=lista
    resultados['numero']=numero
    resultados['modelo']=modeling
    resultados=resultados.sort_values(by='metrica').reset_index(drop=True)
    resultados=resultados.head(1)
    resultados

    if resultados['modelo'][0]=='gradients':
        modelo=joblib.load('modelos/'+hub+'_retrazos_'+str(resultados['numero'][0])+'.joblib')
    else:
        modelo=joblib.load('modelos/'+hub+'_xbost_retrazos_'+str(resultados['numero'][0])+'.joblib')
    importancias=list(modelo.feature_importances_)

    a=['pais','cantidad_ciudades','educacion',
       'eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo',
       'transito', 'vacaciones', 
       'agenda_comercial_de_turismo', 'agendas_de_cooperacion/_misiones',
       'capacitaciones_y_presentaciones_de_destino',
       'entrega_informacion_valor_agregado', 'fam_-_press_trips',
       'feria_internacional_de_turismo',
       'macrorruedas_y_encuentros_comerciales',
       'otras_acciones_promocion_turismo', 'primera_visita', 'trm','estaciones','ipc','carnavales','holiday']

    table=pd.DataFrame(a, columns = ['variables'])
    table['importancias']=importancias
    table = table.sort_values('importancias',ascending=False).reset_index(drop=True)
    #table



def getCountries():
    return finalCSV["pais"].unique()

def getCountriesByRegion(region):
    return finalCSV[finalCSV["hub"] == region]["pais"].unique()
    

def getRegions():
    return finalCSV["hub"].unique()

def getActividades():

    return finalCSV[""]