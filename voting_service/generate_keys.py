from Crypto.PublicKey import RSA

# Generate a new RSA key
private_key = RSA.generate(2048)

# Get the public key from the private key
public_key = private_key.publickey()

# Export the private key in PEM format
private_key_pem = private_key.export_key()
print(private_key_pem.decode())

# Export the public key in PEM format
public_key_pem = public_key.export_key()
print(public_key_pem.decode())