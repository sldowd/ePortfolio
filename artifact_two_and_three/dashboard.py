"""
Grazioso Salvare Dashboard
Interactive web application for scoring and visualizing rescue dog candidates
from Austin Animal Center shelter data.
"""

from dash import Dash, html, Input, Output, dcc, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_leaflet as dl
import base64
from pathlib import Path
import os

# import controller
from animal_shelter import AnimalShelter
# import scoring algorithm, rescue profiles dict, and minimum score constant
from scoring_algorithm import score_animal_for_profile, rescue_profiles, MIN_SCORE


# dashboard only reads data, so open a read-only connection (writes are blocked in the app)
db = AnimalShelter(read_only=True)
df = pd.DataFrame.from_records(db.read({}))
df.drop(columns=['_id'], inplace=True)
# define new column for to hold fit score produced by scoring algorithm
# column must exist at startup before table is built
df['fit_score'] = None

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

# encode logo to base64 string
# build the logo path from this file's location, not the current folder
LOGO_PATH = Path(__file__).resolve().parent / 'Grazioso Salvare Logo.png'
with open(LOGO_PATH, 'rb') as f:
    encoded_img = base64.b64encode(f.read())

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
    # populate df with all records for scoring, drop id column
    filtered_df = pd.DataFrame.from_records(db.read({}))
    filtered_df.drop(columns=['_id'], inplace=True)
    # rescue type dropdown filter passed to lambda function 
    # and populates each row with a fit score value
    if dropdown_filter in rescue_profiles: # conditional here allows for unscored data display at load and via 'reset' selection from dropdown
        filtered_df['fit_score'] = filtered_df.apply(
            lambda row: score_animal_for_profile(row, dropdown_filter), axis=1
        )
        # filter data frame to remove rows where fit score < MIN_SCORE constant
        filtered_df = filtered_df[filtered_df['fit_score'] >= MIN_SCORE]
        # sort data frame by descending fit score
        filtered_df = filtered_df.sort_values('fit_score', ascending=False)
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

# callback to display breed percentages in pie chart or age distribution in bar chart
@app.callback(
    Output('chart-holder', 'figure'),
   [ Input('shelter-table', 'derived_virtual_data'),
     Input('chart-selector', 'value')]
)
def update_chart(viewData, chart_selector):
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
    if not viewData or not index:
        return None

    dff = pd.DataFrame.from_dict(viewData)
    row = index[0]

    selected = dff.iloc[row]
    lat = selected['location_lat']
    lon = selected['location_long']
    breed = selected['breed']
    name = selected['name']

    return [
        dl.Map(style={'width': '100%', 'height': '500px'},
               center=[lat,lon], # map center uses location coordinates from selected row
               zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the latitude and longitude coordinates for the map
            dl.Marker(position=[lat,lon], children=[
                # Column 4 defines the breed for the animal
                dl.Tooltip(breed),
                dl.Popup([
                    html.H1("Animal Name"),
                    # Column 9 defines the name of the animal
                    html.P(name)
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
    # debug mode is off by default; turn it on with: DASH_DEBUG=1 python3 dashboard.py
    app.run(debug=os.getenv("DASH_DEBUG") == "1")
