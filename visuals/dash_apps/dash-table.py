from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, dash_table, Dash
import logging
from dash.exceptions import PreventUpdate
import json
from dash_bootstrap_templates import load_figure_template
load_figure_template("cyborg")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

#app = DjangoDash('demo3',external_stylesheets=[dbc.themes.CYBORG,dbc_css])
app = Dash(__name__)
df = pd.read_csv('df4.csv')

bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
aggfuncs = ['mean', 'max']
col_names = ['var', '', '50', '100', '150', '200', '250', '300', '350', '400', '450', '500']
dff = df[['Distance', 'velocity', 'SRMean3', 'SplitD']]

dff.loc[:, 'splits']=pd.cut(dff['Distance'], bins)
dff=dff.groupby('splits')[['velocity', 'SRMean3']].agg(aggfuncs)
dff=dff.round(1)
dff_t=dff.T
dff_t =dff_t.reset_index()
dff_t.columns = col_names

app.layout = dbc.Container([
            dbc.Row(
                html.Div([
                    dbc.Label('Effort data'),
                    dbc.Button('Get Data',id='button-1', n_clicks=0),
                html.Div([
                    dash_table.DataTable(id='tbl', columns =[{"name": i, 'id': i} for i in dff_t.columns],
                                    data=dff_t.to_dict('records'),
                    ),]),
                dbc.Alert(id='tbl_out'),
                ]),
            ),
        ],fluid=True,
    className="dbc",)


@app.callback(
    Output('tbl', 'data'),
    Input('button-1', 'n_clicks'),
    prevent_initial_call=True)

def table_update(n_clicks):
    if n_clicks is None:
        return PreventUpdate
    xmin = 56.9388058446112
    xmax  = 557
    #create stored data 
    tdf = df[df['Distance'].between(xmin, xmax)]
    tdf['Distance']=tdf.SplitD.cumsum()

    #convert to json for data store
    jsonified_df=tdf.to_json()

    #click event for table update import json data object
    df2 = pd.read_json(jsonified_df, orient='columns')

    #calculations for new DF into table, work well. issue is return statement
    df2.loc[:, 'splits']=pd.cut(df2['Distance'], bins)
    df2=df2.groupby('splits')[['velocity', 'SRMean3']].agg(aggfuncs)
    df2=df2.round(1)
    df2_t= df2.T
    df2_t = df2_t.reset_index()
    df2_t.columns = col_names

    if n_clicks >=1:
        return df2_t.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
