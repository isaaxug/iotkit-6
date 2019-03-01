from bluepy.btle import Scanner

scanner = Scanner()
devices = scanner.scan(3)

for d in devices:
    for (adtype, desc, value) in d.getScanData():
        if adtype == 9 and value == 'CC2650 SensorTag':
            print('SensorTag: {}, RSSI: {}dB'.format(d.addr, d.rssi))
