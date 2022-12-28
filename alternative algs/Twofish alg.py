from twofish import Twofish
import random
import string
import os

def encrypt_file_two(file_path, key):
    # Set block size to 16 bytes (128 bits)
    block_size = 16

    # Read the input file in binary mode
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # pad
    if len(plaintext) % block_size:
        padded_plaintext = str(plaintext + b"%" * (block_size - len(plaintext) % block_size)).encode("utf-8")
    else:
        padded_plaintext = plaintext

    cipher = Twofish(str.encode(key))
    ciphertext = b""
    for i in range(int(len(padded_plaintext) / block_size)):
        ciphertext += cipher.encrypt(padded_plaintext[i * block_size:(i + 1) * block_size])

    with open(file_path + ".enc", "wb") as f:
        f.write(ciphertext)

    os.remove(file_path)


def decrypt_file_two(file_path, key):
    file_path += ".enc"
    block_size = 16

    # Read the input file in binary mode
    with open(file_path, "rb") as f:
        ciphertext = f.read()

    # Create the Twofish cipher object
    cipher = Twofish(str.encode(key))

    plaintext = b""
    try:
        for i in range(int(len(ciphertext) / block_size)):
            plaintext += cipher.decrypt(ciphertext[i * block_size:(i + 1) * block_size])

        # Write the plaintext to the output file in binary mode
        with open(file_path[:-4], "wb") as f:
            f.write(plaintext)
    except Exception:  # NOQA
        cipher = Twofish(str.encode("utf-8"))

        for i in range(int(len(ciphertext) / block_size)):
            plaintext += cipher.decrypt(ciphertext[i * block_size:(i + 1) * block_size])

        # Write the plaintext to the output file in binary mode
        with open(file_path[:-4], "wb") as f:
            f.write(plaintext)

    # Remove the original input file
    os.remove(file_path)

# Set password as 32 letter string (why systemrandom? https://stackoverflow.com/a/23728630/2213647)
decr_key_two = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
    
# Encrypt
encrypt_file_two(file, decr_key_two)

# Decrypt
decrypt_file_two(file, decr_key_two)
