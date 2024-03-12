# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    html.Br(),
    dcc.Graph(id='success-pie-chart'),
html.Br(),
 dcc.RangeSlider(
        id='payload-slider',
        min=int(spacex_df['Payload Mass (kg)'].min()),
        max=int(spacex_df['Payload Mass (kg)'].max()),
        step=1000,
        marks={i: str(i) for i in range(int(spacex_df['Payload Mass (kg)'].min()), int(spacex_df['Payload Mass (kg)'].max()) + 1, 5000)},
        value=[int(spacex_df['Payload Mass (kg)'].min()), int(spacex_df['Payload Mass (kg)'].max())],
 ),
html.Br(),
dcc.Graph(id='scatter-chart'),
])
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        data = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts().reset_index()
        data.columns = ['Launch Site', 'Successful Launches']
        color_map = {'KSC LC-39A': 'blue', 'CCAFS LC-40': 'red', 'VAFB SLC-4E': 'green', 'CCAFS SLC-40': 'purple'}
        fig = px.pie(data, values='Successful Launches', names='Launch Site', title='Total Success Launches by Site', color='Launch Site', color_discrete_map=color_map)
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        data = filtered_df['class'].value_counts().reset_index()
        data.columns = ['class', 'count']
        fig = px.pie(data, values='count', names='class', title=f'Successful vs Failed Launches for Site {selected_site}')
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, selected_payload_range):
    # Filter DataFrame based on selected launch site and payload range
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= selected_payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= selected_payload_range[1])]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Launch Success')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

