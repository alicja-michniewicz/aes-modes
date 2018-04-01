# Created by Alicja Michniewicz - 208822
import base64, jks, pyaes, random, sys, textwrap
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def AESTool(aesMode, keytool, keyId, action, filename):
	key = readKeystore(keytool, keyId)
	print(type(key))
	if key is None:
		print("Invalid keyId!")
	else:
		if (aesMode == "CBC" or aesMode == "OFB" or aesMode == "CTR"):
			if (action == "Encrypt"):
				Encrypt(filename, chooseMode(aesMode, key))
			elif (action == "Decrypt"):
				Decrypt(filename, chooseMode(aesMode, key))

# AES mode has to be re-initialised for each Enc/Dec operation
def chooseMode(mode, key):
	if (mode == "CBC"):
		_mode = pyaes.AESModeOfOperationCBC(key)
	elif (mode == "OFB"):
		_mode = pyaes.AESModeOfOperationOFB(key)
	elif (mode == "CTR"):
		_mode = pyaes.AESModeOfOperationCTR(key)
	return _mode

# AES key needs to be exactly 16, 24 or 32 bytes
def readKeystore(keytool, keyId):
	ks = jks.KeyStore.load(keytool, "keystore")
	for alias, pk in ks.private_keys.items():
		if (alias == keyId):
			print("Private key: %s" % "\r\n".join(textwrap.wrap(base64.b64encode(pk.pkey_pkcs8[:16]).decode('ascii'), 64)))
			return pk.pkey_pkcs8[:16] # 16 bytes key

# "a" permission enables file editing (Encrypt may be called multiple times).
# "w" would truncate the file every time it's called
def Encrypt(filename, aesMode):
	file_in = open(filename, 'r')
	file_out = open('encrypted.txt', 'a+b')
	pyaes.encrypt_stream(aesMode, file_in, file_out)
	file_in.close()
	file_out.close()

def Decrypt(filename, aesMode):
	file_in = open(filename, 'r+b')
	file_out = open('decrypted.txt', 'w+b')

	pyaes.decrypt_stream(aesMode, file_in, file_out)
	file_in.close()
	file_out.close()

#########################################################################

action = input('Encrypt or Decrypt?\n\t')
aesMode = input('CBC, OFB or CTR?\n\t')

filenames = []
encryptionMode = input('oracle or challenge?\n\t')

if (action == 'Encrypt' and encryptionMode == 'oracle'):
	filesCount = input('how many files?\n\t')

	# Truncate encrypted.txt file before next encryption
	encrypted = open('encrypted.txt', 'w+')
	encrypted.close()

	for _ in range(0, int(filesCount)):
		Tk().withdraw()
		filename = askopenfilename()
		filenames.append(filename)

	for j in range(0, len(filenames)):
		AESTool(aesMode, "keystore.jks", "", action, filenames[j])

elif (action == 'Encrypt' and encryptionMode == 'challenge'):
	for _ in range(2):
		Tk().withdraw()
		filename = askopenfilename()
		filenames.append(filename)

	AESTool(aesMode, "keystore.jks", "", action, random.choice(filenames))

elif (action == 'Decrypt'):
	AESTool(aesMode, "keystore.jks", "keystore", action, 'encrypted.txt')