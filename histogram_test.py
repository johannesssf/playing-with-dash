import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data_sample.csv')
dff = df[['Papel', 'Cotação']]
xaxis = dff['Papel']
yaxis = dff['Cotação']

print(xaxis)
print(yaxis)
ybins = {
    'start': 0,
    'end': yaxis.max(),
}
fig = go.Figure(data=[go.Bar(x=xaxis, y=yaxis)])
fig.show()
