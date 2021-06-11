from controller_sgpio import LEDBIT_FAIL
from controller import Controller, LED_FAIL, LED_LOCATE, LED_OFF

LEDBIT_FAIL   = 0b1 << 22
LEDBIT_LOCATE = 0b1 << 19

class EMMessageController(Controller):
    def __init__(self, dev, count):
        super().__init__(dev, count)

    def clear(self):
        for i in range(0, self.count):
            self._write(i, LED_OFF)

    def _sysfs_name(self, idx):
        return "%s/ata%d/host%d/scsi_host/host%d/em_message" % (self.dev, idx, idx, idx)

    def _write(self, idx, led):
        sysfs = self._sysfs_name(idx)
        
        ledbit = 0
        if led == LED_FAIL:
            ledbit = LEDBIT_FAIL
        elif led == LED_LOCATE:
            ledbit = LEDBIT_LOCATE
        
        fh = open(sysfs, 'w')
        fh.write("%d\n" % ledbit)
        fh.close()

    def write(self, idx, led, clear=True):
        self._write(idx, led)
        if clear:
            for i in range(0, self.count):
                if i == idx:
                    continue
                self._write(i, LED_OFF)
