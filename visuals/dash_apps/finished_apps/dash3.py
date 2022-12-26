from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
import json
from dash_bootstrap_templates import load_figure_template
load_figure_template("superhero")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = DjangoDash('demo3',external_stylesheets=[dbc.themes.SUPERHERO,dbc_css])
#app = Dash(__name__,external_stylesheets=[dbc.themes.CYBORG,dbc_css])
url = https://github.com/b-stead/demo/blob/30a4528235d1719003a3e4b316af5a5ca22f6266/visuals/data/df4.csv
df = pd.read_csv(url)

bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
aggfuncs = ['mean', 'max']
col_names = ['var', '', '50', '100', '150', '200', '250', '300', '350', '400', '450', '500']
dff = df[['Distance', 'Speed', 'SR', 'SplitD']]

dff.loc[:, 'splits']=pd.cut(dff['Distance'], bins)
dff=dff.groupby('splits')[['Speed', 'SR']].agg(aggfuncs)
dff=dff.round(1)
dff_t=dff.T
dff_t =dff_t.reset_index()
dff_t.columns = col_names

markdown_text = '''
    Accessing GPS data in a quick and efficient manner speeds up the evaluation and debrief of training and racing performances

    This service allows users too upload their GPS file to their account where it is available for the athlete and coach to share automatically.
    
    Speeding up this often time consuming process.

    Use the cursor to select the efort area. Once selected click "Get Data" button to extract split information

'''

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=df['Distance'], y=df['Speed'],
                mode='lines+markers',line=dict(width=1.5),
                name='speed'),secondary_y=False,)
fig.add_trace(
    go.Scatter(x=df["Distance"], y=df["SR"], mode='lines+markers',
    connectgaps= True, name= "Stroke Rate", line=dict(width=1.5,color='orange'),marker=dict(size=2, opacity=0.5)),
    secondary_y=True,
)
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=0.2),
    margin=dict(l=20, r=20, t=20, b=20),
    yaxis2_showgrid=False,
    )

app.layout = dbc.Container([
                html.Div([
                        dbc.Row([
                            dbc.Col(
                                html.H2('GPS Data ', className = 'text-center text-primary mb-4'),
                                width=11),
                        ]),
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
                            dcc.Graph(id="graph", figure = fig), 
                            dcc.Store(id='store-value',)
                        ], width=8),
                    ]),
                    dbc.Row([
                        dbc.Col([], width=1),
                        dbc.Col([
                            dbc.Label('Effort data', style={'fontWeight': 'bold'}),
                            dbc.Button('Get Data',id='button-1', color="success", n_clicks=0),

                            dash_table.DataTable(id='tbl', columns =[{"name": i, 'id': i} for i in dff_t.columns],
                                        data=dff_t.to_dict('records'), 
                                        style_header={'fontWeight': 'bold','textAlign': 'center'},
                                        style_cell={'textAlign': 'center'}),
                        ], width=8)
                    ])
                ]),
    ], fluid=True,className="dbc",)
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
        dff=dff.groupby('splits')[['Speed', 'SR']].agg(aggfuncs)
        dff=dff.round(1)
        dff_t=dff.T
        dff_t =dff_t.reset_index()
        dff_t.columns = col_names

        if n_clicks >=1:
            return dff_t.to_dict('records')

