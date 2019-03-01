from bluepy.btle import Scanner

scanner = Scanner()
devices = scanner.scan(3)

for d in devices:
    print('Device: {}, RSSI: {}dB'.format(d.addr, d.rssi))

print('{} devices found'.format(len(devices)))