from Crypto.Cipher import AES
import base64
import Tkinter as tk
import hashlib


def encrypt(data, key):
    """
    :param data: a string to encrypt
    :param key: a key
    :return: encrypted string
    """

    # set block size
    block_size = 32

    # add padding
    padding = '{'
    pad = lambda s: s + (block_size - len(s) % block_size) * padding

    # use base64 encoding
    encode_aes = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    # encrypt
    cipher = AES.new(key)

    # encode
    encoded = encode_aes(cipher, data)

    return encoded


def decrypt(encrypted_string, key):
    padding = '{'
    cipher = AES.new(key)
    decoded = cipher.decrypt(base64.b64decode(encrypted_string)).rstrip(padding)
    return decoded


def copy_to_clipboard(text):
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.destroy()


def clean_clipboard():
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.destroy()


def hash_password(password):
    return hashlib.md5(password).hexdigest()
