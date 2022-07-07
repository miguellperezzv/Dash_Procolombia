import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error #MSE
import joblib
import os


DIRECTORY= os.path.dirname(os.path.dirname(__file__))

final=pd.read_csv(DIRECTORY+r'/data/final.csv', sep = "|")






def rezagos_pais(final,pais,rezagos):
    if rezagos==0:
        verificacion=final[final['pais']==str(pais)]
    else:
        datos=final[final['pais']==pais]
        datos.set_index('llave',inplace = True)
        d=pd.DataFrame([])
        c=datos[['x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9']]
        c=c.shift(periods=rezagos)
        d=pd.concat([d,c])
        d = d.dropna(how='all')
        d=d.reset_index()
        datos=datos.drop(['pais','x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9'], axis=1)
        datos=datos.reset_index()
        verificacion=pd.merge(datos,d, on= ['llave'],how='inner')        
        
    return verificacion

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

def tablas_importancia_pais_destacado_rezagos(pais, rez):


    ### leer los joblib del gradient
    rez=9
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


    ## mejor modelo total rezagos
    resultados_1=pd.DataFrame()
    lista=[]
    numero=[]
    modeling=[]
    variables=[]
    for a in range(rez):
        if a ==0:
            variables=['x1', 'x2','x3','x4','x5','x6','x7','x8','x9']
        else:
            for b in ['x1_'+str(a), 'x2_'+str(a),'x3_'+str(a),'x4_'+str(a),'x5_'+str(a),'x6_'+str(a),'x7_'+str(a),'x8_'+str(a), 'x9_'+str(a)]:
                variables.append(b)
    reales=['cantidad_ciudades', 'educacion',
        'eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo',
        'transito', 'vacaciones', 'trm', 'estaciones', 'ipc',
        'carnavales', 'holiday']
    reales.extend(variables)

    for t,c in enumerate([gradient_total,xgboost_total]):
        verificacion=rezagos_total_pais(final,pais,rez)
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
    resultados_1


    if resultados_1['modelo'][0]=='gradient':
        modelo2=joblib.load(DIRECTORY+r'/modelos_pais_destacado/'+pais+'_retrazos_total.joblib')
    else:
        modelo2=joblib.load(DIRECTORY+r'/modelos_pais_destacado/'+pais+'_xbost_retrazos_total.joblib')
    importancias2=list(modelo2.feature_importances_)
    variables=[]
    for a in range(rez):
        if a ==0:
            variables=['agenda_comercial_de_turismo', 'agendas_de_cooperacion/_misiones',
        'capacitaciones_y_presentaciones_de_destino',
        'entrega_informacion_valor_agregado', 'fam_-_press_trips',
        'feria_internacional_de_turismo',
        'macrorruedas_y_encuentros_comerciales',
        'otras_acciones_promocion_turismo', 'primera_visita']
        else:
            for b in ['agenda_comercial_de_turismo_'+str(a), 'agendas_de_cooperacion/_misiones_'+str(a),'capacitaciones_y_presentaciones_de_destino_'+\
                    str(a),'entrega_informacion_valor_agregado_'+str(a),'fam_-_press_trips_'+str(a),'feria_internacional_de_turismo_'+\
                    str(a),'macrorruedas_y_encuentros_comerciales_'+str(a),'otras_acciones_promocion_turismo_'+str(a), 'primera_visita_'+str(a)]:
                variables.append(b)
    a=['cantidad_ciudades', 'educacion',
        'eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo',
        'transito', 'vacaciones','trm', 'estaciones', 'ipc',
        'carnavales', 'holiday']
    a.extend(variables)
    table=pd.DataFrame(a, columns = ['variables'])
    table['importancias']=importancias2
    table = table.sort_values('importancias',ascending=False).reset_index(drop=True)
    table = table[table.variables.isin(variables)]
    table=table.head(15)
    table['orden']=[a+1 for a in range(15)]
    table=table[['orden','variables']]
    return table

def tablas_actividades_destacadas(pais):
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
    resultados=pd.DataFrame()
    lista=[]
    numero=[]
    modeling=[]
    reales=['cantidad_ciudades','educacion','eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo','transito', 'vacaciones', 
            'x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9', 'trm','estaciones','ipc','carnavales','holiday']
    for a,c in enumerate(gradients):
        verificacion=rezagos_pais(final,pais,a)
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
        b=pais
        verificacion=rezagos_pais(final,b,a)
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
        modelo=joblib.load(DIRECTORY+r'/modelos_pais_destacado/'+pais+'_retrazos_'+str(resultados['numero'][0])+'.joblib')
    else:
        modelo=joblib.load(DIRECTORY+r'/modelos_pais_destacado/'+pais+'_xbost_retrazos_'+str(resultados['numero'][0])+'.joblib')
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
    table
    buenos=['agenda_comercial_de_turismo', 'agendas_de_cooperacion/_misiones',
        'capacitaciones_y_presentaciones_de_destino',
        'entrega_informacion_valor_agregado', 'fam_-_press_trips',
        'feria_internacional_de_turismo',
        'macrorruedas_y_encuentros_comerciales',
        'otras_acciones_promocion_turismo', 'primera_visita']
    table = table[table.variables.isin(buenos)]
    table['orden']=[a+1 for a in range(9)]
    table=table[['orden','variables']]
    return table, resultados