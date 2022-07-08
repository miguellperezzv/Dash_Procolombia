import pandas as pd
import holidays
from sklearn.impute import KNNImputer


print("Processing Viajeros.csv Dataset\n")
viajes=pd.read_excel('data/viajeros.xlsb', sheet_name='Motivo de viaje')

viajes.columns=['anio','mes','pais','ciudad','total','visitantes']
viajes['mes'] = viajes['mes'].replace({'enero':'01','febrero':'02','marzo':'03','abril':'04','mayo':'05','junio':'06',
                                       'julio':'07','agosto':'08','septiembre':'09','octubre':'10','noviembre':'11','diciembre':'12'}, regex=True)
viajes['ciudad']=viajes['ciudad'].str.split(',',expand=True)[0].replace({'á':'a','é':'e','ó':'o','í':'i','ú':'u'}, regex=True)
viajes['ciudad']=viajes['ciudad'].str.lower()
viajes['pais']=viajes['pais'].str.lower()
viajes['pais']=viajes['pais'].replace({'á':'a','é':'e','ó':'o','í':'i','ú':'u',' ':'_'}, regex=True)
viajes['total'] = viajes['total'].str.split(' ',expand=True)[0].replace({'á':'a','é':'e','ó':'o','í':'i','ú':'u',',':''}, regex=True)
viajes['total'] = viajes['total'].replace({'NO':'sin_motivo'})
viajes['total']=viajes['total'].str.lower()
viajes['total']=viajes['total'].astype('category')
viajes['motivos']=viajes['total'].cat.codes
viajes['llave']=viajes['anio'].astype('str')+'-'+viajes['mes']
#viajes['visitantes']=viajes['visitantes'].str.replace(',','.')
#viajes['visitantes']=viajes['visitantes'].astype(float).astype(int)

print("Processing frecuencias.csv Dataset\n")

vuelos=pd.read_csv('data/frecuencias.csv',encoding='latin-1',sep=';')
vuelos.columns=['pais','anio','mes','frecuencia','sillas']
vuelos['frecuencia']=vuelos['frecuencia'].str.replace(',','.')
vuelos['frecuencia']=vuelos['frecuencia'].astype(float).astype(int)
vuelos['sillas']=vuelos['sillas'].str.replace(',','.')
vuelos['sillas']=vuelos['sillas'].astype(float).astype(int)
vuelos['pais']=vuelos['pais'].str.lower()
vuelos['pais']=vuelos['pais'].replace({'á':'a','é':'e','ó':'o','í':'i','ú':'u'})
vuelos['llave']=vuelos['anio'].astype('str')+'-'+vuelos['mes'].astype('str').str.zfill(2)
vuelos=vuelos[['llave','pais','frecuencia','sillas']]

print("Processing festivos Dataset\n")
### festivos
years_list =[2017,2018,2019,2020,2021,2022,2023]

# The holidays in CO
co = []
for x in years_list:
    for ptr in holidays.CO(years = x).items():
        co.append({ 'date': ptr[0], 'holiday': ptr[1]})

df = pd.DataFrame.from_records(co)
df['llave'] = pd.to_datetime(df['date']).dt.to_period('M')
df_holidays_month = pd.DataFrame(df.groupby('llave').holiday.count()).reset_index()
df_holidays_month['llave']=df_holidays_month['llave'].astype(str)

print("Processing Fechas Carnavales.xlsx Dataset\n")

## carnavales
carnavales=pd.read_excel('data/carnavales.xlsx')
carnavales.columns=['fecha','dia','festividad']
carnavales['anio']=carnavales['fecha'].astype(str).str.split('-',expand=True)[0]
carnavales['mes']=carnavales['fecha'].astype(str).str.split('-',expand=True)[1]
carnavales['llave']=carnavales['anio'].astype('str')+'-'+carnavales['mes'].astype('str').str.zfill(2)
m=carnavales.groupby(['llave','festividad']).count().reset_index()
carnavales=m.groupby(['llave'])['anio'].count().reset_index()

carnavales.columns=['llave','carnavales']


print("Processing Fechas TRM.xlsx Dataset\n")

### trm
trm=pd.read_excel('data/TRM.xlsx')
trm.drop(trm.index[:7], inplace=True)
trm.drop(trm.tail(4).index,inplace = True)
trm.rename(columns={ trm.columns[0]: "llave", trm.columns[1]: "TRM"  }, inplace = True)
trm['llave'] = pd.to_datetime(trm['llave']).dt.to_period('M')
trm=trm.groupby(['llave']).mean().reset_index().astype(str)



print("Processing IPC_Variacion_mensual_2003_a_2022.csv Dataset\n")
## ipc
ipc=pd.read_csv('data/IPC.csv',sep=';',encoding='cp1252')
ipc['mes']=ipc['mes'].str.lower()
ipc['mes'] = ipc['mes'].replace({'enero':'01','febrero':'02','marzo':'03','abril':'04','mayo':'05','junio':'06',
                                       'julio':'07','agosto':'08','septiembre':'09','octubre':'10','noviembre':'11','diciembre':'12'})
ipc['ipc']=ipc['ipc'].str.replace(',','.')
ipc['ipc']=ipc['ipc'].astype(float)
ipc['llave']=ipc['anio'].astype('str')+'-'+ipc['mes'].astype('str')
ipc=ipc[['llave','ipc']]

print("Processing Clima por HUB.xlsx Dataset\n")
### estaciones 
estaciones=pd.read_excel('data/clima.xlsx')
lista=['Hub', 'Mes','Clima']
for columnas in lista:
    estaciones[columnas] = estaciones[columnas].replace({'á':'a','é':'e','ó':'o','í':'i','ú':'u',' ':''}, regex=True)
    estaciones[columnas] = estaciones[columnas].str.lower()
estaciones['Mes_No']=estaciones['Mes_No'].astype(int).astype(str)
estaciones['Año']=estaciones['Año'].astype(int).astype(str)
estaciones['llave']=estaciones['Año']+'-'+estaciones['Mes_No'].str.zfill(2)
estaciones['Clima']=estaciones['Clima'].astype('category')
estaciones['estaciones']=estaciones['Clima'].cat.codes
estaciones=estaciones[['Hub','llave', 'estaciones']]



print("Processing campañas.csv Dataset\n")
campañas=pd.read_excel('data/campanas.xlsx',sheet_name='Base de datos')
campañas.drop(campañas.index[:2], inplace=True)
campañas.drop(campañas.tail(1).index,inplace = True)
campañas.rename(columns={ campañas.columns[0]: "servicio", campañas.columns[1]: "anio", campañas.columns[2]: "fecha_servicio", campañas.columns[3]: "empresa", campañas.columns[4]: "pais_empresa"  }, inplace = True)
lista=['servicio','pais_empresa']
for columnas in lista:
    campañas[columnas] = campañas[columnas].replace({'á':'a','é':'e','ó':'o','í':'i','ú':'u',' ':'_'}, regex=True)
    campañas[columnas] = campañas[columnas].str.lower()
campañas['llave'] = campañas['anio'].astype(str)  +'-'+ campañas['fecha_servicio'].replace({'ene':'01','feb':'02','mar':'03','abr':'04','may':'05','jun':'06',
                                       'jul':'07','ago':'08','sep':'09','oct':'10','nov':'11','dic':'12'})
campañas.to_csv('data/campañas.csv',sep='|',index=False)




print("Merging Dataset\n")
ipc=pd.merge(ipc,carnavales, on=['llave'],how='left')
ipc=pd.merge(ipc,df_holidays_month, on=['llave'],how='left')
trm=pd.merge(trm,ipc, on=['llave'],how='left')


#viajes
a=viajes.groupby(['llave','pais','total'])['total'].agg(['count']).reset_index()
a.columns=['llave','pais','total','motivos']
a=a.pivot(index=['llave','pais'], columns='total', values='motivos').reset_index().fillna(0)

b=viajes.groupby(['llave','pais'])['visitantes'].agg(['sum']).reset_index()
b.columns=['llave','pais','pasajeros']

c=viajes.groupby(['llave','pais'])['ciudad'].agg(['unique']).reset_index()
c.columns=['llave','pais','cantidad_ciudades']
lista=[]
for indice in range(len(c)):
    lista.append(len(c['cantidad_ciudades'][indice]))
c['cantidad_ciudades']=lista
c['pasajeros']=b['pasajeros']

base=pd.merge(c,a, left_on=['llave','pais'] ,right_on= ['llave','pais'],how='left')

hub=pd.read_csv('data/hubs.csv',encoding='latin-1',sep=';')
hub.columns=['hub','oficina','paises']

lista=['hub','oficina','paises']
for columnas in lista:
    hub[columnas] = hub[columnas].str.strip()
    hub[columnas] = hub[columnas].replace({'á':'a','é':'e','ó':'o','í':'i','ú':'u',' y ':',',' ':'_'}, regex=True)
    hub[columnas] = hub[columnas].str.lower()
print("-hub")    

hub['hub']=hub['hub'].replace({'alianza_pacifico':'alianzapacifico'})

oficinas=list(hub['hub'].unique())

dic={}
paises=list(base['pais'].unique())
for i in range(len(paises)):
    for j in range(len(hub['paises'].unique())):
        if paises[i] in hub['paises'][j]:
            dic[paises[i]]=hub['hub'][j]
            break
        else:
            pass   

base['hub']=base['pais'].replace(dic)

base=pd.merge(base,vuelos,on=['llave','pais'],how='left')

base=pd.merge(base,estaciones, left_on=['llave','hub'] ,right_on= ['llave','Hub'],how='left')
#base
print("-base")

# ## Filtrar bases



base_limpia = base[base.hub.isin(list(hub['hub'].unique()))]
print("-base 2")

campañas_limpias = campañas[campañas.pais_empresa.isin(list(base_limpia['pais'].unique()))]
#campañas_limpias
print("-cmpgn clean")

resumen=campañas_limpias.groupby(['llave','pais_empresa','servicio']).size().reset_index()
resumen.columns=['llave','pais_empresa','servicio','total']


resumen_3=base_limpia[base_limpia.pais.isin(list(campañas_limpias['pais_empresa'].unique()))]
#resumen_3
print("-res3")


# ### imputar datos perdidos de la serie de pasajeros

periodos=resumen_3[resumen_3['pais']=='alemania']['llave'].to_list()

country=list(resumen_3['pais'].unique())

#for a in country:


country.remove("martinica")
country.remove("oman") 
country.remove("guadalupe")
country.remove("curazao") 
country.remove("papua_nueva_guinea")


imputado=pd.DataFrame([])
arreglado=pd.DataFrame([])
for a in range(len(country)):
    imputado['llave']=periodos
    imputado['pais']=[country[a]for i in range(len(periodos))]
    arreglado=pd.concat([arreglado,imputado])

print("-imputar")
resumen_3=pd.merge(arreglado,resumen_3, on=['llave','pais'] ,how='left')
resumen_3['hub']=resumen_3['pais'].replace(dic)
#resumen_3
print("-res 3.1")

resumen_3=resumen_3[resumen_3['llave']<'2020-03']


imputer = KNNImputer(n_neighbors=12, weights="uniform")
imputacion=[]
imputacion2=[]
for a in country:
    a=resumen_3[resumen_3['pais']==a]
    imputer.fit(a[["pasajeros"]])
    imputacion.extend(imputer.transform(a[["pasajeros"]]).ravel())
    imputer.fit(a[["cantidad_ciudades"]])
    imputacion2.extend(imputer.transform(a[["cantidad_ciudades"]]).ravel())
    
resumen_3["pasajeros-inputados"] = imputacion
resumen_3['cantidad_ciudades-inputados']=imputacion2
resumen_3.loc[resumen_3.cantidad_ciudades.isnull(),'sin_motivo']=resumen_3['cantidad_ciudades-inputados']
for a in ['pasajeros-inputados','cantidad_ciudades-inputados','sin_motivo']:
    resumen_3[a]=resumen_3[a].apply(round)
print("-imputar 2")


resumen_4=resumen.pivot(index=['llave','pais_empresa'], columns='servicio', values='total').reset_index().fillna(0)


# ## unir base final


final=pd.merge(resumen_3,resumen_4, left_on=['llave','pais'] ,right_on= ['llave','pais_empresa'],how='left')
final=pd.merge(final,trm, on=['llave'],how='left')
final=final[['llave', 'pais', 'cantidad_ciudades-inputados', "pasajeros-inputados", 'educacion',
       'eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo',
       'transito', 'vacaciones', 'hub',
       'agenda_comercial_de_turismo', 'agendas_de_cooperacion/_misiones',
       'capacitaciones_y_presentaciones_de_destino',
       'entrega_informacion_valor_agregado', 'fam_-_press_trips',
       'feria_internacional_de_turismo',
       'macrorruedas_y_encuentros_comerciales',
       'otras_acciones_promocion_turismo', 'primera_visita',
       'TRM','estaciones','ipc','carnavales','holiday']].fillna(0)
final=final.rename(columns={'cantidad_ciudades-inputados':'cantidad_ciudades','pasajeros-inputados':'pasajeros'})
#final
print("-merge final")


final.columns=['llave', 'pais', 'cantidad_ciudades', 'pasajeros', 'educacion',
       'eventos', 'negocios', 'otros', 'religion', 'salud', 'sin_motivo',
       'transito', 'vacaciones', 'hub', 
       'x1', 'x2','x3','x4','x5','x6','x7','x8', 'x9', 'trm','estaciones','ipc','carnavales','holiday']


final.to_csv('data/final.csv',sep='|',index=False)
print("-to csv")

