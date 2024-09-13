import binascii
import hashlib
import os

from app.errors import WrongPassword


def hash_password(password: str) -> str:
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")

    password_hash = hashlib.pbkdf2_hmac(
        "sha512", password.encode("utf-8"), salt, 100000
    )

    password_hash = binascii.hexlify(password_hash)

    return (salt + password_hash).decode("ascii")


def check_password(password: str, password_hash: str) -> None:
    salt = password_hash[:64]
    password_hash = password_hash[64:]

    current_password_hash = hashlib.pbkdf2_hmac(
        "sha512", password.encode("utf-8"), salt.encode("ascii"), 100000
    )

    current_password_hash = binascii.hexlify(current_password_hash).decode(
        "ascii"
    )

    if not current_password_hash == password_hash:
        raise WrongPassword
