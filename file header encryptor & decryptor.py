from cryptography.fernet import Fernet


def encrypt_header(file_path, key):
    # Open the file in binary mode
    with open(file_path, 'rb+') as file:
        # Read the first few bytes of the file, which represent the header
        header = file.read(8)
        # Generate a Fernet object using the key
        fernet = Fernet(key)
        # Encrypt the header
        encrypted_header = fernet.encrypt(header)
        # Seek to the beginning of the file and overwrite the header with the encrypted header
        file.seek(0)
        file.write(encrypted_header)


def decrypt_header(file_path, key):
    with open(file_path, 'rb+') as file:
        # Read the first few bytes of the file (which represent the encrypted header)
        encrypted_header = file.read(8)
        fernet = Fernet(key)
        header = fernet.decrypt(encrypted_header)
        # file.seek to the start of the file to overwrite the encrypted header with the decrypted header
        file.seek(0)
        file.write(header)


def main():
    file_path = ("/path/to/file.txt",)
    decrypt_key = Fernet.generate_key()

    # Encrypt
    for i in file_path:
        encrypt_header(i, decrypt_key)

    # Decrypt
    for i in file_path:
        decrypt_header(i, decrypt_key)


if __name__ == "__main__":
    main()
