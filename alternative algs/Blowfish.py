from Cryptodome.Cipher import Blowfish
from Cryptodome.Random import get_random_bytes
import time
import os


def encrypt_file(key, file_path, iv):
    cipher = Blowfish.new(key, Blowfish.MODE_CFB, iv)
    # Specify the path to the file you want to encrypt
    with open(file_path, "rb") as f:
        # Read the contents of the file
        plaintext = f.read()

    ciphertext = cipher.encrypt(plaintext)
    with open(file_path + ".enc", "wb") as f:
        f.write(ciphertext)

    # delete the original file
    os.remove(file_path)


def decrypt_file(key, file_path, iv):
    decipher = Blowfish.new(key, Blowfish.MODE_CFB, iv)
    with open(file_path + ".enc", "rb") as f:
        ciphertext = f.read()

    # Decrypt the contents of the file
    plaintext = decipher.decrypt(ciphertext)
    with open(file_path + ".enc", "wb") as f:
        f.write(plaintext)


# Generate a random key and initialization vector
enc_key = get_random_bytes(Blowfish.key_size[0])  # NOQA
init_vect = get_random_bytes(Blowfish.block_size)

file_set = set()

# Encrypt
for file in file_set:
    encrypt_file(enc_key, file, init_vect)
   
# Decrypt
for file in file_set:
    decrypt_file(enc_key, file, init_vect)
