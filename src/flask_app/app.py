from sqlite3 import connect
from flask import Flask, request, render_template
import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json


# Join the 2 other source tables to the schools table
# Join table satscores on CDSCode
# Join table frpm on County, District, and School name
query = """SELECT schools.*, satscores.NumTstTakr, satscores.AvgScrMath, satscores.AvgScrRead, satscores.AvgScrWrite , frpm."Percent (%) Eligible Free (K-12)" AS FreeLunchPrcnt, frpm."Percent (%) Eligible FRPM (K-12)" AS ReduLunchPrcnt
        FROM schools 
        LEFT JOIN satscores ON satscores.cds=schools.CDSCode
        LEFT JOIN frpm ON frpm."County Name"=schools.County AND frpm."District Name"=schools.District AND frpm."School Name"=schools.School
        WHERE satscores.NumTstTakr IS NOT NULL AND schools.LastUpdate >= '2010-01-01'"""
# Connect to the sqlite db
conn = connect('data/cdeschools.sqlite')
# Read the result of the above query into a dataframe using the above connection
df = pd.read_sql(query, conn)
# Close the sql connection as it is not used anymore
conn.close()


# Convert ReduLunchPrcnt from 0-1 to 0-100
df['ReduLunchPrcnt'] = df['ReduLunchPrcnt'] * 100
# Sum the average scores to the the combined average score
df['CombinedAvgScr'] = df['AvgScrMath'] + df['AvgScrRead'] + df['AvgScrWrite']


# Creates a line graph showing the combined average score on the x axis and the reduced lunch percentage on the y axis.
# 100 random points are grabbed to minimize the amount of data points shown in the graph. The 100 points are then sorted by combined average score ascending
# Specifies the x range to 900-2100 to prevent empty areas on the left and right sides of the graph. Height is set to 1000 to make it easier to view
# Markers is set to true to show markers that highlight the individual data points
fig = px.line(df.sample(100).sort_values(by='CombinedAvgScr', ascending=True), x='CombinedAvgScr', y='ReduLunchPrcnt', markers=True, range_x=[900, 2100], height=1000, title='Reduced Lunch Percent by SAT Score')
# Connects the gaps so the graph does not jump
fig.update_traces(connectgaps=True)
# Gets the json of the graph to later render on the webpage
graph_json_line = json.dumps(fig, cls=PlotlyJSONEncoder)


# Creates a scatter plot showing the combined average score on the x axis and the reduced lunch percentage on the y axis.
# Height is set to 1000 to make it easier to see and the range for the y axis is set to 0-100 to prevent empty areas in the chart at the top and bottom.
fig = px.scatter(df, x='CombinedAvgScr', y='ReduLunchPrcnt', color='County', height=1000, range_y=[0, 100])
# Gets the json of the plot to later render on the webpage
graph_json_scatter = json.dumps(fig, cls=PlotlyJSONEncoder)


# Creates the Flask app and specified the folder for the webpage templates
app = Flask(__name__, template_folder='templates')

# Routes the index page. Will return for all HTTP methods
@app.route('/', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def index():
        return f"Hello, {request.remote_addr}!<br><a href='/data'>Click here to go to the data page</a> or visit {request.url_root}data"

# Routes the data page. Returns the data.html template with the graphs made above
@app.route('/data/', methods = ['GET'])
def data():
        return render_template('data.html', graph_json_line=graph_json_line, graph_json_scatter=graph_json_scatter, header='SAT Scores by Free/Reduced Lunch', description="""A scatter plot showing the average SAT scores for each section from each school over the percantage of the school's students that have reduced or free lunch in the CDE dataset.""")
