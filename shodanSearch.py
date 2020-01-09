#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
author: @mezdanak, modzero AG, https://www.modzero.ch, @mod0
usage: $ python shodanSearch.py -s 'shodanSearchTerm' -o results.txt

This tool can be used to retrieve IP-address:port combinations from a shodan.io search (argument -s). 
Results will be stored in the file specified (argument -o).
'''
import sys
import argparse

try:
	import shodan
except ImportError:
	print('[-] Error: Cannot import \'shodan\', run $ sudo pip3 install shodan')
	sys.exit()

if __name__ == '__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-s', '--search', type=str, help='search query', default='tornado',
							action='store', required=True)
	argparser.add_argument('-o', '--output', type=str, help='output filename', default='out.txt',
							action='store', required=True)
	args = argparser.parse_args()
	try:
		shodan_api_key = input('[+] Input: Enter your shodan.io API key: ')
		if len(shodan_api_key) != 32:
			print('[-] Error: Invalid shodan.io API key.')
			sys.exit()
		else:
			api = shodan.Shodan(shodan_api_key)
		results = api.search(args.search)
		print(results)
		results_total = results['total']
		pages = int(round(results_total/100)) + 1
		print('[+] Info: Total {0} results.'.format(str(results['total'])))
		perform_query = input('[+] Input: Do you want to perform the query? This will cost you {0} shodan Query Credits [Y/N]: '.format(pages))
		if perform_query.upper() == 'Y':
			print('[+] Info: Fetching results from {0} pages. Results will be written to {1}. Shodan.io API calls are time throttled 1/sec.'.format(pages, args.output))
			for x in range(0,pages):
				print('[+] Info: Fetching page {0}'.format(x))
				results_page = api.search(args.search, page=x)
				try:
					with open(args.output, 'a') as result_file:
						try:
							for item in results_page['matches']:
								result_file.write(item['ip_str'] + ':' + str(item['port']) + '\n') # Configure your prefered output format here!
						except KeyError as e:
							print('[-] Error: Please check your defined output format. {0} not found.'.format(e))
							sys.exit()
				except IOError:
					print('[-] Error: Cannot open {0}'.format(args.output))
					sys.exit()
			print('[+] Info: Finished.\n')
		else:
			print('[+] Info: Quitting program.')
			sys.exit()
	except shodan.APIError as e:
		print('[-] Error: {0}'.format(e))
