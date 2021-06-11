LED_OFF = 0
LED_LOCATE = 1
LED_FAIL = 2

class Controller:
    def __init__(self, dev) -> None:
        self.dev = dev
