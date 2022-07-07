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

def display_map_single_region(start_date,end_date, hub): 
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


#PRINCIPAL MODIFICATIONS AFTER PROCOLOMBIA'S MEETING:
#this is the function to display the map per country
#IT ZOOMS TO THE COUNTRY A LOT, IT IS BETTER THE HUBS MAP

def display_map_single_country(start_date,end_date, country): 
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
        locations=dff[dff['pais'] == country]['codigo_pais'],       
        z = dff[dff['pais'] == country]['pasajeros'],
        text = dff[dff['pais'] == country]['pais'],
        colorscale = 'Darkmint',
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Pasajeros'
    ))
    
    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(
        title_text='Pasajeros por región y rango de fechas seleccionado',
        geo=dict(
            showframe=True,
            showland = False,
            showcountries = True,
            countrycolor = 'darkgray',
            countrywidth = 1,
    ))
    return fig





def display_time_series(selected_countries, start_date, end_date):
    print("SELECTED COUNTRRIESS")
    print(selected_countries)
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



def display_heatmap_hub(selected_countries,selected_activity, start_date, end_date):
    f_start_date = start_date.date()
    start_date = pd.to_datetime(f_start_date)
    f_end_date = end_date.date()
    end_date = pd.to_datetime(f_end_date)
    
    df["llave"] = pd.to_datetime(df["llave"], format="%Y-%m")
    dff= df[(df['llave'] >= start_date) & (df['llave'] <= end_date)]
    dff=dff[dff['pais'].isin(selected_countries)]
    dff=dff.groupby(['pais','llave']).sum().reset_index()
    
    removed_countries=[]
    
    for c in selected_countries:
        if ((dff[dff['pais']==c][selected_activity].sum())<5).all():
            removed_countries.append(c)
    print(removed_countries)
    
    selected_countries=list(set(selected_countries)-set(removed_countries))
    dff=finalCSV[finalCSV['pais'].isin(selected_countries)]
    dff=dff.groupby(['pais','llave']).sum().reset_index()
    
    title_joined="Cantidad Actividades realizadas del tipo: "+selected_activity+" a lo largo del tiempo para los países seleccionados"

    fig = go.Figure(data=go.Heatmap(
            z=dff[selected_activity],
            x=dff['llave'],
            y=dff['pais'],
            colorscale='Mint'))
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
            colorscale='Mint'))
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