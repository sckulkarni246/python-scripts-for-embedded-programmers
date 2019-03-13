import os
import sys
import serial
import argparse
import time
import hashlib
import OpenSSL.crypto as oc
import ecdsa
import binascii

# Set up argument parser
# Argument Parsers
appDescription = \
"Welcome to Honeywell Demo Application\
\r\n-----------------------------------------------"
argparser = argparse.ArgumentParser(description=appDescription)
argparser.add_argument("--port", default="COM19", help="COM port to open")
argparser.add_argument("--baudrate", default="115200", help="Baudrate in bps")
args = argparser.parse_args()

comport = args.port
baudrate = int(args.baudrate)

# Variables

VAL_CMDID_CONREQ        =       0x01
VAL_CMDID_CONAYE        =       0x02
VAL_CMDID_AUTHREQ       =       0x03
VAL_CMDID_CERT          =       0x04
VAL_CMDID_CHALL         =       0x05
VAL_CMDID_CHALLRESP     =       0x06
VAL_CMDID_CHALLRESPOK   =       0x07
VAL_CMDID_ECDHPUBKEY    =       0x08
VAL_CMDID_TTYL          =       0x09

SER_MAX_BYTES           =       0xFF

SRC_PC                  =       0xAA
SRC_GATEWAY             =       0x55

class Frame:
    def __init__(self):
        self.length = 0
        self.source = 0
        self.commandId = 0xFF
        self.payload = bytearray()
        self.checksum = 0
        self.rawframe = bytearray()

def calc_checksum(f):
    return 0xFF

def create_rawframe(source,commandId,payload):
    f = Frame()
    f.length = len(payload) + 5
    f.source = source
    f.commandId = commandId
    f.payload = payload
    f.payloadLen = len(payload)
    f.checksum = calc_checksum(f)

    f.rawframe = bytearray()
    f.rawframe.append(f.length & 0x00FF)
    f.rawframe.append(f.length & 0xFF00)
    f.rawframe.append(f.source)
    f.rawframe.append(f.commandId)
    f.rawframe.extend(f.payload)
    f.rawframe.append(f.checksum)

    return f.rawframe

def extract_cert_from_auth_response(f):
    # Extract n bytes from index 3 to (end-1)th byte
    fLen = f[0] + f[1]*256
    return f[4:fLen-1]

def verify_gateway_cert(cert):
    # Take cert and verify it using the pubkey - TODO
    f = open("rx-cert.pem","wb")
    f.write(cert)
    f.close()

    f = open("rx-cert.pem","rb")
    buf_rxcert = f.read()
    f.close()

    f = open("ca-cert.pem","rb")
    buf_cacert = f.read()
    f.close()

    certobj_rxcert = oc.load_certificate(oc.FILETYPE_PEM,buf_rxcert)
    certobj_cacert = oc.load_certificate(oc.FILETYPE_PEM,buf_cacert)

    store = oc.X509Store()
    store.add_cert(certobj_cacert)
    ctx = oc.X509StoreContext(store,certobj_rxcert)

    try:
        ctx.verify_certificate()
    except:
        print("ERROR! Could not verify certificate...")
        return False
    
    return True

def extract_challresp_from_response(f):
    fLen = f[0] + f[1]*256
    return f[4:68],f[68:fLen-1]

def verify_resp(cr,chall,pub):
    strpub = (binascii.hexlify(pub))
    strchall = (binascii.hexlify(chall))
    strcr = (binascii.hexlify(cr))
    print("<<----- Signature: " + strcr.decode() + " ----->>")
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(strpub.decode()),curve=ecdsa.NIST256p)
    try:
        vk.verify(bytes.fromhex(strcr.decode()), bytes.fromhex(strchall.decode()),hashfunc=hashlib.sha256) # True
    except:
        print("ERROR! Could not verify signature...")
        return False
    return True

def extract_pubkey_for_ecdhe(f):
    fLen = f[0] + f[1]*256
    return f[4:fLen-1]

def exit_handler():
    global ser
    if(ser.is_open == True):
        ser.close()
    sys.exit(0)

# Create a serial port object
ser = serial.Serial()
ser.baudrate = 115200
ser.timeout = 0.5
ser.port = comport

# Open the serial port
print("Opening COM Port...")
ser.open()
portOpened = False
if(ser.is_open == True):
    portOpened = True

# Connection Request (PC to Gateway)

txFrame = bytearray()
rxFrame = bytearray()
txFramePayload = bytearray()
numBytes = 0

########## CONNECTION REQUEST ###########
print("SENDING connection request...")
txFrame = create_rawframe(SRC_PC,VAL_CMDID_CONREQ,txFramePayload)
numBytes = ser.write(txFrame)
time.sleep(1)

numBytes = ser.in_waiting
if(numBytes > 0):
    rxFrame = ser.read(numBytes)
    print("SUCCESS! Gateway responded to the connection request..." + str(numBytes) + " bytes were received...")
else:
    print("ERROR! Gateway did not respond to connection request...EXITING...")
    exit_handler()

########## AUTHENTICATION REQUEST ###########
print("SENDING authentication request...")
txFrame = create_rawframe(SRC_PC,VAL_CMDID_AUTHREQ,txFramePayload)
numBytes = ser.write(txFrame)
time.sleep(1)

numBytes = ser.in_waiting
if(numBytes > 0):
    rxFrame = ser.read(numBytes)
    print("SUCCESS! Gateway responded to the authentication request..." + str(numBytes) + " bytes were received...")
else:
    print("ERROR! Gateway did not respond to authentication request...EXITING...")
    exit_handler()

gatewayCert = extract_cert_from_auth_response(rxFrame)
certOk = verify_gateway_cert(gatewayCert)

if(certOk == True):
    print("SUCCESS! Gateway certificate was verified successfully...")
else:
    print("ERROR! Gateway cert could not be verified successfully...EXITING...")
    exit_handler()

########## CHALLENGE TO GATEWAY ###########
print("SENDING random challenge...")
randomString = b"Hi I am a random challenge!"
txFramePayload = bytearray(hashlib.sha256(randomString).digest())
txFrame = create_rawframe(SRC_PC,VAL_CMDID_CHALL,txFramePayload)
numBytes = ser.write(txFrame)
time.sleep(1)

numBytes = ser.in_waiting
if(numBytes > 0):
    rxFrame = ser.read(numBytes)
    print("SUCCESS! Gateway responded to the challenge..." + str(numBytes) + " bytes were received...")
else:
    print("ERROR! Gateway did not respond to challenge...EXITING...")
    sys.exit(0)

challresp,mypub = extract_challresp_from_response(rxFrame)
respOk = verify_resp(challresp,randomString,mypub)

if(respOk == True):
    print("SUCCESS! The gateway's response has been verified successfully...")

########## SEND CHALLRESPOK ##########
print("SENDING challenge response OK...")
txFramePayload = bytearray()
txFrame = create_rawframe(SRC_PC,VAL_CMDID_CHALLRESPOK,txFramePayload)
numBytes = ser.write(txFrame)
time.sleep(1)

numBytes = ser.in_waiting
if(numBytes > 0):
    rxFrame = ser.read(numBytes)
    print("SUCCESS! Gateway has sent its new public key for ECDHE..." + str(numBytes) + " bytes were received...")
else:
    print("ERROR! Gateway did not respond with its new public key for ECDHE...EXITING...")
    sys.exit(0)

gwpubkey = extract_pubkey_for_ecdhe(rxFrame)
print("<<----- Public Key for ECDHE: " + binascii.hexlify(gwpubkey).decode() + " ----->>")

############## THE END #################
ser.close()
print("End of demo...EXITING...")
sys.exit(0)
        

