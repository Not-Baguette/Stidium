from cryptography.fernet import Fernet


def encrypt_header(file_path, key):
    # Read the first few bytes of the file (which represent the header)
    with open(file_path, 'rb+') as file:
        header = file.read(8)
        fernet = Fernet(key)
        encrypted_header = fernet.encrypt(header)
        # file.seek to the start of the file to overwrite the encrypted header with the decrypted header
        file.seek(0)
        file.write(encrypted_header)


def decrypt_header(file_path, key):
    # Read the first few bytes of the file (which represent the encrypted header)
    with open(file_path, 'rb+') as file:
        encrypted_header = file.read(8)
        fernet = Fernet(key)
        header = fernet.decrypt(encrypted_header)
        # file.seek to the start of the file to overwrite the encrypted header with the decrypted header
        file.seek(0)
        file.write(header)


def main():
    # P.S. Don't forget to use multithreading if you want to implement it
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
