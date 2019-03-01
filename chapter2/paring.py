from bluepy.btle import Scanner, Peripheral
import signal

scanner = Scanner()
devices = scanner.scan(3)
addr = None

for d in devices:
    for (adtype, desc, value) in d.getScanData():
        if adtype == 9 and value == 'CC2650 SensorTag':
            print('SensorTag: {}, RSSI: {}dB'.format(d.addr, d.rssi))
            addr = d.addr

if addr != None:
    # 接続開始
    tag = Peripheral(addr)
    # 接続状態の確認 状態が`conn`なら接続できている
    print('State: {}'.format(tag.getState()))
    print('Press Ctrl+C to exit.')
    signal.pause()

print('SensorTag not found.')