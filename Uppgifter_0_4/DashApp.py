from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import hashlib
import plotly.express as px

# Read the data from the csv file into a pandas DataFrame.
file_path_athletes = '../Data/athlete_events.csv'
data_athletes = pd.read_csv(file_path_athletes)
# Read the data from the csv file into a pandas DataFrame
file_regions = '../Data/noc_regions.csv'
regions = pd.read_csv(file_regions)

# Filtrera ut idrottare från USA
usa_athletes = data_athletes[data_athletes['NOC'] == 'USA'].copy()

# Anonymiseringsfunktion
def anonymize_name(name):
    return hashlib.sha256(name.encode()).hexdigest()

usa_athletes['Name'] = usa_athletes['Name'].apply(anonymize_name)

