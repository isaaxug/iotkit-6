import time
from bluepy.sensortag import SensorTag

class Sensor(object):

    def __init__(self, addr):
        self.addr = addr
        self.tag = SensorTag(addr)
        self.tag.battery.enable()
        self.tag.humidity.enable()
        time.sleep(1.0)

    def state(self):
        """
            stateメソッドはセンサーの状態を文字列で返します。
            "conn" - 接続済み
            "disc" - 接続切れ
            "scan", "tryconn" - 接続中
        """
        return self.tag.getState()

    def read(self):
        temperature, humidity = self.tag.humidity.read()
        battery =  self.tag.battery.read()

        return (temperature, humidity, battery)

    def stop(self):
        self.tag.disconnect()

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--mac', required=True, dest='mac',
                    help='SensorTagのMACアドレス')
    args = ap.parse_args()

    s = Sensor(args.mac)
    print('State: {}'.format(s.state()))
    print(s.read())
    s.stop()