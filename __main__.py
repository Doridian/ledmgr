from disk_controller import DiskController
from led_controller_em_message import EMMessageLEDController
from led_controller import LED_FAIL, LED_LOCATE
from led_controller_sgpio import SGPIOLEDController

from time import sleep
from json import load

fh = open('config.json', 'r')
config = load(fh)
fh.close()

led_controllers = {}
disk_controllers = {}
mappings = {}
for ctrl in config['led_controllers']:
    type = ctrl['type'].lower()
    if type == 'em_message':
        CTor = EMMessageLEDController
    elif type == 'sgpio':
        CTor = SGPIOLEDController
    ctrlo = CTor(config)
    led_controllers[ctrlo.id] = ctrlo

for ctrl in config['disk_controllers']:
    ctrlo = DiskController(config)
    disk_controllers[ctrlo.id] = ctrlo

print(led_controllers)
print(disk_controllers)

"""
ctrl = EMMessageLEDController('/sys/devices/pci0000:00/0000:00:11.0/0000:05:00.0/host7/bsg/sas_host7', 4)
for i in range(0,4):
    print('Setting LED %d' % i)
    ctrl.write(i, LED_LOCATE)
    sleep(1)
    ctrl.write(i, LED_FAIL)
    sleep(1)
ctrl.clear()

ctrl = SGPIOLEDController('/sys/devices/pci0000:00/0000:00:1f.2', 6)
for i in range(0,4):
    print('Setting LED2 %d' % i)
    ctrl.write(i, LED_LOCATE)
    sleep(1)
    ctrl.write(i, LED_FAIL)
    sleep(1)
ctrl.clear()
"""
