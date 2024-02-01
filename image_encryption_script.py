from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image
import os

def pad(data):
    # Padding the data to make its length a multiple of 16
    block_size = 16
    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length] * padding_length)

def unpad(data):
    # Remove padding from the data
    padding_length = data[-1]
    return data[:-padding_length]

def encrypt_image(input_path, output_path, key):
    with open(input_path, 'rb') as file:
        plaintext = file.read()

    # Pad the plaintext before encryption
    plaintext = pad(plaintext)

    # Generate an initialization vector (IV)
    iv = os.urandom(16)

    # Create an AES cipher object
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the plaintext
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Write the IV and ciphertext to the output file
    with open(output_path, 'wb') as file:
        file.write(iv + ciphertext)

def decrypt_image(input_path, output_path, key):
    with open(input_path, 'rb') as file:
        data = file.read()

    # Extract IV and ciphertext
    iv = data[:16]
    ciphertext = data[16:]

    # Create an AES cipher object
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext and unpad the result
    plaintext = unpad(decryptor.update(ciphertext) + decryptor.finalize())

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as file:
        file.write(plaintext)

# Example usage
path = os.getcwd()
input_image_path = path+"/image_folder/"+(input("input_image:\n"))
encrypted_image_path = path+'/encrypted_image.enc'
decrypted_image_path = path+'decrypted_image.jpg'

# Replace 'your_secret_key' with a 16-byte (128-bit) key
secret_key = b'your16bytekey123'

# Encrypt the image
encrypt_image(input_image_path, encrypted_image_path, secret_key)

# Decrypt the image
decrypt_image(encrypted_image_path, decrypted_image_path, secret_key)
