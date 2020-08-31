import binascii
import hashlib
import urllib.request
import re


def hash_simple(key: bytes, string: bytes, algorithm: str = 'sha512', length: int = 20):
    cipher = int(binascii.hexlify(hashlib.pbkdf2_hmac(algorithm, string, key, 100000)), 16) % (10 ** length)
    return cipher


def check_online_version(url: str, current_version: str) -> str:

    try:
        contents = urllib.request.urlopen(url).read()
        contents = contents.decode()
        online_version = re.findall(r"__version__[ =0-9.a-z\'\"]+\n", contents)[0]
        online_version = re.sub(r'(__version__ *= *)', '', online_version).replace('"', '').replace("'", '')
    except Exception:
        online_version = ''

    return online_version.strip()
