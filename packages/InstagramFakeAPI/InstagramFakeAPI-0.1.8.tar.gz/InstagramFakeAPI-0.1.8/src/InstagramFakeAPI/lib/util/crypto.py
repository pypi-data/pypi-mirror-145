import io
import base64
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_v1_5
import struct

from Cryptodome.PublicKey import RSA


class Crypto:
    def __init__(self):
        pass

    @staticmethod
    def jazoest(phone_id) -> str:
        return f"2{sum(ord(i) for i in phone_id)}"

    @staticmethod
    def encrypt_password(password: str, pub_key: str, key_id: int, cur_time: int) -> str:
        # Key and IV for AES encryption
        rand_key = get_random_bytes(32)
        iv = get_random_bytes(12)

        # Encrypt AES key with Instagram's RSA public key
        pubkey_bytes = base64.b64decode(pub_key)
        pubkey = RSA.import_key(pubkey_bytes)
        cipher_rsa = PKCS1_v1_5.new(pubkey)
        encrypted_rand_key = cipher_rsa.encrypt(rand_key)

        cipher_aes = AES.new(rand_key, AES.MODE_GCM, nonce=iv)
        # Add the current time to the additional authenticated data (AAD) section
        cipher_aes.update(str(cur_time).encode("utf-8"))
        # Encrypt the password and get the AES MAC auth tag
        encrypted_passwd, auth_tag = cipher_aes.encrypt_and_digest(password.encode("utf-8"))

        buf = io.BytesIO()
        # 1 is presumably the version
        buf.write(bytes([1, int(key_id)]))
        buf.write(iv)
        # Length of the encrypted AES key as a little-endian 16-bit int
        buf.write(struct.pack("<h", len(encrypted_rand_key)))
        buf.write(encrypted_rand_key)
        buf.write(auth_tag)
        buf.write(encrypted_passwd)
        encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"#PWD_INSTAGRAM:4:{cur_time}:{encoded}"
