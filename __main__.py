from subprocess import call
from led_controller import LED_FAIL, LED_LOCATE, LED_OFF, LED_REBUILD
from time import sleep
from disk_controller import DiskController
from led_controller_em_message import EMMessageLEDController
from led_controller_sgpio import SGPIOLEDController
from json import load
from os import lstat, readlink
from os.path import abspath, join, dirname
from stat import S_ISLNK
from sys import argv

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

for map in config['mappings']:
    to = map['to'].split(':')
    mappings[map['from']] = (led_controllers[to[0]], int(to[1]))

def resolve_disk(disk):
        while True:
            disk = abspath(disk)
            statres = lstat(disk)
            if not S_ISLNK(statres.st_mode):
                if disk.startswith('/dev/'):
                    return resolve_disk('/sys/block/%s' % disk[5:])
                break
            disk = join(dirname(disk), readlink(disk))

        disk = abspath(disk)
        return disk

def find_disk_controller(disk):
    disk = resolve_disk(disk)
    for _, ctrl in disk_controllers.items():
        idx = ctrl.get_index(disk)
        if idx >= 0:
            return (ctrl, idx)
    return (None, -9001)

def map_disk(disk):
    ctrl, idx = find_disk_controller(disk)
    if not ctrl:
        return (None, -9001)
    return mappings['%s:%d' % (ctrl.id, idx)]

def set_disk_led(disk, led, clear=True):
    ctrl, idx = map_disk(disk)
    if not ctrl:
        return

    ctrl.write(idx, led, clear)

    if clear:
        for _, octrl in led_controllers.items():
            if octrl.id != ctrl.id:
                octrl.clear()

def clear_all():
        for _, octrl in led_controllers.items():
            octrl.clear()

if len(argv) < 2:
    clear_all()
else:
    d = argv[1]
    print(d)
    call(['smartctl', '-i', d])
    set_disk_led(d, LED_FAIL)
    sleep(5)
    set_disk_led(d, LED_LOCATE)
    sleep(5)
    set_disk_led(d, LED_REBUILD)
    sleep(5)
    set_disk_led(d, LED_OFF)
