from disk_controller import DiskController
from led_controller_em_message import EMMessageLEDController
from led_controller_sgpio import SGPIOLEDController
from json import load
from os import lstat, readlink
from os.path import abspath, join, dirname
from stat import S_ISLNK

fh = open('config.json', 'r')
config = load(fh)
fh.close()

led_controllers = {}
disk_controllers = {}
mappings = {}

for ctrlc in config['led_controllers']:
    type = ctrlc['type'].lower()
    if type == 'em_message':
        CTor = EMMessageLEDController
    elif type == 'sgpio':
        CTor = SGPIOLEDController
    ctrlo = CTor(ctrlc)
    led_controllers[ctrlo.id] = ctrlo

for ctrlc in config['disk_controllers']:
    ctrlo = DiskController(ctrlc)
    disk_controllers[ctrlo.id] = ctrlo

def resolve_disk(disk):
        while True:
            disk = abspath(disk)
            statres = lstat(disk)
            if not S_ISLNK(statres.st_mode):
                break
            disk = join(dirname(disk), readlink(disk))

        disk = abspath(disk)
        return disk

for x in ['a','b','c','d','e','f','g']:
    for _, ctrl in disk_controllers.items():
        dev = resolve_disk('/sys/block/sd%s' % x)
        idx = ctrl.get_index(dev)
        if idx >= 0:
            print(ctrl, dev, x, idx)
