from sensor import Sensor
from bluepy.btle import Scanner
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import json
import time
import sys
import config

class Gateway(object):

    def __init__(self):
        self.scanner = Scanner()
        self.sensors = {}
        self.client = self._create_client()

    def _create_client(self):
        # AWS IoTのクライアント作成
        client = AWSIoTMQTTClient(config.DEVICE_NAME)
        # クライアントの初期設定    
        client.configureEndpoint(config.AWS_ENDPOINT, 8883)
        client.configureAutoReconnectBackoffTime(1, 32, 20)
        client.configureOfflinePublishQueueing(-1)
        client.configureDrainingFrequency(2)
        client.configureConnectDisconnectTimeout(300)
        client.configureMQTTOperationTimeout(10)
        client.configureCredentials(config.AWS_ROOTCA,
                                    config.AWS_KEY,
                                    config.AWS_CERT)

        client.connect(60)
        client.publish('gateway/'+config.DEVICE_NAME+'/stat', 'connected.', 1)

        return client

    def loop(self):
        addrs = self._scan()
        for addr in addrs:
                self._connect(addr)

        print('{} devices connected'.format(len(self.sensors)))
        while True:
            payload = self._aggregate()
            self.client.publish(
                topic='gateway/'+config.DEVICE_NAME+'data',
                payload=json.dumps(payload),
                QoS=1
            )
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