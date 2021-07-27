from led_controller import LEDController, LED_FAIL, LED_LOCATE, LED_OFF, LED_REBUILD
from errno import EBUSY
from time import sleep

ledmap = {}
LED_KEEP = -1
ledmap[LED_OFF]     = 0
ledmap[LED_FAIL]    = 0b1 << 22
ledmap[LED_LOCATE]  = 0b1 << 19
ledmap[LED_REBUILD] = ledmap[LED_FAIL] | ledmap[LED_LOCATE]

class EMMessageLEDController(LEDController):
    def __init__(self, config):
        super().__init__(config)
        self.states = [LED_KEEP] * self.count

    def clear(self):
        self.states = [ledmap[LED_OFF]] * self.count

    def write(self, idx, led):
        self.states[idx] = ledmap[led]

    def send(self):
        for idx, led in enumerate(self.states):
            self._write(idx, led)

    def _sysfs_name(self, idx):
        return '%s/%s/em_message' % (self.dev, self.subdev
            .replace('#', '%d' % (idx + self.subdev_value))
            .replace('$', '%d' % (idx + self.subdev2_value))
        )

    def _write(self, idx, led):
        if led == LED_KEEP:
            return

        sysfs = self._sysfs_name(idx)

        data = '%d\n' % led

        fh = open(sysfs, 'r')
        fd = fh.read()
        fh.close()

        if fd == data:
            return

        while True:
            try:
                fh = open(sysfs, 'w')
                fh.write('%d\n' % led)
                fh.close()
                break
            except OSError as e:
                if e.errno != EBUSY:
                    raise e
            sleep(0.05)
