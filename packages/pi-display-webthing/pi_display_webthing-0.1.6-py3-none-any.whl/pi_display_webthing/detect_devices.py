from smbus2 import SMBus
from typing import List


def scan() -> List[str]:
    devices = []
    try:
        bus = SMBus(1) # 1 indicates /dev/i2c-1
        for device in range(128):
            try:
                bus.read_byte(device)
                devices.append(hex(device))
            except:
                pass
    except FileNotFoundError as e:
        print("WARNING: I2C seems not to be activated")
    return devices

