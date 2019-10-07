import sys, os
import getopt

try: 
    import esptool
except ImportExcept:
    print("No esptool module found. Install it, using: pip install esptool")
    sys.exit(4)

def find_port():
    ports = esptool.list_ports.comports()

    ports = [p for p in ports if is_skribrain_port(p)]

    if not ports:
        raise Exception('             No suitable port found.\n'
                        'Check the Skribrain connection and try again.')
    elif len(ports) > 1:
        raise Exception('     More than one Skribrain detected.\n'
                        'Connect only one Skribrain and try again.')
    else:
        print(ports[0].device)
        return ports[0]

def is_skribrain_port(port):
    return (port.product and port.product.encode('utf-8') == b'FT231X USB UART') \
        or (port.manufacturer and port.manufacturer.encode('utf-8') == 'FTDI')


def upload_esp(port, boot_app, bootloader, skribot_app, skribot_parts):
        esptool_args = [
            '--chip', 'esp32',
            '--port', port,
            '--baud', '921600',
            '--before', 'default_reset',
            '--after', 'hard_reset',
            'write_flash', '-z',
            '--flash_mode', 'dio',
            '--flash_freq', '80m',
            '--flash_size', 'detect',
            '0xe000', boot_app,
            '0x1000', bootloader,
            '0x10000', skribot_app,
            '0x8000', skribot_parts]
        try:
            esptool.main(esptool_args)
        except Exception as e:
            print("ESP upload_esp failed {}".format(e))

def help():
    print("Usage:\npython main.py -a <skribot_app> -p <skribot_parts>")
    print("i.e.: python main.py -p SkriBotApp.ino.partitions.bin -a SkriBotApp.ino.bin")

def main():
    skribot_app = None
    skribot_parts = None
    
    boot_app = "boot_app0.bin"
    bootloader = "bootloader_qio_80m.bin"

    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ha:p:")
        except getopt.GetoptError as err:
            # print help information and exit:
            print(str(err))  # will print something like "option -a not recognized"
            sys.exit(2)
        else:
            for o, a in opts:
                if o == '-h':
                    help()
                    sys.exit(0)
                elif o == '-a':
                    skribot_app = a
                elif o == '-p':
                    skribot_parts = a

    port = find_port()
    upload_esp(port.device, boot_app, bootloader, skribot_app, skribot_parts)

if __name__ == "__main__":
    main()



