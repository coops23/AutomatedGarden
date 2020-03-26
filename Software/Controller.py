import serial

class Controller:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        
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
        if (index >= 0 and index < 4):
            cmd = str(index + 3)
            self._write(cmd)
            return self._read()
        else:
            return "Error. Invalid motor index."