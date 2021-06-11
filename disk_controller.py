from base_controller import BaseController

class DiskController(BaseController):
    def __init__(self, config):
        super().__init__(config)

    def get_index(self, disk):
        if not disk.startswith(self.dev):
            return -9001

        # TODO: This is kinda stupid...
        for i in range(self.subdev_value, 100):
            if disk.startswith('%s/%s/' % (self.dev, self.subdev.replace('#', '%d' % i))):
                return (i - self.subdev_value)

        return -9002
