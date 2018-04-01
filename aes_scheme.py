import io

import numpy
import pyaes
from pyaes import PADDING_NONE


class RandomIVGenerator:

    def __init__(self) -> None:
        super().__init__()

    def next_iv(self):
        return numpy.random.bytes(16)


class IncrementalIVGenerator:

    def __init__(self) -> None:
        super().__init__()
        self.iv = numpy.random.bytes(16)

    def next_iv(self):
        iv_value = int.from_bytes(self.iv, 'big')
        iv_value += 1

        self.iv = iv_value.to_bytes(len(self.iv), 'big')

        return self.iv


class AES:

    def __init__(self, mode, key, gen=RandomIVGenerator()):
        super().__init__()
        self.mode = mode
        self.key = key
        self.gen = gen

    def encrypt(self, filename, savename):
        file_in = open(filename, 'r+b')
        file_out = open(savename, 'w+b')

        pyaes.encrypt_stream(self.init_mode(), file_in, file_out)

        file_in.close()
        file_out.close()

    def decrypt(self, filename, savename):
        file_in = open(filename, 'r+b')
        file_out = open(savename, 'w+b')

        pyaes.decrypt_stream(self.init_mode().encrypt(), file_in, file_out)

        file_in.close()
        file_out.close()

    # AES mode has to be re-initialised for each Enc/Dec operation
    def init_mode(self):
        if self.mode == "CBC":
            return pyaes.AESModeOfOperationCBC(self.key, self.gen.next_iv())
        elif self.mode == "OFB":
            return pyaes.AESModeOfOperationOFB(self.key, self.gen.next_iv())
        elif self.mode == "CTR":
            counter = pyaes.Counter(int.from_bytes(self.gen.next_iv(), 'big'))
            return pyaes.AESModeOfOperationCTR(self.key, counter)

        raise AttributeError("Mode " + self.mode + " unsupported")
