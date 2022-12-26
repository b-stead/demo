import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px
from dash import dcc, html
import dash
from dash import Input, Output
from dash_bootstrap_templates import load_figure_template
load_figure_template("superhero")

#dbc_css = dbc

#pylint: disable=too-many-arguments, unused-argument, unused-variable
#external_stylesheets = chriddyp

app = DjangoDash('demo1',external_stylesheets=[dbc.themes.SUPERHERO])
app.css.append_css({ "external_url" : "/static/assets/css/dbc.css" })
app.css.append_css({ "external_url" : "/static/assets/css/chriddyp.css" })

url = https://github.com/b-stead/demo/blob/7e52014c12781053352499aafb69a21d2ff769b6/visuals/data/Benchmarking.csv

df = pd.read_csv(url, encoding='UTF-8')

markdown_text = '''
    Performance data measured as a percentage from a standard. \n
    Click an Athlete to see their individual performance progression


'''
fig = px.scatter(df, x="Date", y="WLT%",color='Name',
                hover_name='Name', 
                hover_data=["Session"], 
                size_max=20)
fig.update_yaxes(autorange='reversed')

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H2("Longitudinal Performance Data", className = 'text-center text-primary mb-4'),
    width=12),
    ),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(children=markdown_text, className='text-white'),
                dcc.Graph(
                id='benchresults',
                figure=fig
            ),
        html.Div(id='athlete-plot')
            
        ]),
    ]),

],fluid=True)



@app.callback(
    Output("athlete-plot", 'children'),
    Input('benchresults', 'clickData')
)
def update_graph2(clickData):
    if clickData is None:
        return dash.no_update
    else:
        athlete_name = clickData['points'][0]['hovertext']

        dff = df[df['Name']==athlete_name[:]]
        dff=dff.sort_values(by='Date') 

    fig2 = px.scatter(dff, x='Date', y = 'WLT%',
            hover_name='Date',
            hover_data=['Date','Session'],
            title= athlete_name[:],
        )
    fig2.update_yaxes(autorange='reversed')

    return dcc.Graph(
        figure = fig2
    )
 
