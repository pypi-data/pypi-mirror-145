import os
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

class Keystore:
    """
    Stores RSA private and public keys for SSH to containers
    """
    def __init__(self):

        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )

        self.key = key

        self.private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.TraditionalOpenSSL,
            crypto_serialization.NoEncryption()
        )

        self.public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )

    def create_private_key_file(self):
        with open('.oompa_key', 'wb') as private_key_file:
            private_key_file.write(self.private_key)
            private_key_file.close()
        os.chmod('.oompa_key', 0o600)

    def create_public_key_file(self):
        with open('.oompa_key.pub', 'wb') as public_key_file:
            public_key_file.write(self.public_key)
            public_key_file.close()
        os.chmod('.oompa_key.pub', 0o644)
