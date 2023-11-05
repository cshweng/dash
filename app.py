# Import packages
from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

px.defaults.template = "ggplot2"
# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Alarm Table
df = pd.read_csv('~/Downloads/LoRA Sensors Alert.csv')
# Initialize the app
app = Dash(__name__)


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
# Sample Data

df2 = pd.read_csv('~/Downloads/plotly_test_LoRA.csv').sort_values('arrtime_0_converted')

df = df.iloc[:]
output = []
@callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def alarm_chart(rows, derived_virtual_selected_rows):
    
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)
    for index, row in dff.iterrows():
        df_o = df2[df2['deveui']==row['deveui']]
        df_o = df_o[['arrtime_0_converted', 'deveui',row['measurement']]]
        df_o = df_o[df_o[row['measurement']].notnull()]
        fig=px.line(df_o, x='arrtime_0_converted', y=row['measurement'])
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
        output.append(dcc.Graph(figure=fig,style={'height': '300px'}))
    
# App layout
app.layout = html.Div([
                    #html.Div([
                    #   dcc.Dropdown(
                    #        df['Alert Rule'].unique(),
                    #        df['Alert Rule'].unique(),
                    #        id='drop-down',
                    #        multi=True
                    #    ) 
                    #    ]),
                    html.Div([
                        dash_table.DataTable(
                            data=df.to_dict('records'), 
                            columns=[
                                {"name": i, 'id': i} for i in df.columns
                                ],
                            filter_action='native',
                            style_data={
                                'whiteSpace': 'normal',
                                'height': '300px',
                                'backgroundColor':colors['background'], 
                                'color':colors['text']
                                },
                            style_table={
                                'overflowY': 'auto', 
                                'backgroundColor':colors['background']
                                },
                            style_header={},
                            css=[{
                                    'selector': 'tr:first-child',
                                    'rule': 'display: none',
                                }]
                            )
                            ],
                        style={
                            'width': '45%', 
                            'float': 'left',
                            'backgroundColor':colors['background'] 
                            }
                        ),
                    html.Div(output ,style={'width': '55%', 'float': 'left'})
                    ],
                style={'backgroudnColor':colors['background']}
                )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

