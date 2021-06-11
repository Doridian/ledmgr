LED_OFF = 0
LED_LOCATE = 1
LED_FAIL = 2

class Controller:
    def __init__(self, dev, count):
        self.dev = dev
        self.count = count
