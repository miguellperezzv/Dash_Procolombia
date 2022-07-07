import pandas as pd
import prophet as prp
from prophet.plot import plot_plotly
import plotly.graph_objects as go
import plotly.express as px
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error #MSE

DIRECTORY= os.path.dirname(os.path.dirname(__file__))

finalCSV = pd.read_csv(DIRECTORY+r'/data/final.csv', sep = "|")
df = pd.read_csv(DIRECTORY+r'/data/final.csv', sep = "|")

actividades = [         {'label':'Agenda comercial de turismo' , 'value' : 'x1'}, 
                        {'label' : 'Agendas de Cooperación', 'value' :'x2'}, 
                        {'label' : 'Capacitaciones y presentaciones de destino' , 'value' : 'x3'},
                        {'label':'Entrega informacion valor agregado' ,'value' : 'x4'},  
                        {'label': 'FAM - PRESS Trips','value' : 'x5'}, 
                        {'label':'Feria internacional de Turismo' , 'value' :'x6'}, 
                        {'label':'Macrorruedas y Encuentros Comerciales' ,'value' : 'x7'},
                        {'label':'Otras Acciones promocion turismo' ,'value' : 'x8'}, 
                        {'label':'Primera Visita', 'value' :'x9'}, 
                ]

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
        colorscale = 'Darkmint',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Pasajeros',
    ))
    fig.update_geos(fitbounds="locations", visible=False)
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

def display_time_series(hub,selected_countries, start_date, end_date):
    f_start_date = start_date.date()
    start_date = pd.to_datetime(f_start_date)
    f_end_date = end_date.date()
    end_date = pd.to_datetime(f_end_date)
    
    df["llave"] = pd.to_datetime(df["llave"], format="%Y-%m")
    dff= df[(df['llave'] >= start_date) & (df['llave'] <= end_date)]
    dff=dff[dff['pais'].isin(selected_countries)]
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


def display_barplot(selected_countries,selected_activities,start_date, end_date):
    f_start_date = start_date.date()
    start_date = pd.to_datetime(f_start_date)
    f_end_date = end_date.date()
    end_date = pd.to_datetime(f_end_date)
    
    df["llave"] = pd.to_datetime(df["llave"], format="%Y-%m")
    dff= df[(df['llave'] >= start_date) & (df['llave'] <= end_date)]
    dff=dff[dff['pais'].isin(selected_countries)]

    dff=dff.groupby(['pais']).sum().reset_index()
     

    fig = px.bar(dff, x="pais",
                 y=selected_activities,
                 text_auto=True,
                 title="Total actividades de promoción por en el país",
                 labels={"variable":"actividad","value":"cantidad"})
    
    newnames = {'x1': 'Agenda comercial de turismo',
                'x2': 'Agendas de Cooperación',
                'x3': 'Capacitaciones y presentaciones de destino',
		'x4': 'Entrega información valor agregado',
                'x5': 'FAM - PRESS Trips',
                'x6': 'Feria internacional de Turismo',
                'x7': 'Macrorruedas y Encuentros Comerciales',
		'x8': 'Otras Acciones promoción turismo',
                'x9': 'Primera Visita',
}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

    return fig

def rezagos_total_pais(final,pais,reg):
    datos=final[final['pais']==pais]
    datos.set_index('llave',inplace = True)
    t=pd.DataFrame([])
    for a in range(reg):
        d=pd.DataFrame([])
        c=datos[['x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9']]
        c=c.shift(periods=a)
        d=pd.concat([d,c])
        if a==0:
            t=pd.concat([t,d],axis=1)
        else:
            d.columns=['x1_'+str(a), 'x2_'+str(a),'x3_'+str(a),'x4_'+str(a),'x5_'+str(a),'x6_'+str(a),'x7_'+str(a),'x8_'+str(a), 'x9_'+str(a)]
            d=d[['x1_'+str(a), 'x2_'+str(a),'x3_'+str(a),'x4_'+str(a),'x5_'+str(a),'x6_'+str(a),'x7_'+str(a),'x8_'+str(a), 'x9_'+str(a)]]
            t=pd.concat([t,d],axis=1)
    t=t.reset_index()
    datos=datos.drop(['pais','x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9'], axis=1)
    datos=datos.reset_index()
    verificacion=pd.merge(datos,t, on= ['llave'],how='inner')
    verificacion=verificacion.fillna(0)
        
    return verificacion



def rezagos_pais(final,pais,rezagos):
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
    return figFinal, dif.head(24), dif.tail(24)




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

    if resultados['modelo'][0]=='gradients':
        modelo=joblib.load('modelos/'+hub+'_retrazos_'+str(resultados['numero'][0])+'.joblib')
    else:
        modelo=joblib.load('modelos/'+hub+'_xbost_retrazos_'+str(resultados['numero'][0])+'.joblib')
    importancias=list(modelo.feature_importances_.round(5))

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
    print("TABLA TIPO " +str(type(table)))
    buenos=['agenda_comercial_de_turismo', 'agendas_de_cooperacion/_misiones',
        'capacitaciones_y_presentaciones_de_destino',
        'entrega_informacion_valor_agregado', 'fam_-_press_trips',
        'feria_internacional_de_turismo',
        'macrorruedas_y_encuentros_comerciales',
        'otras_acciones_promocion_turismo', 'primera_visita']
    tableActividades = table[table.variables.isin(buenos)]
    ## mejor modelo total rezagos
    '''
    resultados_1=pd.DataFrame()
    lista=[]
    numero=[]
    modeling=[]
    reales=['pais', 'cantidad_ciudades', 'educacion',
        'eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo',
        'transito', 'vacaciones', 'trm', 'estaciones', 'ipc',
        'carnavales', 'holiday', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8',
        'x9', 'x1_1', 'x2_1', 'x3_1', 'x4_1', 'x5_1', 'x6_1', 'x7_1', 'x8_1',
        'x9_1', 'x1_2', 'x2_2', 'x3_2', 'x4_2', 'x5_2', 'x6_2', 'x7_2', 'x8_2',
        'x9_2', 'x1_3', 'x2_3', 'x3_3', 'x4_3', 'x5_3', 'x6_3', 'x7_3', 'x8_3',
        'x9_3', 'x1_4', 'x2_4', 'x3_4', 'x4_4', 'x5_4', 'x6_4', 'x7_4', 'x8_4',
        'x9_4', 'x1_5', 'x2_5', 'x3_5', 'x4_5', 'x5_5', 'x6_5', 'x7_5', 'x8_5',
        'x9_5', 'x1_6', 'x2_6', 'x3_6', 'x4_6', 'x5_6', 'x6_6', 'x7_6', 'x8_6',
        'x9_6', 'x1_7', 'x2_7', 'x3_7', 'x4_7', 'x5_7', 'x6_7', 'x7_7', 'x8_7',
        'x9_7', 'x1_8', 'x2_8', 'x3_8', 'x4_8', 'x5_8', 'x6_8', 'x7_8', 'x8_8',
        'x9_8']
    for t,c in enumerate([gradient_total,xgboost_total]):
        verificacion=rezagos_total(finalCSV,hub,rez)
        X_train, X_test, y_train, y_test = train_test_split(verificacion[reales],verificacion[['pasajeros']], test_size=0.2, random_state=100, shuffle=True)
        predicciones = c.predict(X = X_test)
        rmse = mean_squared_error(
                y_true  = y_test,
                y_pred  = predicciones,
                squared = False
            )
        lista.append(rmse)
        if t==0:
            modeling.append('gradient')
        else:
            modeling.append('xgboost')
            

    resultados_1['metrica']=lista
    resultados_1['modelo']=modeling
    resultados_1=resultados_1.sort_values(by='metrica').reset_index(drop=True)
    resultados_1=resultados_1.head(1)'''

    return table, tableActividades
    #table

def tabla_influencia_destacados(pais, rez):
    ### leer los joblib del gradient
    directorio = DIRECTORY+r'/modelos_pais_destacado/'
    contenido = os.listdir(directorio)
    contador=0
    name=pais+'_retrazos_'
    name1=pais+'_retrazos_total'
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
    ### xgboost
    rename=pais+'_xbost_retrazos_'
    rename1=pais+'_xbost_retrazos_total'
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
    reales=['cantidad_ciudades','educacion','eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo','transito', 'vacaciones', 
            'x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9', 'trm','estaciones','ipc','carnavales','holiday']
    for a,c in enumerate(gradients):
        verificacion=rezagos_pais(finalCSV,pais,a)
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
        b='estados_unidos'
        verificacion=rezagos_pais(finalCSV,b,a)
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

    ## mejor modelo total rezagos
    resultados_1=pd.DataFrame()
    lista=[]
    numero=[]
    modeling=[]
    reales=['cantidad_ciudades', 'educacion',
        'eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo',
        'transito', 'vacaciones', 'trm', 'estaciones', 'ipc',
        'carnavales', 'holiday', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8',
        'x9', 'x1_1', 'x2_1', 'x3_1', 'x4_1', 'x5_1', 'x6_1', 'x7_1', 'x8_1',
        'x9_1', 'x1_2', 'x2_2', 'x3_2', 'x4_2', 'x5_2', 'x6_2', 'x7_2', 'x8_2',
        'x9_2', 'x1_3', 'x2_3', 'x3_3', 'x4_3', 'x5_3', 'x6_3', 'x7_3', 'x8_3',
        'x9_3', 'x1_4', 'x2_4', 'x3_4', 'x4_4', 'x5_4', 'x6_4', 'x7_4', 'x8_4',
        'x9_4', 'x1_5', 'x2_5', 'x3_5', 'x4_5', 'x5_5', 'x6_5', 'x7_5', 'x8_5',
        'x9_5', 'x1_6', 'x2_6', 'x3_6', 'x4_6', 'x5_6', 'x6_6', 'x7_6', 'x8_6',
        'x9_6', 'x1_7', 'x2_7', 'x3_7', 'x4_7', 'x5_7', 'x6_7', 'x7_7', 'x8_7',
        'x9_7', 'x1_8', 'x2_8', 'x3_8', 'x4_8', 'x5_8', 'x6_8', 'x7_8', 'x8_8',
        'x9_8']
    for t,c in enumerate([gradient_total,xgboost_total]):
        verificacion=rezagos_total_pais(finalCSV,b,rez)
        X_train, X_test, y_train, y_test = train_test_split(verificacion[reales],verificacion[['pasajeros']], test_size=0.2, random_state=100, shuffle=True)
        predicciones = c.predict(X = X_test)
        rmse = mean_squared_error(
                y_true  = y_test,
                y_pred  = predicciones,
                squared = False
            )
        lista.append(rmse)
        if t==0:
            modeling.append('gradient')
        else:
            modeling.append('xgboost')
            

    resultados_1['metrica']=lista
    resultados_1['modelo']=modeling
    resultados_1=resultados_1.sort_values(by='metrica').reset_index(drop=True)
    resultados_1=resultados_1.head(1)
    if resultados['modelo'][0]=='gradients':
        modelo=joblib.load(DIRECTORY+r'/modelos/paises/'+pais+'_retrazos_'+str(resultados['numero'][0])+'.joblib')
    else:
        modelo=joblib.load(DIRECTORY+r'/modelos/paises/'+pais+'_xbost_retrazos_'+str(resultados['numero'][0])+'.joblib')
    importancias=list(modelo.feature_importances_)

    a=['cantidad_ciudades','educacion',
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
    buenos=['agenda_comercial_de_turismo', 'agendas_de_cooperacion/_misiones',
       'capacitaciones_y_presentaciones_de_destino',
       'entrega_informacion_valor_agregado', 'fam_-_press_trips',
       'feria_internacional_de_turismo',
       'macrorruedas_y_encuentros_comerciales',
       'otras_acciones_promocion_turismo', 'primera_visita']
    table2 = table[table.variables.isin(buenos)]
    return table, table2

def display_heatmap_hub(selected_countries,selected_activity, start_date, end_date):
    f_start_date = start_date.date()
    start_date = pd.to_datetime(f_start_date)
    f_end_date = end_date.date()
    end_date = pd.to_datetime(f_end_date)
    
    df["llave"] = pd.to_datetime(df["llave"], format="%Y-%m")
    dff= df[(df['llave'] >= start_date) & (df['llave'] <= end_date)]
    dff=dff[dff['pais'].isin(selected_countries)]
    dff=dff.groupby(['pais','llave']).sum().reset_index()
    dff = dff[~(dff == 0).all(axis=1)]
    title_joined="Cantidad Actividades realizadas del tipo: "+selected_activity+" a lo largo del tiempo para los países seleccionados"

    fig = go.Figure(data=go.Heatmap(
            z=dff[selected_activity],
            x=dff['llave'],
            y=dff['pais'],
            colorscale='Blues'))
    fig.update_xaxes(
            dtick="M6",
            tickformat="%b\n%Y")
    fig.update_layout(
            xaxis_title="fecha",
            yaxis_title="pais",
            title=title_joined)
    return fig

def heatmap_visitors(hub, start_date,end_date):
    df["llave"] = pd.to_datetime(df["llave"], format="%Y-%m")
    dff=df[(df['hub']==hub) & (df['pais']!='venezuela') & (df['llave'] >= start_date) & (df['llave'] <= end_date)]
    dff=dff.groupby(['pais','llave']).sum().reset_index()
    title_joined="Cantidad llegada de pasajeros para región "+ hub

    fig = go.Figure(data=go.Heatmap(
            z=dff['pasajeros'],
            x=dff['llave'],
            y=dff['pais'],
            colorscale='Blues'))
    fig.update_xaxes(
            dtick="M6",
            tickformat="%b\n%Y")
    fig.update_layout(
            xaxis_title="fecha",
            yaxis_title="pais",
            title=title_joined)
    return fig


def getCountries():
    return finalCSV["pais"].unique()

def getCountriesByRegion(region):
    return finalCSV[finalCSV["hub"] == region]["pais"].unique()
    

def getRegions():
    return finalCSV["hub"].unique()

def getRegion(pais):
    region = finalCSV[finalCSV["pais"] == pais]["hub"].head(1)
    print("REGION ES "+ region)
    return region