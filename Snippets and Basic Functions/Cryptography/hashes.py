import hashlib
import binascii

msg = b"Hey this is a message!"
hashop = hashlib.sha256(msg).digest()
print(binascii.hexlify(hashop).decode())