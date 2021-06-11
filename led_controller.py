from base_controller import BaseController

LED_OFF = 0
LED_LOCATE = 1
LED_FAIL = 2

class LEDController(BaseController):
    def __init__(self, config):
        super().__init__(config)
        self.count = config['count']