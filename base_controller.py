from os.path import exists, abspath

def find_char_offset(pattern, char):
    if not char in pattern:
        return (-8001, pattern)

    for i in range(0, 100):
        dev = pattern.replace(char, '%d' % i)
        if exists(dev):
            return (i, dev)

    return (-8002, pattern)

class BaseController:
    def __init__(self, config):
        self.id = config['id']
        self.dev_value, self.dev = find_char_offset(config['dev'], '*')
        self.dev = abspath(self.dev)

        if 'subdev' not in config:
            self.subdev = None
            self.subdev_value = -8003
            self.subdev2_value = -8003
            return

        self.subdev = config['subdev'].replace('*', '%d' % self.dev_value)

        subdev1 = self.subdev
        if 'subdev_pre' in config:
            subdev1 = config['subdev_pre'].replace('*', '%d' % self.dev_value)
        self.subdev_value, _ = find_char_offset('%s/%s' % (self.dev, subdev1), '#')

        subdev2 = self.subdev.replace('#', '%d' % self.subdev_value)
        self.subdev2_value, _ = find_char_offset('%s/%s' % (self.dev, subdev2), '$')
