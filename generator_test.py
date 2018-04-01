import unittest

from aes_scheme import IncrementalIVGenerator


class TestIncrementalIvGenerator(unittest.TestCase):

    def test_givenIV_nextIncremented(self):
        gen = IncrementalIVGenerator()
        iv = int.from_bytes(gen.next_iv(), 'big')
        next_iv = int.from_bytes(gen.next_iv(), 'big')

        print(iv)
        print(next_iv)

        self.assertEqual(next_iv, iv + 1)


if __name__ == '__main__':
    unittest.main()
