from genericpath import exists
from base_controller import BaseController

class DiskController(BaseController):
    def __init__(self, config):
        super().__init__(config)
        if 'subdev_find' in config:
            self.subdev_find = config['subdev_find'].replace('*', '%d' % self.dev_value)
        else:
            self.subdev_find = None

    def get_index(self, disk):
        if not disk.startswith(self.dev):
            return -9001

        subdev_find = self.subdev
        if self.subdev_find:
            subdev_find = self.subdev_find

        # TODO: This is kinda stupid...
        found_devphy = None
        found_i = -9002
        for i in range(0, 100):
            devphy = '%s/%s/' % (self.dev, subdev_find.replace('#', '%d' % i))
            if disk.startswith(devphy):
                found_devphy = devphy
                found_i = i
                break

        if self.subdev_find:
            found_i = -9003
            for i in range(self.subdev_value, 100): 
                devphysub = '%s/%s/' % (found_devphy, self.subdev.replace('#', '%d' % i))
                if exists(devphysub):
                    found_i = i
                    break

        return found_i - self.subdev_value
