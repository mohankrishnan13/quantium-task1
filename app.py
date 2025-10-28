# app.py
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import numpy as np

# -------------------------
# 1. Load and prepare data
# -------------------------
df = pd.read_csv('output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# -------------------------
# 2. Initialize Dash app
# -------------------------
app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

# -------------------------
# 3. Define the app layout
# -------------------------
app.layout = html.Div([
    html.H1("Soul Foods Sales Visualiser", style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': 30}),

    html.Div(
        "Line chart showing Pink Morsels sales over time.",
        style={'textAlign': 'center', 'marginBottom': 20, 'fontSize': 18}
    ),

    html.Div([
        html.Label("Select Region:", style={'fontWeight': 'bold', 'marginRight': 10}),
        dcc.RadioItems(
            id='region-selector',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            inline=True,
            style={'marginBottom': 30}
        )
    ], style={'textAlign': 'center'}),

    dcc.Graph(
        id='visualization'
    )
], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '900px', 'margin': '0 auto'})


# -------------------------
# 4. Callback for updating chart
# -------------------------
@app.callback(
    Output('visualization', 'figure'),
    Input('region-selector', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    fig = px.line(
        filtered_df,
        x='date',
        y='sales',
        title=f'Pink Morsels Sales Over Time ({selected_region.title()})',
        labels={'date': 'Date', 'sales': 'Sales'}
    )

    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center'},
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#f9f9f9'
    )

    return fig


# -------------------------
# 5. Run app
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
