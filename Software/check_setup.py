import Controller
from datetime import datetime

if __name__ == "__main__":            
    ctrl =  Controller.Controller('/dev/ttyS0', 9600)

    for i in range(0,50):
        try:
            data = ctrl.get_humidity()
            print(data)
        except ValueError as e:
            print(e)
