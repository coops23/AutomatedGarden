import Controller
import datetime
import math
import statistics

SAMPLE_COUNT = 10

if __name__ == "__main__":            
    ctrl =  Controller.Controller('/dev/ttyS0', 9600)

    median = 0
    samples = []
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    for i in range(0, SAMPLE_COUNT):
        samples.append(ctrl.get_humidity())
    median = int(statistics.median(samples))
    print(samples)
    print(median)
    f = open("/home/pi/Desktop/AutomatedGarden/Software/data.csv", "a")
    f.write(date_time + "," + str(median) + "," + "False" + "\n")
    f.close()
