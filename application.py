import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import pandas as pd
import time
import uuid
from backend.gdrive import get_data, get_dataframe
from backend.cache import get_cache
from scripts.startup import startup_development


if __name__ == '__main__':
    startup_development()


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True


cache = get_cache(app)


def serve_layout():
    session_id = str(uuid.uuid4())
    return html.Div([
        html.Div(session_id, id='session-id', style={'display': 'none'}),
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


app.layout = serve_layout


def render_data(session_id):
    return html.Div([
        html.Button('Refresh', id='refresh'),
        html.H3('Source Data'),
        html.Div([render_table_initial(session_id)], id='data-content')
    ])


def render_chart(session_id):
    return html.Div([
        html.H3('Plot'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=dt(1997, 5, 3),
            end_date_placeholder_text='To'
        ),
        # html.Div(id='slider-container'),
        dcc.Slider(
            id='plot-slider',
            min=0,
            max=1,
            step=0.05,
            value=0,
            updatemode='drag',
            marks={
                0: "none",
                1: "none2"
            }
        ),
        html.Div(id='plot-content')
    ])


@app.callback(
    Output('plot-slider', 'marks'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ])
def update_slider(start_date, end_date):
    marks = {
        0: str(start_date),
        1: str(end_date)
    }
    return marks


@app.callback(
    Output('plot-content', 'children'),
    [
        Input('plot-slider', 'value'),
        Input('session-id', 'children')
    ])
def render_chart_specific(val, session_id):
    df = cache.get(session_id)
    print(time.time())
    if df is None:
        df = get_dataframe()
        cache.set(session_id, df)
    return html.Div([
        html.H4(val),
        html.Pre(df.to_csv())
        ])


def render_table_initial(*args):
    return render_table(*args)


@app.callback(
    Output('data-content', 'children'),
    [
        Input('refresh', 'n_clicks'),
        Input('session-id', 'children')
    ])
def render_table_callback(nclicks, session_id):
    return render_table(session_id)

def render_table(session_id):
    df = get_dataframe()
    res = cache.set(session_id, df, timeout=5*60)
    return html.Pre(df.to_csv())


@app.callback(
    Output('tabs-content', 'children'),
    [
        Input('tabs', 'value'),
        Input('session-id', 'children')
    ])
def render_content(tab, session_id):
    if tab == 'tab-data':
        return render_data(session_id)
    elif tab == 'tab-chart':
        return render_chart(session_id)


application = app.server


if __name__ == '__main__':
    application.debug = False
    application.run(host="0.0.0.0")
