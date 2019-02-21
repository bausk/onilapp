import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
from datetime import timedelta
import uuid
from backend.gdrive import get_dataframe
from backend.cache import get_cache
from backend.data import extract_from_df, date_from_timeline, all_to_average
from backend.vizualise import single_day


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


def render_chart_layout(session_id):
    end_date = dt.today()
    start_date = end_date - timedelta(days=100)
    return html.Div([
        html.H3('Plot'),
        html.Div([
            html.H5('Time Frame:'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dt.strftime(start_date, '%Y-%m-%d'),
                end_date=dt.strftime(end_date, '%Y-%m-%d'),
                end_date_placeholder_text='To'
            ),
        ]),
        html.Div([
            html.H5('Z Scale:'),
            dcc.Input(
                id='z-scale',
                type='number',
                value='100',
                min='1',
                max='10000'
            ),
        ]),
        html.Div([
            dcc.Slider(
                id='plot-slider',
                min=0,
                max=1,
                step=0.01,
                value=1,
                # updatemode='drag',
                marks={
                    0: str(start_date),
                    1: str(end_date)
                }
            )
        ], style={
            'marginBottom': 50,
            'marginTop': 25,
            'marginLeft': 100,
            'marginRight': 'auto',
            'max-width': '600px'
        }),
        html.Div([
            dcc.Graph(
                id='plot-content',
                style={
                    'max-height': '600',
                    'height': '60vh',
                    'max-width': '80vw'
                }
            )
        ],
            className='row',
            style={'margin-bottom': '20'}
        )
    ])


@app.callback(
    Output('plot-slider', 'marks'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ])
def update_slider_marks(start_date, end_date):
    marks = {
        0: str(start_date),
        1: str(end_date)
    }
    return marks


@app.callback(
    Output('plot-slider', 'step'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ])
def update_slider_step(start_date, end_date):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')
    diff = end - start
    step = 1 / int(diff.days)
    return step


@app.callback(
    Output('plot-content', 'figure'),
    [
        Input('plot-slider', 'value'),
        Input('session-id', 'children'),
        Input('z-scale', 'n-submit'),
        Input('z-scale', 'n-blur')
    ],
    [
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        State('plot-content', 'relayoutData'),
        State('z-scale', 'value'),
    ]
)
def render_chart(val, session_id, ns, nb, start_date, end_date, current_layout, scale):
    df = cache.get(session_id)
    if df is None:
        df = get_dataframe()
        cache.set(session_id, df)
    # 1. Get day
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')
    data = all_to_average(extract_from_df(
        df, date_from_timeline(start, end, val)))
    # 2. Get row

    initial_layout = {
        "title": "Inclination Chart",
        'margin': {
            'l': 10,
            'r': 10,
            'b': 10,
            't': 60,
        },
        'paper_bgcolor': '#FAFAFA',
        "hovermode": "closest",
        "scene": {
            "aspectmode": "manual",
            "aspectratio": {
                'x': 1,
                'y': 4,
                'z': 1
            },
            'camera': {
                'center': {'x': -0.3316074267231184, 'y': -0.5704900622086274, 'z': -0.8053651445188535},
                'eye': {'x': 1.5417545350375266, 'y': -2.987277065249906, 'z': 2.349161002992645},
                'up': {'x': 0, 'y': 0, 'z': 1}
                },
            "xaxis": {
                "title": "Width (m)",
                "range": [0, 30],
                "showbackground": True,
                "backgroundcolor": "rgb(230, 230,230)",
                "gridcolor": "rgb(255, 255, 255)",
                "zerolinecolor": "rgb(255, 255, 255)"
            },
            "yaxis": {
                "title": "Length (m)",
                "range": [0, 120],
                "showbackground": True,
                "backgroundcolor": "rgb(230, 230,230)",
                "gridcolor": "rgb(255, 255, 255)",
                "zerolinecolor": "rgb(255, 255, 255)"
            },
            "zaxis": {
                # "rangemode": "tozero",
                "title": "Z (m)",
                "range": [-3, 3],
                "showbackground": True,
                "backgroundcolor": "rgb(230, 230,230)",
                "gridcolor": "rgb(255, 255, 255)",
                "zerolinecolor": "rgb(255, 255, 255)"
            }
        },
    }
    if current_layout is not None:
        try:
            up = current_layout['scene.camera']['up']
            center = current_layout['scene.camera']['center']
            eye = current_layout['scene.camera']['eye']
            initial_layout['scene']['camera']['up'] = up
            initial_layout['scene']['camera']['center'] = center
            initial_layout['scene']['camera']['eye'] = eye
        except:
            pass
    layout = go.Layout(**initial_layout)
    # 2.2. Data.
    surface_points = single_day(data)

    trace1 = {
        "type": "mesh3d",
        'x': surface_points[0],
        'y': surface_points[1],
        'z': [x * float(scale) for x in surface_points[2]],
        'intensity': surface_points[2],
        'autocolorscale': True,
        # "colorscale": [
        #     [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"], [
        #         0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"],
        # ],
        "lighting": {
            "ambient": 1,
            "diffuse": 0.9,
            "fresnel": 0.5,
            "roughness": 0.9,
            "specular": 2
        },
        "flatshading": True,
        "reversescale": False
    }
    # 3. Plot
    data = [trace1]
    figure = dict(data=data, layout=layout)
    return figure


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
    cache.set(session_id, df, timeout=5*60)
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
        return render_chart_layout(session_id)


application = app.server


if __name__ == '__main__':
    application.debug = False
    application.run(host="0.0.0.0")
