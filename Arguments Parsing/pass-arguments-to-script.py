import argparse

# Argument Parsers
appDescription = \
"Pass arguments to this app - it will print them\
\r\n-----------------------------------------------"
argparser = argparse.ArgumentParser(description=appDescription)
argparser.add_argument("--arg1", default="False1", help="Argument 1 - this text will come up in help")
argparser.add_argument("--arg2", default="False2", help="Argument 2 - this text will come up in help")
argparser.add_argument("--arg3", default="False3", help="Argument 3 - this text will come up in help")
argparser.add_argument("--arg4", default="False4", help="Argument 4 - this text will come up in help")
argparser.add_argument("--arg5", default="False5", help="Argument 5 - this text will come up in help")
args = argparser.parse_args()

arg1 = args.arg1
arg2 = args.arg2
arg3 = args.arg3
arg4 = args.arg4
arg5 = args.arg5

print("%s %s %s %s %s" %(arg1,arg2,arg3,arg4,arg5))