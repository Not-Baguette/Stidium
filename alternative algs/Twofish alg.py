from twofish import Twofish

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
