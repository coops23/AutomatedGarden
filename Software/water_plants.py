import Controller
import datetime
import time

SAMPLE_COUNT = 50
WATERING_TIME_SECS = 30


if __name__ == "__main__":            
    ctrl =  Controller.Controller('/dev/ttyS0', 9600)

    moisture = 0
    for i in range(0, SAMPLE_COUNT):
        data = ctrl.get_humidity()
        moisture += data
    moisture = int(moisture / SAMPLE_COUNT)

    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    watered = "False"
    if moisture >= 700:
        ctrl.open_valve(2)
        time.sleep(WATERING_TIME_SECS)
        ctrl.close_valve(2)
        watered = "True"

    f = open("/home/pi/Desktop/AutomatedGarden/Software/data.csv", "a")
    f.write(date_time + "," + str(moisture) + "," + watered + "\n")
    f.close()

