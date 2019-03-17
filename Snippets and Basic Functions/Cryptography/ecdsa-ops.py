import ecdsa
import hashlib

sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
vk = sk.get_verifying_key()

a = b"Hello World!"

sig = sk.sign(a,hashfunc=hashlib.sha256)
result = vk.verify(sig,a,hashfunc=hashlib.sha256)

strsk = sk.to_string()
strvk = vk.to_string()

sk2 = ecdsa.SigningKey.from_string(strsk,curve=ecdsa.NIST256p)
vk2 = sk2.get_verifying_key()
