"""
Grazioso Salvare Dashboard
Interactive web application for filtering and visualizing rescue dog candidates
from Austin Animal Center shelter data.
Last Updated: 12 December 2025
"""

from dash import Dash, html, Input, Output, dcc, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_leaflet as dl
import base64

# import controller
from animal_shelter import AnimalShelter


db = AnimalShelter()
df = pd.DataFrame.from_records(db.read({}))
df.drop(columns=['_id'], inplace=True)

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

# encode logo to base64 string
binary_img = open('Grazioso Salvare Logo.png', 'rb').read()
encoded_img = base64.b64encode(binary_img)

app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    # Anchor component with requested logo and link
                    html.A([
                        html.Img(
                            src='data:image/png;base64,{}'.format(encoded_img.decode()),
                            style={
                                'height': '300px',
                                'width': 'auto',
                                'objectFit': 'contain'
                            }
                        )
                    ], href='https://www.snhu.edu', target='_blank')
                ], xs=12, md=4, className='d-flex align-items-center justify-content-center'),
                dbc.Col([
                    html.Div([
                        html.H2('Welcome to the Grazioso Salvare Dashboard', className='card-title mb-2 mt-2'),
                        html.P([
                            "This dashboard helps identify rescue dog candidates from Austin-area animal shelters. "
                            "Use the filters below to search for dogs matching specific rescue profiles: ",
                            html.Br(),
                            html.Strong("Water Rescue"), ", ",
                            html.Strong("Mountain/Wilderness Rescue"), ", or ",
                            html.Strong("Disaster/Individual Tracking"), ". ",
                            html.Br(),
                            "Each rescue type has preferred breed, age, and sex criteria"
                            " optimized for training success.",
                        ], className='card-text mb-3', style={'font-size':'20px'}),
                        html.P("This dashboard was built by Sarah Dowd 💾",
                           className='text-muted small mb-0')
                    ])
                ], xs=12, md=8, className='mb-0'),
            ], className='mb-4 d-flex align-items-center justify-content-center'),
        ])
    ], style={ 'backgroundColor' : '#faf8f5' }, className='shadow-sm mb-4 m-5'),
    dbc.Container([
        dbc.Card([
           dbc.CardBody([
               dbc.Row([
                   dbc.Col(html.H5('Filter by Rescue Type', className='card-title mb-0')),
                   dbc.Col(
                       dbc.Button(
                           "Export to CSV",
                           id='export-button',
                           n_clicks=0,
                           class_name='me-1',
                           outline=True,
                           size='sm',
                           color='light',
                       ), width='auto'
                   )
               ], justify='between', align='center', class_name='mb-3'),
                # dropdown menu with rescue type filters requested by client
                dcc.Dropdown(['Water Rescue', 'Mountain Rescue', 'Disaster Rescue', 'Reset'],
                            placeholder='Select Rescue Type', id='dropdown-filter',
                             style=
                                {
                                    'color': '#2c3e50',
                                }),
           ], style={'color': 'white',
                    'backgroundColor': '#2c3e50',
                     'borderRadius': '8px'},
                className='p-3'),
                dcc.Download(id='download-dataframe-csv')
        ]),
        # data table displays shelter data--selectable rows, native pagination, 10 rows per page
        # cells left-aligned with max width, table scrolls horizontally, sorting enabled
        dash_table.DataTable(data=df.to_dict('records'),
                            columns=[
                                {
                                    'name' : i.replace('_', ' ').title(), # transform from snake case to title case
                                    'id' : i,
                                    'deletable' : False,
                                    'selectable' : True
                                } for i in df.columns],
                            row_selectable='single',
                            page_action='native',
                            sort_action='native',
                            page_size=10,
                            page_current=0,
                            id='shelter-table',
                            style_cell=
                                {
                                    'textAlign' : 'left',
                                    'height': 'auto',
                                    'minWidth': '90px',
                                    'width': '180px',
                                    'maxWidth': '180px',
                                    'textOverflow' : 'ellipsis',
                                },
                            style_table=
                                {
                                    'overflowX': 'auto',
                                    'borderRadius': '8px'
                                },
                            style_data=
                                {
                                    'backgroundColor': '#faf8f5',
                                    'fontFamily': '"Ubuntu", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
                                },
                            style_header=
                                {
                                    'color': 'white',
                                    'backgroundColor': '#2c3e50',
                                    'fontFamily': '"Ubuntu", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
                                },
                                css=[{
                                        'selector': 'input[type="radio"]:checked',
                                        'rule': 'accent-color: #c9341b;'
                                    }],
                            selected_rows=[0]
                            ),
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Dropdown(
                            ['Breed Distribution', 'Age Distribution'],
                            id='chart-selector',
                            value='Breed Distribution',
                            style={'color': '#2c3e50'})
                        ], style=
                            {
                                'color': 'white',
                                'backgroundColor': '#2c3e50',
                                'borderRadius': '8px',
                                'size' : '50%',
                            },
                            className='p-3')
                    ),
                    dcc.Graph(
                        id='chart-holder',
                        style={'height' : '500px'}
                    )
                ], xs=12, md=6
            ),
            dbc.Col(
                [html.H5('Selected Animal Location', className='mb-2'),
                 html.Div(id='map-div')
                 ], xs=12, md=6
            )
        ])
    ], fluid=True),

], fluid='true', className='p-4', style={'backgroundColor': '#F2E6E3'})

# callback to update datatable by filtering data based on dropdown selection
@app.callback(
    Output('shelter-table', 'data'),
    Output('shelter-table', 'selected_rows'),
    Input('dropdown-filter', 'value')
)
def update_table(dropdown_filter):
    # create query for each dropdown filter based on given Grazioso Salvare criteria
    if dropdown_filter == 'Water Rescue':
        query = {
            'breed': {'$in': ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']},
            'sex_upon_outcome': 'Intact Female',
            'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}
        }
    elif dropdown_filter == 'Mountain Rescue':
        query = {
            'breed': {'$in': ['German Shepherd', 'Alaskan Malamute',
                              'Old English Sheepdog', 'Siberian Husky', 'Rottweiler']},
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}
        }
    elif dropdown_filter == 'Disaster Rescue':
        query = {
            'breed': {'$in': ['Doberman Pinscher', 'German Shepherd',
                              'Golden Retriever', 'Bloodhound', 'Rottweiler']},
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 20, '$lte': 300}
        }
    # reset option passes in empty query as in first df construct
    else:
        query = {}
    # pass dropdown_filter query into db.read to create new filtered dataframe & drop objectid
    filtered_df = pd.DataFrame.from_records(db.read(query))
    filtered_df.drop(columns=['_id'], inplace=True)
    # return filtered dataframe to data property of DataTable
    return filtered_df.to_dict('records'), [0]

# callback to highlight selected row in data table
@app.callback(
    Output('shelter-table', 'style_data_conditional'),
    Input('shelter-table', 'selected_rows')
)
def highlight_selected_row(selected_rows):
    return [{
        'if' : {'row_index': selected_rows},
        'backgroundColor': '#2c3e50',
        'color': 'white'
    }]

# callback to display breed percentages in pie chart
@app.callback(
    Output('chart-holder', 'figure'),
   [ Input('shelter-table', 'derived_virtual_data'),
     Input('chart-selector', 'value')]
)
def update_pie_chart(viewData, chart_selector):
    if viewData is None:
        return {}

    # define dataframe from shelter-table data
    chart_df = pd.DataFrame.from_records(viewData)
    if chart_df.empty:
        return {}
    if chart_selector == 'Breed Distribution':
        # filter to display top 8 breeds -- otherwise full df pie chart looks like nonsense
        top_breeds = chart_df['breed'].value_counts().head(8).reset_index()
        top_breeds.columns = ['breed', 'count']
        # construct pie chart with plotly express
        fig = px.pie(
            top_breeds,
            names='breed',
            values='count',
            title='Breed Distribution',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        # customize with update_traces method
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Dogs Available: %{value}<br>Percentage: %{percent}<extra></extra>',
            textposition='inside',
            textinfo='percent',
            marker=dict(line=dict(color='white', width=2))
        )
        # match style of page with update_layout method
        fig.update_layout(
            paper_bgcolor='#F2E6E3',
            font={'family' : 'ubuntu'},
            title_font={'size' : 22}
        )
        # return breed distribution pie chart
        return fig

    if chart_selector == 'Age Distribution':
        # convert age in weeks to age in years using float division for precision
        chart_df['age_years'] = chart_df['age_upon_outcome_in_weeks'] / 52
        # define age bins & labels to group dogs by age range
        bins = [0, 0.5, 1, 2, 3, 4, 5, 6, 100]
        labels = ['<6 months', '6-12 months', '1-2 years', '2-3 years', '3-4 years','4-5 years', '5-6 years', '6+ years']
        # categorize each animal into age group by age in years (converts age_years to age_group)
        chart_df['age_group'] = pd.cut(chart_df['age_years'], bins=bins, labels=labels, right=False)
        # count animals in each age group, sort by index instead of count, create age distribution data frame
        age_distribution = chart_df['age_group'].value_counts().sort_index().reset_index()
        # explicitly rename data frame columns
        age_distribution.columns = ['age_group', 'count']

        # define bar chart to display animal counts grouped by age
        fig_bar = px.bar(age_distribution,
                         x='age_group',
                         y='count',
                         title='Age Distribution',
                         labels={'age_group': 'Age Group', 'count': 'Number of Dogs'},
                         color='age_group',
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         )
        # style bars - hover & appearance
        fig_bar.update_traces(
            hovertemplate='<b>%{x}</b><br>Animals: %{y}<extra></extra>',
            marker=dict(line=dict(color='white', width=2))
        )
        # style background color, text
        fig_bar.update_layout(
            paper_bgcolor='#F2E6E3',
            plot_bgcolor='#2c3e50',
            font={'family': 'ubuntu'},
            title_font={'size': 22},
            showlegend=False
        )
        # return age distribution bar chart
        return fig_bar

    else:
        return {}

# callback to populate map
@app.callback(
    Output('map-div', "children"),
    [Input('shelter-table', "derived_virtual_data"),
     Input('shelter-table', "derived_virtual_selected_rows")])
def update_map(viewData, index):
    if viewData is None:
        return None
    elif index is None:
        return None
    dff = pd.DataFrame.from_dict(viewData)
    if index is None:
        row = 0
    else:
        row = index[0]
    return [
        dl.Map(style={'width': '100%', 'height': '500px'},
               center=[dff.iloc[row, 13], dff.iloc[row, 14]], # changed map center from Austin to selected row loc
               zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]], children=[
                # Column 4 defines the breed for the animal
                dl.Tooltip(dff.iloc[row, 4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    # Column 9 defines the name of the animal
                    html.P(dff.iloc[row, 9])
                ])
            ])
        ])
    ]

# callback to export data displayed in data table to csv
# custom button and callback chosen instead of DataTable's built in export_format prop
# to maintain consistent styling and button placement within the card layout
@app.callback(Output('download-dataframe-csv', 'data'),
            Input('export-button', 'n_clicks'),
            State('shelter-table', 'derived_virtual_data'),
              prevent_initial_call=True)
def export_to_csv(n_clicks, viewData):
    dff = pd.DataFrame.from_dict(viewData)
    return dcc.send_data_frame(dff.to_csv,'shelter_data.csv',index=False)


if __name__ == '__main__':
    app.run(debug=True)

