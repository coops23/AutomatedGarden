import Controller
from datetime import datetime

if __name__ == "__main__":            
    ctrl =  Controller.Controller('/dev/ttyS0', 9600)
    f = open("data.csv", "a")

    data = ctrl.get_humidity()
    data = data.decode('ascii')
    data = data.strip('\n')
    data = data.split(' ')
    msg = ""
    for i in range(0, len(data)):
        datum = str(int(data[i]))
        msg += datum + ','

    msg += datetime.now().strftime("%m/%d/%Y,%H:%M:%S") 
    msg += "\n"
    print(msg)
    f.write(msg)
    f.close()

