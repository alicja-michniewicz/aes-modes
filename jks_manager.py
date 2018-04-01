import base64
import textwrap

from jks import jks


class Keystore:

    def __init__(self, keystore, password) -> None:
        super().__init__()
        self.ks = jks.KeyStore.load(keystore, password)

    def load_key(self, alias):
        pk = self.ks[alias]
        print("Private key: %s" % "\r\n".join(
            textwrap.wrap(base64.b64encode(pk.pkey_pkcs8[:16]).decode('ascii'), 64)))

        return pk.pkey_pkcs8[:16]  # 16 bytes key
