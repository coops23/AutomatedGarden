
from flask import Flask, render_template, redirect, url_for, Response, make_response
from graphing import parse_data, parse_line
import psutil
import datetime
import os
import Controller
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
import random
import time
import datetime

app = Flask(__name__)
ctrl = Controller.Controller('/dev/ttyS0', 9600)

def template(title = "Farmatron", text = "", plot = None):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/humidity")
def humidity():
    data = ctrl.get_humidity()
    templateData = template(text = str(data), plot = None)
    return render_template('main.html', **templateData)

@app.route("/data_log")
def data_log():
    msg = ""
    with open('/home/pi/Desktop/AutomatedGarden/Software/data.csv', 'r') as f:
        msg += f.read()
    templateData = template(text = msg)
    return render_template('main.html', **templateData)

@app.route('/plot.png')
def plot():
    fig = plt.figure()

    moisture_plot = fig.add_subplot(1, 1, 1, title = "Moisture vs Time")
    msg = ""
    with open('/home/pi/Desktop/AutomatedGarden/Software/data.csv', 'r') as f:
        msg += f.read()

    x = []
    y = []
    oldest_date = None
    latest_date = None
    for line in msg.splitlines():
        info = line.split(",")
        datetime_object = datetime.datetime.strptime(info[0], '%m/%d/%Y %H:%M:%S')
        if oldest_date is None:
           oldest_date = datetime_object
        latest_date = datetime_object
        y.append(int(info[1]))
        x.append(latest_date)

    # convert to 24 hour so we can plot one day clearly
    today = datetime.date.today()
    time = []
    moisture = []
    for i in range(0, len(x)):
        if x[i].date() == today:
            time.append((x[i].hour * 100) + x[i].minute)
            moisture.append(y[i])
    moisture_plot.set_xlim([0, 2400])
    #moisture_plot.set_xticklabels(moisture_plot.get_xticklabels(), rotation=0)
    moisture_plot.plot(time, moisture)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'

    return response

@app.route("/open_valve")
def open_valve():
   templateData = template(text = str(ctrl.open_valve(2)), plot = None)
   return render_template('main.html', **templateData)

@app.route("/close_valve")
def close_valve():
   templateData = template(text = str(ctrl.close_valve(2)),  plot = None)
   return render_template('main.html', **templateData)

@app.route("/water_plants")
def water_plants():
   ctrl.open_valve(2)
   time.sleep(5)
   ctrl.close_valve(2)

   templateData = template(text = "plants watered",  plot = None)
   return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='192.168.0.163', port=5000, debug=True)
    # app.run()
