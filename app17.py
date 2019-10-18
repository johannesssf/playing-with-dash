import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

global_df = pd.read_csv('data_sample.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Bigger than 3.4', 'value': 1},
            {'label': 'Smaller then 3.4', 'value': 2}],
        value=1,
    ),
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}),
])


@app.callback(
    Output('intermediate-value', 'children'),
    [Input('dropdown', 'value')])
def clean_data(value):
    # some expensive clean data step
    cleaned_df = global_df[['Papel', 'Cotação']]
    if value == 1:
        cleaned_df = cleaned_df[cleaned_df['Cotação'] > 3.4]
    else:
        cleaned_df = cleaned_df[cleaned_df['Cotação'] <= 3.4]

    return cleaned_df.to_json(date_format='iso', orient='split')


@app.callback(
    Output('graph', 'figure'),
    [Input('intermediate-value', 'children')])
def update_graph(jsonified_cleaned_data):
    # more generally, this line wold be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    return go.Figure(data=[go.Bar(x=dff['Papel'], y=dff['Cotação'])])


@app.callback(
    Output('table', 'children'),
    [Input('intermediate-value', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    return html.Table(
        [html.Tr([html.Th(key) for key in dff.keys()])] +
        [html.Tr([html.Td(a), html.Td(b)]) for a, b in zip(dff['Papel'], dff['Cotação'])]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
