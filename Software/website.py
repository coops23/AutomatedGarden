from flask import Flask, render_template, redirect, url_for
from graphing import parse_data
import psutil
import datetime
import os
import Controller
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
ctrl = Controller.Controller('/dev/ttyS0', 9600)

def template(title = "Farmatron", text = ""):
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

    templateData = template(text = msg)
    return render_template('main.html', **templateData)

@app.route("/data_log")
def data_log():
    msg = ""
    with open('/home/pi/Desktop/AutomatedGarden/Software/data.csv', 'r') as f:
        msg += f.read()
    templateData = template(text = msg)
    return render_template('main.html', **templateData)

@app.route("/plot.png")
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
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
