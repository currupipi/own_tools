#!/usr/bin/env python
#Script to encrypt/decrypt a directory or folder with a pasword
#WARNING: Needs Crypto

from Crypto.Cipher import AES
import hashlib
import random
import sys
import os
import argparse
import getpass


def file_exists(file_or_dir_name):
	"""Checks file exists in path"""
	if not os.path.exists(file_or_dir_name):
		print '[!] ERROR: File or directory {} does not exist'.format(file_or_dir_name)
		sys.exit(10)
	return 0

def get_password():
	"""Prompts user for password"""
	try:
		password = getpass.getpass('passwd: ')
	except Exception as msg:
		print '[!] ERROR: {} Can not get password from user'.format(msg)
		sys.exit(10)
	return password

def gen_key_from_password(password):
	"""Generates a 32 bit key long"""
	try:
		key = hashlib.sha256(password).digest()
	except Exception as msg:
		print '[!] ERROR: {} Can not generate key from password'.format(msg)
		sys.exit(11)
	return key

def encrypt(file_name, password, chunksize=64*1024):
	"""Encrypts a file generating a key from a password"""
	iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	key = gen_key_from_password(password)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(file_name)

    with open(file_name, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
	


def decrypt(path, password):
	"""Decrypts a file"""



# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m' # blue

#Argument parsing
help_message = ("USAGE:\n" +
                "The fortify.py script encrypts and decrypts a file or directory\n" +
				"Example :\n" +
				"fortify.py -e <path2file>  -p <password>") 
parser = argparse.ArgumentParser(usage=help_message, description='Encrypt/decrypt a file or dir')
parser.add_argument('-e', help='Path to the file or directory', default=False)
parser.add_argument('-p', help='Password of the encrypt/decrypt', default=False)
args = parser.parse_args()


if __name__ == "__main__":

	hosts = set(args.t)
	ports = set(args.p)
	timeout = float(args.s)

	#Loop through the hosts
	for host in hosts:
		print G + '[+] INFO: Scanning host {}'.format(host) + W
		#Loop through the ports
		for port in ports:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			except socket.error as msg:
				print R + '[-] ERROR: Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1] + W
				sys.exit(69)

			s.settimeout(timeout)

			try:	
				s.connect((host,int(port)))
				print G + "\t[+] INFO: Port {} is open".format(port) + W

			except Exception as msg:
			#except socket.error, exc:
				print R + "\t[!] WARNING: {} Can not connect to port {}".format(msg, port) + W

			s.close()

