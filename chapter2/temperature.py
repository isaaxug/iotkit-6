from bluepy.btle import Scanner, Peripheral
import signal
import struct
import time

scanner = Scanner()
devices = scanner.scan(3)
addr = None

for d in devices:
    for (adtype, desc, value) in d.getScanData():
        if adtype == 9 and value == 'CC2650 SensorTag':
            print('SensorTag: {}, RSSI: {}dB'.format(d.addr, d.rssi))
            addr = d.addr

# 接続開始
tag = Peripheral(addr)
# IR Temperatureサービスを取得
service = tag.getServiceByUUID('F000AA20-0451-4000-B000-000000000000')
# Dataキャラクタリスティックの取得
data = service.getCharacteristics('F000AA21-0451-4000-B000-000000000000')[0]
# Configurationキャラクタリスティックの取得
conf = service.getCharacteristics('F000AA22-0451-4000-B000-000000000000')[0]
# 温度センサーの有効化
conf.write(b'\x01', withResponse=True)
time.sleep(1)


raw_data = data.read()
raw_temp, raw_humid = struct.unpack('<HH', raw_data)
temp = -40.0 + 165.0 * (raw_temp / 65536.0)

print(temp)