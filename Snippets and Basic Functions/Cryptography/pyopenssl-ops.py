import OpenSSL.crypto as oc

# Read node cert
f = open("nodecert.pem","rb")
buf_nodecert = f.read()
f.close()

# Read ca cert
f = open("cacert.pem","rb")
buf_cacert = f.read()
f.close()

# Convert to OpenSSL objects
obj_nodecert = oc.load_certificate(buf_nodecert)
obj_cacert = oc.load_certificate(buf_cacert)

# Open a store
store = oc.X509Store()

# Add the CA cert object to the store and create a context with Node cert
store.add_cert(certobj_cacert)
ctx = oc.X509StoreContext(store,certobj_rxcert)

try:
	ctx.verify_certificate()
except:
	print("ERROR! Could not verify certificate...")
	return False
