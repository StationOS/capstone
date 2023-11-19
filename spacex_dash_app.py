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


sites = list(spacex_df['Launch Site'].unique())
print(sites)
options=[]

d = {}
d['label'] = 'All Sites'
d['value'] = 'ALL'
options.append(d)

for s in sites:
    d = {}
    d['label'] = s
    d['value'] = s
    options.append(d)

marks = {}
m = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]

for ms in m:
    marks[str(ms)]=str(ms) 
 


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                            
                                dcc.Dropdown(id='site-dropdown',value='ALL',options=options,placeholder='Select a Launch Site here',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks=marks,
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):

    filtered_df1 = spacex_df[spacex_df['Launch Site']==entered_site]
    filtered_df = filtered_df1.groupby(['class']).sum()
    #print(filtered_df)

    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Successful Launches by Site',hole=.5)
        return fig
    else:
        fig = px.pie(filtered_df, values='Unnamed: 0', 
        names=filtered_df.index, 
        title='Total Successful Launches for '+entered_site,hole=.5)
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, slide_value):


    print(slide_value)

    filtered_df1 = spacex_df[spacex_df['Launch Site']==entered_site]

    filtered_df2 = filtered_df1[(filtered_df1['Payload Mass (kg)']>slide_value[0])&(filtered_df1['Payload Mass (kg)']<slide_value[1])]

    filtered_df3 = spacex_df[(spacex_df['Payload Mass (kg)']>slide_value[0])&(spacex_df['Payload Mass (kg)']<slide_value[1])]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df3, x= 'Payload Mass (kg)' , y = 'class',  
        color='Booster Version Category',
        title='Successes by Payload Mass')

        fig.update_traces(marker={'size': 15})
        return fig
    else:
        fig = px.scatter(filtered_df2, x= 'Payload Mass (kg)' , y = 'class',  
        color='Booster Version Category',
        title='Successes by Payload Mass for '+entered_site)
        fig.update_traces(marker={'size': 15})
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
