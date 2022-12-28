from Crypto.Cipher import Twofish
import os

def encrypt_file(input_file, key):
    # Create the output file name by appending '.enc' to the input file name
    output_file = input_file + '.enc'

    # Open the input and output files
    with open(input_file, 'rb') as in_file, open(output_file, 'wb') as out_file:
        # Create a Twofish cipher object
        cipher = Twofish.new(key, Twofish.MODE_CFB)

        # Read the input file in blocks of 128 bytes
        while True:
            block = in_file.read(128)
            if len(block) == 0:
                break
            elif len(block) % 16 != 0:
                # If the block is not a multiple of 16 bytes, pad it with zeros
                block += b'\x00' * (16 - len(block) % 16)
            
            # Write the encrypted block to the output file
            out_file.write(cipher.encrypt(block))

def decrypt_file(output_file, key):
    input_file = output_file + '.enc'

    # Open the input and output files
    with open(input_file, 'rb') as in_file, open(output_file, 'wb') as out_file:
        # Create a Twofish cipher object
        cipher = Twofish.new(key, Twofish.MODE_CFB)

        # Read the input file in blocks of 128 bytes
        while True:
            block = in_file.read(128)
            if len(block) == 0:
                break

            # Write the decrypted block to the output file
            out_file.write(cipher.decrypt(block))

    
# Define the key and input file name as strings
key = os.urandom(32)
input_file = 'input.txt'

# Encrypt the file
encrypt_file(input_file, key)

# Decrypt the file
decrypt_file(input_file, key)
