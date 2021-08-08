# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
from plotly.io._renderers import nbformat

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': x, 'value': x} for x in
                                                      (['All Sites'] + list(spacex_df['Launch Site'].unique()))],
                                             value='All Sites',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                marks={0:'0', 2500:'2500', 5000:'5000', 10000:'10000'},
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def pie_chart(site):
    if site=='All Sites':
        df_total=pd.DataFrame.copy(spacex_df)
        fig = px.pie(df_total.groupby('Launch Site',as_index=False).sum(), values='class', names='Launch Site',
                         title='Total Success Launches by Site')
    else:
        df_site=spacex_df.loc[spacex_df['Launch Site']==site].groupby('class',as_index=False).count()
        fig = px.pie(df_site, values='Mission Outcome', names='class',
                         title='Total Success Launches by ' + site)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")])
def scatter_plot(site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    if site == 'All Sites':
        fig = px.scatter(spacex_df[mask], x='Payload Mass (kg)', y='class',
                         color="Booster Version Category",
                         title='Corellation betwee Payload and Success for All Sites')
    else:
        fig = px.scatter(spacex_df[mask].loc[spacex_df['Launch Site'] == site], x='Payload Mass (kg)', y='class',
                         color="Booster Version Category",
                         title='Corellation betwee Payload and Success for ' + site)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
