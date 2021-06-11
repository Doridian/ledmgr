from controller_em_message import EMMessageController
from controller import LED_FAIL
from controller_sgpio import SGPIOController

from time import sleep

ctrl = SGPIOController('/sys/devices/pci0000:00/0000:00:11.0/0000:05:00.0/host7/bsg/sas_host7', 4)
for i in range(0,4):
    print("Setting LED %d" % i)
    ctrl.write(i, LED_FAIL)
    sleep(1)
ctrl.clear()

ctrl = EMMessageController('/sys/devices/pci0000:00/0000:00:1f.2', 6)
for i in range(0,4):
    print("Setting LED2 %d" % i)
    ctrl.write(i, LED_FAIL)
    sleep(1)
ctrl.clear()
