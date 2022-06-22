from dash import dash_table
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
details_table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])