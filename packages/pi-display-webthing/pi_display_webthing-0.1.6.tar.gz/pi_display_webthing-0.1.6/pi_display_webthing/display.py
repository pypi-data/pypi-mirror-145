from RPLCD.i2c import BaseCharLCD
import threading
import time
import uuid


class Panel:

    def __init__(self, display, changed_listener):
        self.display = display
        self.changed_listener = changed_listener
        self.__text = ""
        self.__ttl = -1
        self.ttl_watchdog_id = None

    @property
    def ttl(self) -> int:
        return self.__ttl

    @property
    def text(self) -> str:
        return self.__text

    def update_text(self, text: str):
        self.__text = text
        self.display.on_panel_updated()
        self.changed_listener()

    def update_ttl(self, ttl: int):
        self.__ttl = ttl
        wdid = str(uuid.uuid4())
        self.ttl_watchdog_id = wdid
        threading.Thread(target = self.run_expire_watchdog, args = (ttl, wdid)).start()

    def run_expire_watchdog(self, ttl: int, wdid: str):
        remaining_sec = ttl
        while (remaining_sec > 0):
            time.sleep(1)
            remaining_sec = remaining_sec - 1
            if self.ttl_watchdog_id == wdid:
                if remaining_sec > 0:
                    self.__ttl = remaining_sec
                    self.changed_listener()
                else:
                    self.clear()

    def clear(self):
        self.__text = ""
        self.__ttl = -1
        self.display.on_panel_updated()
        self.changed_listener()

    def is_empty(self):
        return len(self.__text) == 0


class Display:

    LAYER_UPPER = 0
    LAYER_MIDDLE = 1
    LAYER_LOWER = 2

    def __init__(self, lcd: BaseCharLCD, changed_listener):
        self.__lcd = lcd
        self.__text = ""
        self.changed_listener = changed_listener
        self.panels = [Panel(self, changed_listener), Panel(self, changed_listener), Panel(self, changed_listener)]

    def panel(self, layer: int) -> Panel:
        return self.panels[layer]

    @property
    def text(self) -> str:
        return self.__text

    def __update_text(self, text: str):
        self.__text = text
        self.__lcd.clear()
        self.__lcd.write_string(self.__text)
        self.changed_listener()

    def on_panel_updated(self):
        text = ""
        for layer in range(0, len(self.panels)):
            panel = self.panels[layer]
            if not panel.is_empty():
                text = panel.text
                break
        self.__update_text(text)