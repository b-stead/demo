
from django.core.cache import cache
import dash
from dash import dcc, html, Input, Output, callback
from dash.dependencies import MATCH, ALL
import pandas as pd
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
import json
from django_plotly_dash import DjangoDash
from django_plotly_dash.consumers import send_to_pipe_channel
from django.utils.translation import gettext, gettext_lazy as _

from dash_bootstrap_templates import load_figure_template
load_figure_template("superhero")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
#pylint: disable=too-many-arguments, unused-argument, unused-variable

external_stylesheets = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = DjangoDash('demo2', external_stylesheets=[dbc.themes.SUPERHERO,dbc_css])

url = https://github.com/b-stead/demo/blob/1a6744f5df1e9a303838c1b1edc2911c1df9ab57/visuals/data/Benchmark-2.csv
url2 = https://github.com/b-stead/demo/blob/1a6744f5df1e9a303838c1b1edc2911c1df9ab57/visuals/data/latest.csv
    
df = pd.read_csv(url)
dflt = pd.read_csv(url2)
df['Date']=pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime("%Y/%m/%d")
aggfuncs=['min']

max_val = df['Long%'].max().max()
sizes = [np.max([max_val/5, val]) for val in df['Short%'].values]
df['Index']=df['Short%']/df['Long%']
dfl = df.sort_values('Date').groupby('Name').tail(1)

markdown_text = '''
    Need to keep track visually of your athlete progression over time?
    
    Here we are looking at Peak Speed(10m) against a Maximal Aerobic Effort (1500m).
  
    Click on a marker to see that individuals longitudinal performances

    WC: Womens Canoe, WK: Womens Kayak, MC: Mens Canoe, MK: Mens Kayak
'''

fig = px.scatter(dfl, x='LongSpeed', y='ShortV', color='Class',
        size='ShortV',
        labels={'x': 'Max Aerobic', 'y':'Max Speed'},
        hover_name='Name',
        hover_data={'Name':True, 'Date': True, 'Long':True, 'Short':True, 'LongSpeed':False, 'ShortV':False},
        symbol='Class',
        )
fig.update_xaxes(range=[10, 17])
fig.update_layout(
    xaxis_title="MAS(1500m)", 
    yaxis_title="Peak Speed",
    )

app.layout = dbc.Container([
    html.Div([
            dbc.Row([
        dbc.Col(
            html.H2('Benchmark Profile ', className = 'text-center text-primary mb-4'),
        width=11),
    ]),

    html.Div([
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([
                dcc.Markdown(children=markdown_text),
            ], width=11),
            
        ])
    ]),
    html.Div([
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([                    
                    dcc.Graph(id='bench-graph',
                    figure=fig),
            ], width=5),
            dbc.Col([
                    html.Div( id='indiv-graph') 
            ], width=5)
        ]),
    ]),
])
],fluid=True, className="dbc")


@app.callback(
    Output('indiv-graph', 'children'),
    Input('bench-graph', 'clickData')
)
def update_graph(clickData):
    if not clickData:
        return dash.no_update
       
    athlete_name = clickData['points'][0]['customdata']
    dff = df[df['Name']== athlete_name[0]]
    
    dff=dff.sort_values(by='Date')

    return dcc.Graph(
        figure = px.line(dff, x='Date', y=['PkV','ShortV', 'MedV','LongV'],
            labels={'x': 'Date', 'PkV':'Speed (m/s)'},
            hover_name='Date',
            hover_data=['Name','Long','Short', 'Med'],

            title= athlete_name[0],
            markers=True,
        )
    )
