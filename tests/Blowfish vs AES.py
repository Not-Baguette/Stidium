from Cryptodome.Cipher import Blowfish
from Cryptodome.Random import get_random_bytes
from cryptography.fernet import Fernet
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


def try_func(file_path, key):
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Generate a Fernet object using the key and encrypt the data
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)

        # Write the encrypted data to a new file
        with open(file_path + ".enc", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        os.remove(file_path)
    except FileNotFoundError:
        pass


def try_func_decr(file_path, key):
    try:
        with open(file_path + ".enc", "rb") as encrypted_file:
            # Read the encrypted data
            encrypted_data = encrypted_file.read()

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        # Write the decrypted data to a new file
        with open(file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)

        os.remove(file_path + ".enc")
    except FileNotFoundError:
        pass


# check current directory for any txt files
file_set = set()
for file in os.listdir():
    if file.endswith(".txt"):
        file_set.add(file)


start = time.time()
for file in file_set:
    encrypt_file(enc_key, file, init_vect)
print("Time to encrypt via Blowfish algorithm: " + str(time.time() - start))

start = time.time()
for file in file_set:
    decrypt_file(enc_key, file, init_vect)
print("Time to decrypt via Blowfish algorithm: " + str(time.time() - start))

start = time.time()
decr_key = Fernet.generate_key()
for file in file_set:
    try_func(file, decr_key)
print("Time to encrypt via AES algorithm: " + str(time.time() - start))

start = time.time()
for file in file_set:
    try_func_decr(file, decr_key)
print("Time to decrypt via AES algorithm: " + str(time.time() - start))
