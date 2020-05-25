import Controller
import datetime
import time
import statistics

SAMPLE_COUNT = 10
WATERING_TIME_SECS = 20
MOISTURE_THRESHOLD = 750

if __name__ == "__main__":            
    ctrl =  Controller.Controller('/dev/ttyS0', 9600)

    moisture = 0
    data = []
    for i in range(0, SAMPLE_COUNT):
        data.append(ctrl.get_humidity())
    moisture = int(statistics.median(data))
    print(data)
    print(moisture)

    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    watered = "False"
    if moisture >= MOISTURE_THRESHOLD:
        ctrl.open_valve(2)
        time.sleep(WATERING_TIME_SECS)
        ctrl.close_valve(2)
        watered = "True"

    f = open("/home/pi/Desktop/AutomatedGarden/Software/data.csv", "a")
    f.write(date_time + "," + str(moisture) + "," + watered + "\n")
    f.close()

