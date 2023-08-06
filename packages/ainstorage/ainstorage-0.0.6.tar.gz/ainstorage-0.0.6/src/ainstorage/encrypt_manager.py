from Crypto.Cipher import AES
import secrets

# encrypt functions
def generate_secret_key():
    secret_key = '0'

    while secret_key.startswith('0'):
        secret_key = secrets.token_bytes(16).hex()
    
    return secret_key

def encrypt_file(file, secret_key):
    aes_cipher = AES.new(secret_key.encode(), AES.MODE_GCM)
    nonce = aes_cipher.nonce
    file_data = file.read()
    cipher_text, tag = aes_cipher.encrypt_and_digest(file_data)

    return { 'nonce': nonce, 'tag': tag, 'cipher_text': cipher_text }

def generate_re_enc_key():
    print('TBD')

def encrypt_re_enc_key():
    print('TBD')

# decrypt functions
def decrypt_file(nonce, tag, cipher_text, secret_key):
    aes_cipher = AES.new(secret_key.encode(), AES.MODE_GCM, nonce)
    data = aes_cipher.decrypt_and_verify(cipher_text, tag)

    return data