# app.py
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import numpy as np

# -------------------------
# 1. Load and prepare data
# -------------------------
df = pd.read_csv('output.csv')
df['date'] = np.array(pd.to_datetime(df['date']))
df = df.sort_values('date')

# -------------------------
# 2. Initialize Dash app
# -------------------------
app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

# -------------------------
# 3. Create the visualization
# -------------------------
line_chart = px.line(
    df,
    x='date',
    y='sales',
    title='Pink Morsels Sales Over Time',
    labels={'date': 'Date', 'sales': 'Sales'}
)

visualization = dcc.Graph(
    id='visualization',
    figure=line_chart
)

# -------------------------
# 4. Define the app layout
# -------------------------
app.layout = html.Div([
    html.H1("Soul Foods Sales Visualiser", style={'textAlign': 'center'}),
    html.Div(
        "Line chart showing Pink Morsels sales over time.",
        style={'textAlign': 'center', 'marginBottom': 20}
    ),
    visualization
])

# -------------------------
# 5. Run app
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
