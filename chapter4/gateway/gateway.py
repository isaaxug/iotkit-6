from sensor import Sensor
from bluepy.btle import Scanner
from datetime import datetime

import time
import sys

class Gateway(object):

    def __init__(self):
        self.scanner = Scanner()
        self.sensors = {}

    def loop(self):
        addrs = self._scan()
        for addr in addrs:
            self._connect(addr)

        print('{} devices connected'.format(len(self.sensors)))
        while True:
            print(self._aggregate())
            time.sleep(10)

    def _scan(self):
        addrs = []
        devices = self.scanner.scan(5)
        for d in devices:
          for (adtype, desc, value) in d.getScanData():
              if adtype == 9 and value == 'CC2650 SensorTag':
                  print('Sensor found: {}, RSSI: {}dB'.format(d.addr, d.rssi))
                  addrs.append(d.addr)

        return addrs

    def _connect(self, addr):
        if addr in self.sensors:
            return

        sensor = Sensor(addr)
        self.sensors[addr] = sensor

    def _aggregate(self):
        sensor_data = []
        for addr, sensor in self.sensors.items():
            t, h, b = sensor.read()
            sensor_data.append({
              'mac': addr,
              'temperature': t,
              'humidity': h,
              'battery': b
            })

        return {
            'sensors': sensor_data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


if __name__ == '__main__':
    g = Gateway()
    print('Press Ctrl+C to exit.')
    try:
        g.loop()
    except KeyboardInterrupt:
        sys.exit(0)