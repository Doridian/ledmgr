from disk_controller import DiskController
from led_controller_em_message import EMMessageLEDController
from led_controller_sgpio import SGPIOLEDController
from json import load
from os import lstat, readlink
from os.path import abspath, join, dirname
from stat import S_ISLNK

class Config:
    def __init__(self, file):
        self.led_controllers = {}
        self.disk_controllers = {}
        self.mappings = {}

        fh = open(file, 'r')
        config = load(fh)
        fh.close()

        for ctrlc in config['led_controllers']:
            type = ctrlc['type'].lower()
            if type == 'em_message':
                CTor = EMMessageLEDController
            elif type == 'sgpio':
                CTor = SGPIOLEDController
            else:
                raise ValueError('Unknown controller type: %s' % type)
            ctrlo = CTor(ctrlc)
            self.led_controllers[ctrlo.id] = ctrlo

        for ctrlc in config['disk_controllers']:
            ctrlo = DiskController(ctrlc)
            self.disk_controllers[ctrlo.id] = ctrlo

        for map in config['mappings']:
            to = map['to'].split(':')
            self.mappings[map['from']] = (self.led_controllers[to[0]], int(to[1]))

    def resolve_disk(self, disk):
            while True:
                disk = abspath(disk)
                statres = lstat(disk)
                if not S_ISLNK(statres.st_mode):
                    if disk.startswith('/dev/'):
                        return self.resolve_disk('/sys/block/%s' % disk[5:])
                    break
                disk = join(dirname(disk), readlink(disk))

            disk = abspath(disk)
            return disk

    def find_disk_controller(self, disk):
        disk = self.resolve_disk(disk)
        for _, ctrl in self.disk_controllers.items():
            idx = ctrl.get_index(disk)
            if idx >= 0:
                return (ctrl, idx)
        return (None, -9001)

    def map_disk(self, disk):
        ctrl, idx = self.find_disk_controller(disk)
        if not ctrl:
            return (None, -9001)
        return self.mappings['%s:%d' % (ctrl.id, idx)]

    def set_disk_led(self, disk, led):
        ctrl, idx = self.map_disk(disk)
        if not ctrl:
            raise ValueError('Unknown disk: %s' % disk)
        ctrl.write(idx, led)

    def clear_all(self):
        for _, octrl in self.led_controllers.items():
            octrl.clear()

    def send_all(self):
        for _, octrl in self.led_controllers.items():
            octrl.send()
