from led_controller import LED_FAIL, LED_LOCATE, LED_OFF, LED_REBUILD
from config import Config
from argparse import ArgumentParser

LEDSTATE_BY_STRING = {
    'off': LED_OFF,
    'fail': LED_FAIL,
    'rebuild': LED_REBUILD,
    'locate': LED_LOCATE,
}


parser = ArgumentParser()
parser.add_argument('--clear', dest='clear', help='Whether to unset/blank unnamed LEDs or not', type=bool, default=True)
parser.add_argument('--config', dest='config', help='config file to use', type=str, default='config.json')
parser.add_argument('leds', metavar='LED', type=str, nargs='*', help='LEDs to set in the form of STATE=DISKDEV (ex: locate=/dev/sda)')
args = parser.parse_args()

config = Config(args.config)

if args.clear:
    config.clear_all()

for ledspec in args.leds:
    led, disk = ledspec.split('=', 1)
    ledval = LEDSTATE_BY_STRING[led.lower()]
    config.set_disk_led(disk, ledval)

config.send_all()
