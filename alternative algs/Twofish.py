from twofish import Twofish
import random
import string
import os


def encrypt_file_two(input_file, key):
    # Set block size to 16 bytes (128 bits)
    block_size = 16

    with open(input_file, "r") as f:
        plaintext = f.read()

    if len(plaintext) % block_size:
        padded_plaintext = str(plaintext + "%" * (block_size - len(plaintext) % block_size)).encode("utf-8")
    else:
        padded_plaintext = plaintext.encode("utf-8")

    cipher = Twofish(str.encode(key))
    ciphertext = b""
    for i in range(int(len(padded_plaintext) / block_size)):
        ciphertext += cipher.encrypt(padded_plaintext[i * block_size:(i + 1) * block_size])

    with open(input_file + ".enc", "wb") as f:
        f.write(ciphertext)

    os.remove(input_file)


def decrypt_file_two(output_file, key):
    output_file += ".enc"
    block_size = 16

    with open(output_file, "rb") as f:
        ciphertext = f.read()

    cipher = Twofish(str.encode(key))

    plaintext = b""
    for i in range(int(len(ciphertext) / block_size)):
        plaintext += cipher.decrypt(ciphertext[i * block_size:(i + 1) * block_size])
    stripped_plaintext = plaintext.decode("utf-8").strip("%")

    with open(output_file[:-4], "wb") as f:
        f.write(stripped_plaintext.encode("utf-8"))

    os.remove(output_file)


# Set password as 32 letter string (why systemrandom? https://stackoverflow.com/a/23728630/2213647)
decr_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))

# Encrypt a file
encrypt_file_two("test.txt", decr_key)

# Decrypt the encrypted file
decrypt_file_two("test.txt", decr_key)
