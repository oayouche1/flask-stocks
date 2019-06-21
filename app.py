# Hello, Flask!
from flask import Flask, render_template, request
from bokeh.embed import components 
import pandas as pd
import requests
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

app = Flask(__name__)
 
@app.route("/")
def hello():
    return render_template('index.html')
 
@app.route("/graph")
def graph():
  stock = request.args.get('stock', '')
  index = request.args.get('index', '4')
  apiURL = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?column_index=%s&api_key=aU6JXbtrQEdfcsmhMWnN' % (stock,index)
  print(apiURL)
  r = requests.get(apiURL)
  x = r.json()
  df = pd.DataFrame(x['dataset']['data'])
  df[0] = pd.to_datetime(df[0], format='%Y-%m-%d')
  p = figure(x_axis_type="datetime")
  p.line(df[0], df[1])
  script, div = components(p)
  return render_template('graph.html', script=script, div=div, stock = stock)
#  return "You said: " + request.args.get('stock', '')

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)