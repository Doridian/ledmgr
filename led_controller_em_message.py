from led_controller import LEDController, LED_FAIL, LED_LOCATE, LED_OFF, LED_REBUILD
from errno import EBUSY
from time import sleep

ledmap = {}
ledmap[LED_FAIL]    = 0b1 << 22
ledmap[LED_LOCATE]  = 0b1 << 19
ledmap[LED_REBUILD] = ledmap[LED_FAIL] | ledmap[LED_LOCATE]

class EMMessageLEDController(LEDController):
    def __init__(self, config):
        super().__init__(config)

    def clear(self):
        for i in range(0, self.count):
            self._write(i, LED_OFF)

    def write(self, idx, led, clear=True):
        self._write(idx, led)
        if clear:
            for i in range(0, self.count):
                if i == idx:
                    continue
                self._write(i, LED_OFF)

    def _sysfs_name(self, idx):
        return '%s/%s/em_message' % (self.dev, self.subdev.replace('#', '%d' % (idx + self.subdev_value)))

    def _write(self, idx, led):
        sysfs = self._sysfs_name(idx)

        ledbit = ledmap[led]

        data = '%d\n' % ledbit

        fh = open(sysfs, 'r')
        fd = fh.read()
        fh.close()

        if fd == data:
            return

        while True:
            try:
                fh = open(sysfs, 'w')
                fh.write('%d\n' % ledbit)
                fh.close()
                break
            except OSError as e:
                if e.errno != EBUSY:
                    raise e
            sleep(0.05)
