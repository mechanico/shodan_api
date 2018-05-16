# shodan_api
<b>shodanSearch.py</b> should help you to export the results of a shodan.io search in a text file. The export format can be customized, depending on your requirements. 

# Requirements
You will first need to install the shodan library by running:

~~~
$ sudo pip install shodan
~~~

You will also need a valid shodan.io account. Get your shodan.io API key from https://account.shodan.io

# Usage
Options:

* -h : Show help 
* -s : Your search query e.g. 'tornadoserver title:home'
* -f : Your output file e.g. output.txt

~~~
$ python shodanSearch.py -h
usage: shodanSearch.py [-h] [-s SEARCH] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -s, --search          search query
  -f, --file            output filename
~~~

The default output format of the results will be:

* IP_adress:port
  * 192.168.100.1:8000

If you want to customize the output format edit the following line in <b>shodanSearch.py</b>:

~~~
result_file.write(item['ip_str'] + ':' + str(item['port']) + '\n') # Configure your prefered output format here!
~~~


# Example

~~~
$ python shodanSearch.py -s 'tornadoserver title:home' -f vulnerable_jupyters.txt
[+] Input: Enter your shodan.io API key: --YOUR_SECRET_API_KEY--
[+] Info: Total 494 results.
[+] Input: Do you want to perform the query? This will cost you 5 shodan Query Credits [Y/N]: y
[+] Info: Fetching results from 5 pages. Results will be written to vulnerable_jupyters.txt. Shodan.io API calls are time throttled 1/sec.
[+] Info: Fetching page 0
[+] Info: Fetching page 1
[+] Info: Fetching page 2
[+] Info: Fetching page 3
[+] Info: Fetching page 4
[+] Info: Finished.
~~~
