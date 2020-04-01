from flask import Flask, render_template, redirect, url_for, Response
from graphing import parse_data
import psutil
import datetime
import os
import Controller
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random

app = Flask(__name__)
ctrl = Controller.Controller('/dev/ttyS0', 9600)

def template(title = "Farmatron", text = "", plot = None):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text,
        'plot' : plot
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/humidity")
def humidity():
    data = ctrl.get_humidity()
    data = data.decode('ascii')
    data = data.strip('\n')
    data = data.split(' ')
    
    msg = ""
    for i in range(0, len(data)):
        datum = str(int(data[i]))
        msg += datum + ' '

    templateData = template(text = msg, plot = None)
    return render_template('main.html', **templateData)

@app.route("/data_log")
def data_log():
    msg = ""
    with open('/home/pi/Desktop/AutomatedGarden/Software/data.csv', 'r') as f:
        msg += f.read(data)
    response = plot_png()
    templateData = template(text = msg, plot = response)
    return render_template('main.html', **templateData)

def plot_png(data):
    fig = create_figure(data)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    
def create_figure(data):
    fig = Figure()
    [x, y] = parse_data(data)
    axis.plot(x, y)
    return fig
    
@app.route("/motor_status")
def motor_status():
   msg = ""
   data = ctrl.get_motor_states()
   data = data.decode('ascii')
   data = data.strip('\n')
   msg = data

   templateData = template(text = msg)
   return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='192.168.0.173', port=5000, debug=True)
    # app.run()
