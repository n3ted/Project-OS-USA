from dash import Dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import pandas as pd
import hashlib
import plotly.express as px


# Read the data from the csv file into a pandas DataFrame.
file_path_athletes = '../Data/athlete_events.csv'
data_athletes = pd.read_csv(file_path_athletes)
# Read the data from the csv file into a pandas DataFrame
file_regions = '../Data/noc_regions.csv'
regions = pd.read_csv(file_regions)
### Data from uppgift 1
# Filtrera ut idrottare från USA
usa_athletes = data_athletes[data_athletes['NOC'] == 'USA'].copy()

# Anonymiseringsfunktion
def anonymize_name(name):
    return hashlib.sha256(name.encode()).hexdigest()

usa_athletes['Name'] = usa_athletes['Name'].apply(anonymize_name)
# Uppgift 1.1: Undersök därefter hur det gått för landet i OS genom tiderna

# Visusalisera de sporter landet fått flest medaljer i

# Räkna medaljer per sport
medal_counts = usa_athletes[usa_athletes['Medal'].notnull()]['Sport'].value_counts()

# Skapa interaktivt stapeldiagram
medal_count_fig = px.bar(medal_counts.head(10), orientation='h', 
labels={'value':'Antal Medaljer', 'index':'Sport'},
title='Topp 10 Sporter för USA efter Antal Medaljer')
medal_count_fig.show()
# Visualisera Antal Medaljer per Olympiskt Spel

# Räkna medaljer per år
medals_per_olympics = usa_athletes[usa_athletes['Medal'].notnull()].groupby(['Year', 'Medal']).size().unstack().fillna(0)

# Skapa interaktivt stapeldiagram
medals_per_olympics_fig = px.bar(medals_per_olympics, barmode='stack',
labels={'value':'Antal Medaljer', 'Year':'År'},
 title='Antal Medaljer per Olympiskt Spel för USA')
medals_per_olympics_fig.show()
# Skapa Histogram över Åldrar på Idrottare

# Skapa interaktivt histogram 
age_histogram_fig = px.histogram(usa_athletes, x='Age', nbins=30,
    labels={'Age':'Ålder'},
    title='Histogram över Åldrar på Amerikanska Idrottare i OS')
age_histogram_fig.show()

### Data from uppgift 2
choosen_sports = ['Athletics', 'Swimming', 'Gymnastics']
sport_data = data_athletes[data_athletes['Sport'].isin(choosen_sports)]
sport_data = data_athletes[data_athletes['Sport'].isin(choosen_sports)]

def visualize_medal_distribution(sport, data):
    # Filter data for the selected sport and valid medals
    sport_medals = data[(data['Sport'] == sport) & data['Medal'].notnull()]

    # Group by Medal and NOC, then count the number of medals
    medal_counts = sport_medals.groupby(['Medal', 'NOC']).size().reset_index(name='Counts')
    # Define a custom color scale
    medal_color_scale = {'Gold': 'gold', 'Silver': 'silver', 'Bronze': '#cd7f32'}
    # Create a sunburst chart
    medal_count_fig = px.sunburst(
        medal_counts, 
        path=['Medal', 'NOC'],  # Hierarchical levels: Medal type, then NOC
        values='Counts',        # Size of each segment
        color='Medal',            # Color by NOC
        color_discrete_map=medal_color_scale,
        title=f"Medal Distribution in {sport}"
    )
    return medal_count_fig
# Function for age distribution
def visualize_age_distribution(sport, data):
    sport_ages = data[data['Sport'] == sport]['Age'].dropna().sort_values()
    max_age = sport_ages.max()
    min_age = sport_ages.min()

    # Create a custom color map for ages
    unique_ages = sport_ages.unique()
    color_scale = px.colors.sequential.Plasma
    age_colors = {age: color_scale[int((age - min_age) / (max_age - min_age) * (len(color_scale) - 1))] for age in unique_ages}

    # Represent each age with a unique color and bin
    age_histogram_fig = px.histogram(
        sport_ages, x='Age',
        nbins=int(max_age - min_age + 1),  # Set bins for each age
        color='Age',
        color_discrete_map=age_colors,
        labels={'value':'Number of Athletes', 'Age':'Age'},
        title=f'Age Distribution in {sport}'
    )

    return age_histogram_fig

# Create and display graphs for 'Athletics'
medal_distribution_fig = visualize_medal_distribution('Athletics', sport_data)
age_distribution_fig = visualize_age_distribution('Athletics', sport_data)
medal_distribution_fig.show()
age_distribution_fig.show()

# Create and display graphs for 'Swimming'
medal_distribution_fig = visualize_medal_distribution('Swimming', sport_data)
age_distribution_fig = visualize_age_distribution('Swimming', sport_data)
medal_distribution_fig.show()
age_distribution_fig.show()

# Create and display graphs for 'Gymnastics'
medal_distribution_fig = visualize_medal_distribution('Gymnastics', sport_data)
age_distribution_fig = visualize_age_distribution('Gymnastics', sport_data)
medal_distribution_fig.show()
age_distribution_fig.show()
def visualize_medal_distribution_years(sport, data):
    # Filter data for the selected sport and only rows with medals won
    sport_medals = data[(data['Sport'] == sport) & data['Medal'].notnull()]
    
    # Group by Medal, NOC, and Year, then count the number of medals
    medal_counts = sport_medals.groupby(['Medal', 'NOC', 'Year']).size().reset_index(name='Counts')

    # Create a scatter plot using medal_counts DataFrame
    medal_timeline_fig = px.scatter(
        medal_counts, x='Year', y='Medal', color='Medal',
        size='Counts',  # Size of markers based on the count of medals
        title=f'Medal Timeline in {sport}',
        width=800, height=400,
        hover_data=['NOC', 'Counts'],  # Additional data to show on hover
    )
    medal_timeline_fig.update_layout(
        xaxis_title="Olympic Year",
        yaxis_title="Medal Type",
        legend_title="Medal"
    )
    return medal_timeline_fig

# Create and display graphs for 'Gymnastics'
medal_distribution_years_fig = visualize_medal_distribution_years('Gymnastics', sport_data)
medal_distribution_years_fig.show()

# Create and display graphs for 'Swimming'
medal_distribution_years_fig = visualize_medal_distribution_years('Swimming', sport_data)
medal_distribution_years_fig.show()

# Create and display graphs for 'Athletics'
medal_distribution_years_fig = visualize_medal_distribution_years('Athletics', sport_data)
medal_distribution_years_fig.show()
#gruppera data efter sport och kön samt räkna antalet medaljer
grouped_data = data_athletes.groupby(['Sport', 'Sex']).size().unstack().reset_index()


melted_data = pd.melt(grouped_data, id_vars='Sport', var_name='Gender', value_name='Count')

#Skapa ett stapel diagrram
fig = px.bar(melted_data, x='Sport', y='Count', color='Gender',
             labels={'Count': 'Amount medalwinners', 'Sport': 'Sport'},
             title='Gender differences in medal distribution for each sport',
             barmode='stack')

fig.show()
# Create a Dash app and layout
app = Dash(__name__)
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200&display=swap" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {%metas%}
        <title>Your App Title</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
app.layout = html.Div([
    
    html.H1('Olympic Data Visualization', style={'textAlign': 'center', 'font-size': 70}),
    dcc.Dropdown(
        id='sport-dropdown',
        options=[
            {'label': 'Athletics', 'value': 'Athletics'},
            {'label': 'Swimming', 'value': 'Swimming'},
            {'label': 'Gymnastics', 'value': 'Gymnastics'}, 
        ],
        value='Athletics', style={'padding-left': 40, 'font-family': "'Inter', sans-serif",'width': '50%'}
    ),
    # Row 1 with two graphs
    html.Div([
        dcc.Graph(id='medal-distribution-plot', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='age-distribution-plot', style={'width': '50%', 'display': 'inline-block'}),
    ], style={'display': 'flex'}),
   html.Div([
        dcc.Graph(id='medal-timeline-plot', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='another-plot', style={'width': '50%', 'display': 'inline-block'}),
    ], style={'display': 'flex'}),    
    
    html.H3('Visualizations for Gender, Age and Medal Distribution', style={'textAlign': 'center', 'font-family': "'Inter', sans-serif", 'font-size': 30}),
    dcc.Dropdown(
        id='Visualization-dropdown',
    options=[
         {'label': 'Gender differences', 'value': 'Gender'},
        {'label': 'Age distribution', 'value': 'Age'},
         {'label': 'Medal distribution', 'value': 'Medal'}
        ],
        value='Gender', style={'padding-left': 40,'font-family': "'Inter', sans-serif",'width': '50%'}
    ),
    dcc.Graph(id='Graph-plot', style={'font-family': "'Inter', sans-serif",'width': '100%', 'display': 'inline-block'}),
])

# Callback for Gender differences
@app.callback(
    Output('Graph-plot', 'figure'),
    Input('Visualization-dropdown', 'value')
)
def uppdate_fig(Visualization_dropdown):

    if Visualization_dropdown == 'Gender':
        return fig
    elif Visualization_dropdown == 'Age':
        return age_histogram_fig
    elif Visualization_dropdown == 'Medal':
        return medal_count_fig
    else:
        return {}

# Callback for medal distribution
@app.callback(
    Output('medal-distribution-plot', 'figure'),
    Input('sport-dropdown', 'value')
)
def update_medal_distribution(sport):
    return visualize_medal_distribution(sport, sport_data)

# Callback for age distribution
@app.callback(
    Output('age-distribution-plot', 'figure'),
    Input('sport-dropdown', 'value')
)
def update_age_distribution(sport):
    return visualize_age_distribution(sport, sport_data)

# Callback for medal timeline
@app.callback(
    Output('medal-timeline-plot', 'figure'),
    Input('sport-dropdown', 'value')
)
def update_medal_timeline(sport):
    return visualize_medal_distribution_years(sport, sport_data)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    
