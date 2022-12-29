from Crypto.Cipher import Blowfish
from twofish import Twofish
from cryptography.fernet import Fernet
from Cryptodome.Random import get_random_bytes
import random
import string
import os
import time


def encrypt_file_two(file_path, key):
    # Read the input file in binary mode
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # check the length of the plaintext and add "a" to it if it is not a multiple of 16 cuz im too lazy to do padding
    if len(key) % 16 != 0:
        key_fill = 16 - len(key) % 16
        key += "a" * key_fill

    if len(plaintext) % 16 != 0:
        plaintext_fill = 16 - len(plaintext) % 16
        plaintext += b"a" * plaintext_fill

    cipher = Twofish()
    cipher.set_key(str.encode(key))

    ciphertext = cipher.encrypt(plaintext)

    with open(file_path + ".enc", "wb") as f:
        f.write(ciphertext)

    os.remove(file_path)


def decrypt_file_two(file_path, key):
    file_path += ".enc"

    # Read the input file in binary mode
    with open(file_path, "rb") as f:
        ciphertext = f.read()

    if len(key) % 16 != 0:
        key_fill = 16 - len(key) % 16
        key += "a" * key_fill

    cipher = Twofish()
    cipher.set_key(str.encode(key))

    plaintext = cipher.decrypt(ciphertext)

    while plaintext.endswith(b"a"):
        plaintext = plaintext[:-1]

    with open(file_path[:-4], "wb") as f:
        f.write(plaintext)

    # Remove the original input file
    os.remove(file_path)


def encrypt_file_blow(key, file_path, iv):
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


def decrypt_file_blow(key, file_path, iv):
    decipher = Blowfish.new(key, Blowfish.MODE_CFB, iv)
    with open(file_path + ".enc", "rb") as f:
        ciphertext = f.read()

    # Decrypt the contents of the file
    plaintext = decipher.decrypt(ciphertext)
    with open(file_path, "wb") as f:
        f.write(plaintext)

    os.remove(file_path + ".enc")


# Define stuff
decr_key_blow = Fernet.generate_key()
init_vect = get_random_bytes(Blowfish.block_size)
decr_key_two = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(22))

# check current directory for any txt files
file_set = set()
for file in os.listdir():
    if file.endswith(".txt"):
        file_set.add(file)
size = len(file_set)

start = time.time()
for file in file_set:
    encrypt_file_two(file, decr_key_two)
print(f"Time to encrypt {size} files via Twofish algorithm: {str(time.time() - start)} seconds")

start = time.time()
for file in file_set:
    decrypt_file_two(file, decr_key_two)
print(f"Time to decrypt {size} files via Twofish algorithm: {str(time.time() - start)} seconds")

start = time.time()
for file in file_set:
    encrypt_file_blow(decr_key_blow, file, init_vect)
print(f"Time to encrypt {size} files via Blowfish algorithm: {str(time.time() - start)} seconds")

start = time.time()
for file in file_set:
    decrypt_file_blow(decr_key_blow, file, init_vect)
print(f"Time to decrypt {size} files via Blowfish algorithm: {str(time.time() - start)} seconds")
