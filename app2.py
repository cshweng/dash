
import plotly.graph_objs as go

import dash
from dash import dcc, html
from dash import dash_table
import plotly.express as px
import pandas as pd
# Sample data
df = pd.DataFrame({'X': [1, 2, 3, 4, 5], 'Y': [10, 11, 12, 11, 10]})

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of your app
app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'Column 1', 'id': 'X'},
            {'name': 'Column 2', 'id': 'Y'},
            {'name': 'Chart', 'id': 'Chart'},
        ],
        data=df.to_dict('records'),
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center'},
    ),
])

# Create a function to generate line charts
def generate_line_chart(x, y):
    fig = px.line(x=x, y=y)
    return dcc.Graph(figure=fig)

@app.callback(
    dash.dependencies.Output('table', 'data'),
    dash.dependencies.Input('table', 'data'),
)
def update_chart_column(data):
    updated_data = []

    for row in data:
        x = [row['X']]
        y = [row['Y']]

        # Generate a line chart for each row
        chart = generate_line_chart(x, y)

        updated_row = dict(row)
        updated_row['Chart'] = chart
        updated_data.append(updated_row)

    return updated_data

if __name__ == '__main__':
    app.run_server(debug=True)
