from os.path import exists

def find_char_offset(pattern, char):
    if not char in pattern:
        return (-9001, pattern)

    for i in range(0, 100):
        dev = pattern.replace(char, '%d' % i)
        if exists(dev):
            return (i, dev)

    return (-9002, pattern)

class BaseController:
    def __init__(self, config):
        self.id = config['id']
        self.dev_value, self.dev = find_char_offset(config['dev'], '*')

        if 'subdev' not in config:
            self.subdev = None
            self.subdev_value = -9003
            return

        subdev = config['subdev'].replace('*', '%d' % self.dev_value)
        self.subdev_value, _ = find_char_offset('%s/%s' % (self.dev, subdev), '#')
        self.subdev = subdev
