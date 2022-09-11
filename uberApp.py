import pandas as pd
import numpy as np
from IPython import display
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import dash_daq as daq
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly import tools
import chart_studio.plotly as py
import plotly.figure_factory as ff


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app_plot = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)

