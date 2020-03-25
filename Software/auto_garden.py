import serial, time
from datetime import datetime
from pathlib import Path

class Controller:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate)
        
    def __del__(self):
        self.ser.close()
        
    def _read(self):
        return self.ser.readline()

    def _write(self, msg):
        msg += "\n"
        self.ser.write(msg.encode())
        
    def get_humidity(self):
        self._write("1")
        return self._read()
    
    def get_motor_states(self):
        self._write("2")
        return self._read()
        
    def toggle_motor(self, index):
        if (index >= 0 and index <= 3):
            if index == 0:
                self._write("3")
            elif index == 1:
                self._write("4")
            elif index == 2:
                self._write("5")
            elif index == 3:
                self._write("6")
            return self._read()
        else:
            return "Error. Invalid motor index."

    def stop_motors(self):
        self._write("7")
        return self._read()

ctrl =  Controller('/dev/ttyS0', 9600)
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
