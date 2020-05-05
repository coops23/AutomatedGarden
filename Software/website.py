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
        msg += f.read()
    templateData = template(text = msg)
    return render_template('main.html', **templateData)

@app.route('/plot.png')
def plot():
    fig = plt.figure()

    section_one_plot = fig.add_subplot(2, 2, 1, title = "Section 1 Moisture")
    section_two_plot = fig.add_subplot(2, 2, 2, title = "Section 2 Moisture")
    section_three_plot = fig.add_subplot(2, 2, 3, title = "Section 3 Moisture")
    section_four_plot = fig.add_subplot(2, 2, 4, title = "Section 4 Moisture")

    msg = ""
    with open('/home/pi/Desktop/AutomatedGarden/Software/data.csv', 'r') as f:
        msg += f.read()

    x = []
    y0 = []
    y1 = []
    y2 = []
    y3 = []
    oldest_date = None
    latest_date = None
    for line in msg.splitlines():
        info = parse_line(line)
        if oldest_date is None:
           oldest_date = info[4]
        latest_date = info[4]
        y0.append(int(info[0]))
        y1.append(int(info[1]))
        y2.append(int(info[2]))
        y3.append(int(info[3]))
        x.append(latest_date)

    # hack to plot for one day
    oldest_date = latest_date.replace(hour = 0, minute = 0, second = 0)
    latest_date = latest_date.replace(hour = 23, minute = 59, second = 59)


    #section_one_plot.set_xlim([oldest_date, latest_date])
    section_one_plot.set_ylim([550, 900])
    section_one_plot.set_xticklabels(section_one_plot.get_xticklabels(), rotation=90)
    section_one_plot.plot(x[:], y0)

    #section_two_plot.set_xlim([oldest_date, latest_date])
    section_two_plot.set_ylim([550, 900])
    section_two_plot.set_xticklabels(section_two_plot.get_xticklabels(), rotation=90)
    section_two_plot.plot(x[:], y1)

    #section_three_plot.set_xlim([oldest_date, latest_date])
    section_three_plot.set_ylim([550, 900])
    section_three_plot.set_xticklabels(section_three_plot.get_xticklabels(), rotation=90)
    section_three_plot.plot(x[:], y2)

    #section_four_plot.set_xlim([oldest_date, latest_date])
    section_four_plot.set_ylim([550, 900])
    section_four_plot.set_xticklabels(section_four_plot.get_xticklabels(), rotation=90)
    section_four_plot.plot(x[:], y3)

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

if __name__ == "__main__":
    app.run(host='192.168.0.173', port=5000, debug=True)
    # app.run()
