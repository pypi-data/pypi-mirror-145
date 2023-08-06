from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
from RPLCD.i2c import CharLCD, BaseCharLCD
from pi_display_webthing.display import Display
import tornado.ioloop
import logging


class DisplayWebThing(Thing):
    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, name: str, description: str, lcd: BaseCharLCD):
        Thing.__init__(
            self,
            'urn:dev:ops:lcddisplay-1',
            'Display ' + name + ' Controller',
            ['Display'],
            description
        )

        self.display = Display(lcd, self.__update_text)

        self.display_text = Value("")
        self.add_property(
            Property(self,
                     'displayed_text',
                     self.display_text,
                     metadata={
                         'title': 'Displayed text',
                         'type': 'string',
                         'description': 'Displayed text',
                         'readOnly': True,
                     }))

        self.upper_layer_text = Value("", self.display.panel(Display.LAYER_UPPER).update_text)
        self.add_property(
            Property(self,
                     'upper_layer_text',
                     self.upper_layer_text,
                     metadata={
                         'title': 'Upper layer text',
                         'type': 'string',
                         'description': 'The text of the upper layer',
                         'readOnly': False,
                     }))

        self.upper_layer_text_ttl = Value(-1, self.display.panel(Display.LAYER_UPPER).update_ttl)
        self.add_property(
            Property(self,
                     'upper_layer_text_ttl',
                     self.upper_layer_text_ttl,
                     metadata={
                         'title': 'Upper layer text (time-to-live)',
                         'type': 'integer',
                         'description': 'The time-to-live of the upper layer. Value -1 deactivates ttl',
                         'readOnly': False,
                     }))

        self.middle_layer_text = Value("", self.display.panel(Display.LAYER_MIDDLE).update_text)
        self.add_property(
            Property(self,
                     'middle_layer_text',
                     self.middle_layer_text,
                     metadata={
                         'title': 'Middle layer text',
                         'type': 'string',
                         'description': 'The text of the middle layer',
                         'readOnly': False,
                     }))

        self.middle_layer_text_ttl = Value(-1, self.display.panel(Display.LAYER_MIDDLE).update_ttl)
        self.add_property(
            Property(self,
                     'middle_layer_text_ttl',
                     self.middle_layer_text_ttl,
                     metadata={
                         'title': 'Middle layer text (time-to-live)',
                         'type': 'integer',
                         'description': 'The time-to-live of the middle layer. Value -1 deactivates ttl',
                         'readOnly': False,
                     }))

        self.lower_layer_text = Value("", self.display.panel(Display.LAYER_LOWER).update_text)
        self.add_property(
            Property(self,
                     'lower_layer_text',
                     self.lower_layer_text,
                     metadata={
                         'title': 'Lower layer text',
                         'type': 'string',
                         'description': 'The text of the lower layer',
                         'readOnly': False,
                     }))

        self.lower_layer_text_ttl = Value(-1, self.display.panel(Display.LAYER_LOWER).update_ttl)
        self.add_property(
            Property(self,
                     'lower_layer_text_ttl',
                     self.lower_layer_text_ttl,
                     metadata={
                         'title': 'Lower layer text (time-to-live)',
                         'type': 'integer',
                         'description': 'The time-to-live of the lower layer. Value -1 deactivates ttl',
                         'readOnly': False,
                     }))

        self.ioloop = tornado.ioloop.IOLoop.current()


    def __update_text(self):
        self.ioloop.add_callback(self.__update_text_props)

    def __update_text_props(self):
        self.display_text.notify_of_external_update(self.display.text)
        self.upper_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_UPPER).text)
        self.upper_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_UPPER).ttl)
        self.middle_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_MIDDLE).text)
        self.middle_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_MIDDLE).ttl)
        self.lower_layer_text.notify_of_external_update(self.display.panel(Display.LAYER_LOWER).text)
        self.lower_layer_text_ttl.notify_of_external_update(self.display.panel(Display.LAYER_LOWER).ttl)


def createI2C(i2c_expander: str, i2c_address: int) -> BaseCharLCD:
    logging.info("bind driver to address " + hex(i2c_address) + " using port expander " + i2c_expander)
    return CharLCD(i2c_expander, i2c_address)


def run_server(port: int, name:str, i2c_expander: str, i2c_address: int, description: str):
    lcd = createI2C(i2c_expander, i2c_address)
    display_webthing = DisplayWebThing(name, description, lcd)
    server = WebThingServer(SingleThing(display_webthing), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')
