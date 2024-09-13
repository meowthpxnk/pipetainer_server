import os
import shutil
from pathlib import Path

import _base_script
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from app import settings


output_file = Path(settings.jwt.private_key_path)

if os.path.exists(output_file.parent):
    shutil.rmtree(output_file.parent)

output_file.parent.mkdir(exist_ok=True, parents=True)


def utf8(s: bytes):
    return str(s, "utf-8")


private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=4096, backend=default_backend()
)
public_key = private_key.public_key()


private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

with open(settings.jwt.private_key_path, "wb") as f:
    f.write(private_pem)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
with open(settings.jwt.public_key_path, "wb") as f:
    f.write(public_pem)
