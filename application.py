import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
from flask_caching import Cache
import os
import pandas as pd
import time
import uuid
from backend.dummydata import get_data


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True


def serve_layout():
    return html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Data', value='tab-data'),
            dcc.Tab(label='Chart', value='tab-chart'),
        ]),
        html.Div(id='tabs-content')
    ])

app.layout = serve_layout


def render_data():
    return html.Div([
        html.Button('Refresh', id='refresh'),
        html.H3('Source Data'),
        html.Div([render_table_initial()], id='data-content')
    ])


def render_chart():
    return html.Div([
        html.H3('Plot'),
        html.Div(id='plot-content')
    ])


def render_table_initial():
    return render_table()


@app.callback(Output('data-content', 'children'),
              [])
def render_table_callback():
    return render_table()


def render_table():
    data = get_data()
    headers = data.pop(0)
    print(headers)
    df = pd.DataFrame(data, columns=headers)
    return html.Pre(df.to_csv())

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-data':
        return render_data()
    elif tab == 'tab-chart':
        return render_chart()


application = app.server


if __name__ == '__main__':
    application.debug = True
    application.run(host="0.0.0.0")
