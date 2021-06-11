from disk_controller import DiskController
from led_controller_em_message import EMMessageLEDController
from led_controller import LED_FAIL, LED_LOCATE
from led_controller_sgpio import SGPIOLEDController

from time import sleep
from json import load, dumps

fh = open('config.json', 'r')
config = load(fh)
fh.close()

led_controllers = {}
disk_controllers = {}
mappings = {}
print("LED")
for ctrlc in config['led_controllers']:
    type = ctrlc['type'].lower()
    if type == 'em_message':
        CTor = EMMessageLEDController
    elif type == 'sgpio':
        CTor = SGPIOLEDController
    ctrlo = CTor(ctrlc)
    led_controllers[ctrlo.id] = ctrlo
    print(ctrlo.dev, ctrlo.subdev, ctrlo.dev_value, ctrlo.subdev_value)

print("DISK")
for ctrlc in config['disk_controllers']:
    ctrlo = DiskController(ctrlc)
    disk_controllers[ctrlo.id] = ctrlo
    print(ctrlo.dev, ctrlo.subdev, ctrlo.dev_value, ctrlo.subdev_value)

for x in ['a','b','c','d','e','f','g','h']:
    for _, ctrl in disk_controllers.items():
        print(ctrl, x,  ctrl.get_index('/dev/sd%s' % x))
