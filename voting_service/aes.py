from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt(key,message):
    encryptor = AES.new(key, AES.MODE_GCM)
    ciphertext = encryptor.encrypt(message)
    nonce = encryptor.nonce
    return ciphertext,nonce

def decrypt(key,message,nonce):
    encryptor = AES.new(key, AES.MODE_GCM,nonce)
    ciphertext = encryptor.encrypt(message)
    return ciphertext

def cmac(key,message):
    c = CMAC.new(key, ciphermod=AES)
    c.update(message)
    mac = c.hexdigest()
    return mac 

if __name__ == "__main__":
    text = 'cryptovote'
    nic = '199845188250'

    key = int(nic).to_bytes(5,'big')+get_random_bytes(11) 

    #encryption
    ciphertext,nonce = encrypt(key,text.encode())
    cmac_text = cmac(key,ciphertext)

    #decryption
    deciphertext = decrypt(key,ciphertext,nonce)
    cmac_cipher = cmac(key,ciphertext)

    print("input text:",text)
    print("AES128:",key)
    print("Encrypted:",ciphertext)
    print("text cmac:",cmac_text)
    print("nonce:",nonce)
    print("Decrypted: ",deciphertext)
    print("encrypted cmac:",cmac_cipher)
    print("cmac verified:",cmac_cipher==cmac_text)
