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
from backend.gdrive import get_data
from backend.cache import get_cache
from scripts.startup import startup_development


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True


cache = get_cache(app)


def get_dataframe(session_id):
    def query_and_serialize_data(session_id):
        # expensive or user/session-unique data processing step goes here

        # simulate a user/session-unique data processing step by generating
        # data that is dependent on time
        now = datetime.datetime.now()

        # simulate an expensive data processing task by sleeping
        time.sleep(5)

        df = pd.DataFrame({
            'time': [
                str(now - datetime.timedelta(seconds=15)),
                str(now - datetime.timedelta(seconds=10)),
                str(now - datetime.timedelta(seconds=5)),
                str(now)
            ],
            'values': ['a', 'b', 'a', 'c']
        })
        return df.to_json()

    return pd.read_json(query_and_serialize_data(session_id))


def serve_layout():
    # session_id = str(uuid.uuid4())
    return html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(
                label='Data',
                value='tab-data',
                className='custom-tab',
                selected_className='custom-tab--selected'
                ),
            dcc.Tab(
                label='Chart',
                value='tab-chart',
                className='custom-tab',
                selected_className='custom-tab--selected'
                ),
        ]),
        html.Div(
            id='tabs-content',
            className='custom-tab-content'
            )
    ])

    # return html.Div([
    #     html.Div(session_id, id='session-id', style={'display': 'none'}),
    #     html.Button('Get data', id='button'),
    #     html.Div(id='output-1'),
    #     html.Div(id='output-2')
    # ])


app.layout = serve_layout


def render_data():
    return html.Div([
        html.Button('Refresh', id='refresh'),
        html.H3('Source Data'),
        html.Div([render_table_initial()], id='data-content')
    ])


@cache.memoize()
def render_chart():
    return html.Div([
        html.H3('Plot'),
        html.Div(id='plot-content')
    ])


def render_table_initial():
    return render_table()


@app.callback(Output('data-content', 'children'),
              [Input('refresh', 'n_clicks')])
def render_table_callback(nclicks):
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
    startup_development()
    application.debug = True
    application.run(host="0.0.0.0")
