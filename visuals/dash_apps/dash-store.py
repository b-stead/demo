from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html
from dash import dcc, dash_table, Dash
import logging
from dash.exceptions import PreventUpdate
import json
from dash_bootstrap_templates import load_figure_template
load_figure_template("cyborg")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

#app = DjangoDash('demo3',external_stylesheets=[dbc.themes.CYBORG,dbc_css])
app = Dash(__name__,external_stylesheets=[dbc.themes.CYBORG,dbc_css])

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

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=df['Distance'], y=df['velocity'],
                mode='lines+markers',
                name='speed'),secondary_y=False,)
fig.add_trace(
    go.Scatter(x=df["Distance"], y=df["SRMean3"], mode='lines+markers',
    connectgaps= True, name= "Stroke Rate", line=dict(width=1.5,color='orange'),marker=dict(size=2, opacity=0.5)),
    secondary_y=True,
) 

app.layout = dbc.Container([
    html.Div([
        dbc.Row(
        html.Div([   
            dbc.Row(
                html.Div([
                    dcc.Graph(
                    id="graph", figure = fig           
                ), 
                dcc.Store(
                    id='store-value',)
                ])
            ),
        ])
    ),
    dbc.Row(
        html.Div([
        html.Div([            
            dcc.Markdown("""
                **Click Data**
                use the cursor to select the ara of the graph you want
            """),
            html.Pre(id='selection-data')
        ],)
    ]),
    ),
    dbc.Row(
            html.Div([
                dbc.Label('Effort data'),
                dbc.Button('Get Data',id='button-1', n_clicks=0),
            html.Div([
                dash_table.DataTable(id='tbl', columns =[{"name": i, 'id': i} for i in dff_t.columns],
                                data=dff_t.to_dict('records'), 
                                style_header={'fontWeight': 'bold','textAlign': 'center'},
                                style_cell={'textAlign': 'center'}),
                    ]),
            #dbc.Alert(id='tbl_out'),
            ]),
            ),
    ])
    ], fluid=True,
    className="dbc",
)

# markdown text of selected data
@app.callback(
    Output('selection-data', 'children'),
    Output('store-value', 'data'),
    Input('graph', 'relayoutData'))
def display_click_data(relayoutData, **kwargs):
    #print(relayoutData)
    #print(type(relayoutData))
    return json.dumps(relayoutData, indent=2), relayoutData

@app.callback(
    Output('tbl', 'data'),
    Input('graph', 'relayoutData'),
    Input('button-1', 'n_clicks'),
    prevent_initial_call=True)

def table_update(relayoutData, n_clicks, **kwargs):
    if n_clicks is None:
        return PreventUpdate
    else:
        xmin = relayoutData["xaxis.range[0]"]
        xmax = relayoutData["xaxis.range[1]"]
        #create stored data 
        tdf = df[df['Distance'].between(xmin, xmax)]
        tdf['Distance']=tdf.SplitD.cumsum()

        #convert to json for data store
        jsonified_df=tdf.to_json()

        #click event for table update import json data object
        dff = pd.read_json(jsonified_df, orient='columns')

        #calculations for new DF into table, work well. issue is return statement
        dff.loc[:, 'splits']=pd.cut(dff['Distance'], bins)
        dff=dff.groupby('splits')[['velocity', 'SRMean3']].agg(aggfuncs)
        dff=dff.round(1)
        dff_t=dff.T
        dff_t =dff_t.reset_index()
        dff_t.columns = col_names

        if n_clicks >=1:
            return dff_t.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)