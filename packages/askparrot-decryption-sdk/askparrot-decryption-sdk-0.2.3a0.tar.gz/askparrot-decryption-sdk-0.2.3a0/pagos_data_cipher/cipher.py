from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import copy
import binascii
import json
import datetime
from time import gmtime, strftime
from Crypto.Protocol.KDF import scrypt

class pagos_data_cipher:
    """
    Cipher to process specific data object with payload
    """
    PAYLOAD_FIELD = 'payload'
    BLOCK_SIZE = 16 # 128
    SALT_FIELD = 'encrypted_at'

    def __init__(self, key):
        self.key = key

    def generate_key(self, gen_key, salt):
        key = scrypt(gen_key.encode('utf-8'), salt.encode('utf-8'), 16, N=2**14, r=8, p=1) 
        return key

    """
    Object encryption (for test purposes only)
    """
    def encrypt_object(self, data):
        encrypted_data = copy.deepcopy(data)
        encrypted_at = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        key = self.generate_key(self.key, encrypted_at)
        cipher = AES.new(key, AES.MODE_ECB)

        if (self.PAYLOAD_FIELD in encrypted_data):
            encrypted_field = cipher.encrypt(pad(json.dumps(encrypted_data[self.PAYLOAD_FIELD]).encode('utf8'), self.BLOCK_SIZE))
            encrypted_data[self.PAYLOAD_FIELD] = binascii.hexlify(encrypted_field).decode()

        encrypted_data[self.SALT_FIELD] = encrypted_at
        return encrypted_data

    """
    Object decryption decrypts payload field
    """
    def decrypt_object(self, data):

        decrypted_data = copy.deepcopy(data)
        encrypted_at = data[self.SALT_FIELD]
        key = self.generate_key(self.key, encrypted_at)
        cipher = AES.new(key, AES.MODE_ECB)

        if (self.PAYLOAD_FIELD in decrypted_data):
            decrypted_field = unpad(cipher.decrypt(binascii.unhexlify(decrypted_data[self.PAYLOAD_FIELD])), self.BLOCK_SIZE)
            decrypted_data.update(json.loads(decrypted_field.decode()))
            del decrypted_data[self.PAYLOAD_FIELD]

        return decrypted_data