from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import time

start_time = time.time()

# Generer et nyt RSA nøglepar
key = RSA.generate(2048)
key_gen_time = time.time() - start_time

private_key = key.export_key()
public_key = key.publickey().export_key()

# Initialiser krypteringen
message = "Dette er en hemmelig besked."
start_time = time.time()
encryptor = PKCS1_OAEP.new(RSA.import_key(public_key))
encrypted = encryptor.encrypt(message.encode())
encrypt_time = time.time() - start_time

# Initialiser dekrypteringen
start_time = time.time()
decryptor = PKCS1_OAEP.new(RSA.import_key(private_key))
decrypted = decryptor.decrypt(encrypted)
decrypt_time = time.time() - start_time

# Print tider og resultater
print(f"Nøglegenereringstid: {key_gen_time} sekunder")
print(f"Krypteringstid: {encrypt_time} sekunder")
print(f"Dekrypteringstid: {decrypt_time} sekunder")
print(f"Krypteret besked: {binascii.hexlify(encrypted)}")
print(f"Dekrypteret besked: {decrypted.decode()}")
