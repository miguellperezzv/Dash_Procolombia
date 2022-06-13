import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm ### Sarimax
import numpy as np
import statsmodels.formula.api as smf


campañas=pd.read_csv('graficos\BD\campañas.csv') 


variable=campañas[['llave','pais_empresa','servicio']].groupby(['llave','pais_empresa','servicio']).size().reset_index()
variable.columns=['llave', 'pais_empresa', 'servicio', 'total']

prueba=variable[(variable['pais_empresa']=='mexico')]
mexico=prueba.pivot(index='llave', columns='servicio', values='total').reset_index().fillna(0)
mexico.columns=['ds','x1','x2','x3','x4','x5','x6','x7','x8']
mexico['ds']= pd.to_datetime(mexico['ds'])
ejercicio=pd.merge(c, mexico, on='ds',how='left').fillna(0)

m1 = Prophet()
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
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = m1.plot(forecast)