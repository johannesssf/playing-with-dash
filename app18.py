import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.graph_objects as go

global_df = pd.read_csv('data_sample.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'P/L', 'value': 'P/L'},
            {'label': 'P/VP', 'value': 'P/VP'},
            {'label': 'PSR', 'value': 'PSR'}],
        value='P/L',
    ),
    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    dcc.Graph(id='graph3'),
    html.Table(id='table'),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}),
])


@app.callback(
    Output('intermediate-value', 'children'),
    [Input('dropdown', 'value')])
def clean_data(value):
    # an expensive query step
    cleaned_df = pd.read_csv('data_sample.csv')

    # a few filter steps that compute the data
    # as it's needed in the future callbacks
    df_1 = cleaned_df[['Papel', 'P/L']]
    df_2 = cleaned_df[['Papel', 'P/VP']]
    df_3 = cleaned_df[['Papel', 'PSR']]

    datasets = {
        'df_1': df_1.to_json(orient='split', date_format='iso'),
        'df_2': df_2.to_json(orient='split', date_format='iso'),
        'df_3': df_3.to_json(orient='split', date_format='iso'),
    }

    return json.dumps(datasets)


@app.callback(
    Output('graph1', 'figure'),
    [Input('intermediate-value', 'children')])
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_1'], orient='split')

    return go.Figure(
        layout_title_text='P/L',
        data=[go.Bar(x=dff['Papel'], y=dff['P/L'])])


@app.callback(
    Output('graph2', 'figure'),
    [Input('intermediate-value', 'children')])
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_2'], orient='split')

    return go.Figure(layout_title_text='P/VP',
    data=[go.Bar(x=dff['Papel'], y=dff['P/VP'])])


@app.callback(
    Output('graph3', 'figure'),
    [Input('intermediate-value', 'children')])
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_3'], orient='split')

    return go.Figure(layout_title_text='PSR',
                     data=[go.Bar(x=dff['Papel'], y=dff['PSR'])])


if __name__ == "__main__":
    app.run_server(debug=True)
