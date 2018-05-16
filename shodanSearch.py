#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
author: @mezdanak, modzero AG, https://www.modzero.ch, @mod0
'''
import sys
import urllib2
import socket
import httplib
import argparse

try:
	import shodan
except ImportError:
	print "[-] Error: Cannot import 'shodan', run $ sudo pip install shodan"
	sys.exit()

if __name__ == '__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-s', '--search', type=str, help='search query', default='foo',
							action='store')
	argparser.add_argument('-f', '--file', type=str, help='output filename', default='out.txt',
							action='store')
	args = argparser.parse_args()
	try:
		shodan_api_key = raw_input('[+] Input: Enter your shodan.io API key: ')
		if len(shodan_api_key) != 32:
			print '[-] Error: Invalid shodan.io API key.'
			sys.exit()
		else:
			api = shodan.Shodan(shodan_api_key)
		results = api.search(args.search)
		results_total = results['total']
		pages = int(round(results_total/100)) + 1
		print '[+] Info: Total %s results.' %str(results['total'])
		perform_query = raw_input('[+] Input: Do you want to perform the query? This will cost you %i shodan Query Credits [Y/N]: ' %pages)
		if perform_query.upper() == 'Y':
			print "[+] Info: Fetching results from %s pages. Results will be written to %s. Shodan.io API calls are time throttled 1/sec." %(pages, args.file)
			for x in range(0,pages):
				print '[+] Info: Fetching page %s' %x
				results_page = api.search(args.search, page=x)
				try:
					with open(args.file, 'a') as result_file:
						try:
							for item in results_page['matches']:
								result_file.write(item['ip_str'] + ':' + str(item['port']) + '\n') # Configure your prefered output format here!
						except KeyError, e:
							print '[-] Error: Please check your defined output format. %s not found.' %e
							sys.exit()
				except IOError:
					print '[-] Error: Cannot open %s' %(args.file)
					sys.exit()
			print '[+] Info: Finished.\n'
		else:
			print '[+] Info: Quitting program.'
			sys.exit()
	except shodan.APIError, e:
		print '[-] Error: %s' %e
