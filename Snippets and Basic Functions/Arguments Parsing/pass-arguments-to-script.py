import argparse

# Argument Parsers
appDescription = \
"Pass arguments to this app - it will print them\
\r\n-----------------------------------------------"
argparser = argparse.ArgumentParser(description=appDescription)
argparser.add_argument("--port", default="COM1", help="Port to open")
argparser.add_argument("--baudrate", default="115200", help="Baudrate in bps")
args = argparser.parse_args()

port = args.port
baudrate = args.baudrate

print("%s %s" %(port,baudrate))