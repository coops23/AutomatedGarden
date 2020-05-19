import Controller
from datetime import datetime

SAMPLE_COUNT = 50
WATERING_TIME_SECS = 10

if __name__ == "__main__":            
    ctrl =  Controller.Controller('/dev/ttyS0', 9600)

    moisture = 0
    for i in range(0, SAMPLE_COUNT):
        data = ctrl.get_humidity()
        moisture += data
    moisture = int(avg / SAMPLE_COUNT)

    if moisture >= 700:
        ctrl.open_valve(2)
        time.sleep(WATERING_TIME_SECS)
        ctrl.close_valve(2)
