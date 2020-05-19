import Controller
import datetime

if __name__ == "__main__":            
    ctrl =  Controller.Controller('/dev/ttyS0', 9600)

    avg = 0
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    for i in range(0,10):
        try:
            data = ctrl.get_humidity()
            avg += data
        except ValueError as e:
            print(e)
    avg = int(avg / 10)

    f = open("/home/pi/Desktop/AutomatedGarden/Software/data.csv", "a")
    f.write(date_time + "," + str(avg) + "\n")
    f.close()
