import serial, time

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

    def open_valve(self, delay):
        msg = ""
        self._write("2")
        msg += str(self._read())
        self._write("4")
        msg += str(self._read())
        time.sleep(delay)

        self._write("5")
        msg += str(self._read())

        return "Valve opened"

    def close_valve(self, delay):
        msg = ""
        self._write("3")
        msg += str(self._read())
        self._write("4")
        msg += str(self._read())
        time.sleep(delay)

        self._write("5")
        msg += str(self._read())

        return "Valve closed"

if __name__ == "__main__":
    ctrl = Controller("/dev/ttyS0", 9600)
    print(ctrl.get_humidity())
    print(ctrl.open_valve(3))
    print(ctrl.close_valve(3))
