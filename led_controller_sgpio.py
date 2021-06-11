from led_controller import LEDController, LED_FAIL, LED_LOCATE
from subprocess import check_call

LEDBIT_FAIL   = 0b100
LEDBIT_LOCATE = 0b010

class SGPIOLEDController(LEDController):
    def __init__(self, config):
        super().__init__(config)
        self.state = 0

    def clear(self):
        self.state = 0
        self.send()

    def write(self, idx, led, clear=True):
        ledbase = self._ledbase(idx)
        ledbit = 0b000
        if led == LED_FAIL:
            ledbit = LEDBIT_FAIL
        elif led == LED_LOCATE:
            ledbit = LEDBIT_LOCATE
        basestate = 0
        if not clear:
            basestate = (self.state & ~(0b111 << ledbase))
        self.state = basestate | (ledbit << ledbase)
        self.send()

    def _ledbase(self, idx):
        return idx * 3

    def _hexchop(self, b):
        return (self.state >> b) & 0xFF

    def send(self):
        check_call(['smp_write_gpio', '--count=1', '--data=%x,%x,%x,%x' % (self._hexchop(24), self._hexchop(16), self._hexchop(8), self._hexchop(0)), '-t', '4', '--index=1', '%s/dev' % self.dev]) 
