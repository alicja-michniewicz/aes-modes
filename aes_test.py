import io
import sys
import unittest

import numpy
import pyaes

from aes_scheme import AES, Encrypt, chooseMode, Decrypt


class TestIncrementalIvGenerator(unittest.TestCase):

    def test_cbc_encrypt_decrypt(self):
        pass

if __name__ == '__main__':
    unittest.main()
