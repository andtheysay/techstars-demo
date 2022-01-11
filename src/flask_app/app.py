from sqlite3 import connect
from flask import Flask, request, render_template
import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

import json

query = """SELECT schools.*, satscores.NumTstTakr, satscores.AvgScrMath, satscores.AvgScrRead, satscores.AvgScrWrite , frpm."Percent (%) Eligible Free (K-12)" AS FreeLunchPrcnt, frpm."Percent (%) Eligible FRPM (K-12)" AS ReduLunchPrcnt
        FROM schools 
        LEFT JOIN satscores ON satscores.cds=schools.CDSCode
        LEFT JOIN frpm ON frpm."County Name"=schools.County AND frpm."District Name"=schools.District AND frpm."School Name"=schools.School
        WHERE satscores.NumTstTakr IS NOT NULL AND schools.LastUpdate >= '2010-01-01'"""
conn = connect('data/cdeschools.sqlite')
df = pd.read_sql(query, conn)
conn.close()
# Use pandas to rearrange the dataframe to make the data show in a scatter plot better
df['ReduLunchPrcnt'] = df['ReduLunchPrcnt'] * 100
print(df['ReduLunchPrcnt'].max())
print(df.head())
df['CombinedAvgScr'] = df['AvgScrMath'] + df['AvgScrRead'] + df['AvgScrWrite']
fig = px.line(df.sample(100).sort_values(by='CombinedAvgScr'), y='ReduLunchPrcnt', x='CombinedAvgScr', range_x=[900, 2100], height=1000, title='Reduced Lunch Percent by SAT Score', markers=True)
fig.update_traces(connectgaps=True)
graph_json_line = json.dumps(fig, cls=PlotlyJSONEncoder)
fig = px.scatter(df, x='CombinedAvgScr', y='ReduLunchPrcnt', color='County', height=1000, range_y=[0, 100])
graph_json_scatter = json.dumps(fig, cls=PlotlyJSONEncoder)
app = Flask(__name__, template_folder='templates')

@app.route('/', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def index():
    return f"Hello, {request.remote_addr}!<br><a href='/data'>Click here to go to the data page</a> or visit {request.url_root}data"

@app.route('/data/', methods = ['GET'])
def data():
        return render_template('data.html', graph_json_line=graph_json_line, graph_json_scatter=graph_json_scatter, header='SAT Scores by Free/Reduced Lunch', description="""A scatter plot showing the average SAT scores for each section from each school over the percantage of the school's students that have reduced or free lunch in the CDE dataset.""")
