from Crypto.Cipher import AES
import base64
import Tkinter as tk
import hashlib
import random

def encrypt(privateInfo,key):
    BLOCK_SIZE = 32
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s)%BLOCK_SIZE)*PADDING
    encode_aes = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = key
    cipher = AES.new(secret)
    encoded = encode_aes(cipher, privateInfo)
    return encoded


def decrypt(encrypted_string, key):
    PADDING = '{'
    decode_aes = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    cipher = AES.new(key)
    decoded = decode_aes(cipher, encrypted_string)
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
