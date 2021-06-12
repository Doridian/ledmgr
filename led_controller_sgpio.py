from led_controller_em_message import LEDBIT_REBUILD
from led_controller import LEDController, LED_FAIL, LED_LOCATE, LED_REBUILD
from subprocess import check_call

ledmap = {}
ledmap[LED_FAIL]    = 0b100
ledmap[LED_LOCATE]  = 0b010
ledmap[LED_REBUILD] = 0b110

class SGPIOLEDController(LEDController):
    def __init__(self, config):
        super().__init__(config)
        self.state = 0

    def clear(self):
        self.state = 0
        self.send()

    def write(self, idx, led, clear=True):
        ledbase = self._ledbase(idx)
        ledbit = ledmap[led]
        basestate = 0
        if not clear:
            basestate = (self.state & ~(0b111 << ledbase))
        self.state = basestate | (ledbit << ledbase)
        self._send()

    def _ledbase(self, idx):
        return idx * 3

    def _hexchop(self, b):
        return (self.state >> b) & 0xFF

    def _send(self):
        check_call(['smp_write_gpio', '--count=1', '--data=%x,%x,%x,%x' % (self._hexchop(24), self._hexchop(16), self._hexchop(8), self._hexchop(0)), '-t', '4', '--index=1', self.dev]) 
