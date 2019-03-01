import time
from bluepy.sensortag import SensorTag

tag = SensorTag('98:07:2d:26:a4:81')
tag.humidity.enable()
time.sleep(1)

print(tag.humidity.read())
tag.disconnect()
del tag