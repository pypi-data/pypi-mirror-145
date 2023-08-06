from string import Template
from pi_display_webthing.app import App
from pi_display_webthing.display_webthing import run_server
from pi_display_webthing.detect_devices import scan


PACKAGENAME = 'pi_display_webthing'
ENTRY_POINT = "display"
DESCRIPTION = "A web connected LCD display module"


UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target network.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --verbose $verbose --port $port --name $name --i2c_address $i2c_address --i2c_expander $i2c_expander
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
''')




class DhtApp(App):

    def do_add_argument(self, parser):
        parser.add_argument('--i2c_expander', metavar='i2c_expander', required=False, type=str, help='the name of the port I²C port expander. Supported: PCF8574, MCP23008, MCP23017')
        parser.add_argument('--i2c_address', metavar='i2c_address', required=False, type=str, help='the I²C address of the LCD Module as hex string')
        parser.add_argument('--name', metavar='name', required=False, type=str, default="", help='the name of the display')

    def do_additional_listen_example_params(self):
        devices = scan()
        if len(devices) > 0:
            device = devices[0]
        else:
            device = " 0x29"
        return "--name nas --i2c_expander PCF8574 --i2c_address " + device

    def do_process_command(self, command:str, port: int, verbose: bool, args) -> bool:
        if command in {'listen', 'register'} and args.i2c_address is None:
            devices = scan()
            if len(devices) == 0:
                print("no devices detected")
                return False
            elif len(devices) > 1:
                print("more than 1 devices found: " + ", ".join(devices) + "\n use --i2c_address parameter to select device")
                return False
            else:
                args.i2c_address = devices[0]
                print("device " + args.i2c_address + " detected. Using it")

        if command == 'listen' and (args.i2c_expander is not None) and (args.i2c_address is not None):
            print("running " + self.packagename + " on  " + str(port))
            run_server(port, args.name, args.i2c_expander, self.to_hex(args.i2c_address), self.description)
            return True

        elif args.command == 'register' and (args.i2c_expander is not None) and (args.i2c_address is not None):
            print("register " + self.packagename  + " on " + str(port) + " and starting it")
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename, entrypoint=self.entrypoint, port=port, verbose=verbose, name=args.name, i2c_expander=args.i2c_expander, i2c_address=args.i2c_address)
            self.unit.register(port, unit)
            return True
        else:
            return False

    def to_hex(self, hexString: str) -> int:
        if hexString.startswith("0x"):
            return int(hexString, 16)
        else:
            return int(hexString)


def main():
    DhtApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()
