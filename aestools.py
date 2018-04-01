import sys
from argparse import *

import numpy

from aes_scheme import AES

parser = ArgumentParser()

parser.add_argument('-k', '--keystore', nargs=None, type=str, help='path to jks keystore', required=True)
parser.add_argument('-a', '--alias', nargs=None, type=str, help='key alias', required=True)
parser.add_argument('-c', '--config', nargs=None, help='keystore config', required=True)

parser.add_argument('-b', '--block', nargs=None, help='block cipher mode of encryption', choices=["CBC", "OFB", "CTR"],
                    default="CBC")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-ch', '--challenge', action="store_true")
subgroup = group.add_mutually_exclusive_group(required=True)
subgroup.add_argument('-e', '--encrypt', action="store_true")
subgroup.add_argument('-d', '--decrypt', action="store_false")
parser.add_argument('-m', '--mode', help='mode', nargs=None, choices=["oracle", "challenger"], default="oracle")
parser.add_argument('-i', '--incremental', help='toggle unsafe IV mode', action="store_true", required=False)
parser.add_argument('-f', '--files', nargs="*", help='files', required=True)

args = parser.parse_args()

print(args)

AES = AES(args.block, numpy.random.bytes(16))


if args.challenge:
    if len(args.files) != 2:
        raise ArgumentError("Wrong number of challenge messages")

    filename = numpy.random.choice(args.files)

    AES.encrypt(filename, "challenge.txt")

if args.encrypt:
    for f in args.files:
        AES.encrypt(f, f + '-encrypted')
else:
    for f in args.files:
        AES.decrypt(f, f + '-decrypted')

# AES.decrypt(sys.stdin.buffer, sys.stdout.buffer)
