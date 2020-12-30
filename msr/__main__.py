from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed, ProcessPoolExecutor
import semver, validators, os, sys, requests
from prettytable import PrettyTable
from typing import List
import time

#no duplicate table entries
explored_set, in_table_set = set(), set()

# reads filename and return list of urls 
def read_file(filename: str) -> List[str]:
	file = open(filename, 'r')
	lines = file.readlines() 
	urls = [""] * len(lines)
	for line_number, line in enumerate(lines):
		urls[line_number] = line.strip() #strip new line from each line
	return urls

# returns byte size of response (request object)
def get_body_size(resp) -> int:
	if 'content-length' in resp.headers:
		return resp.headers['content-length']
	return len(resp.content)

# write the "write_obj" to the XDG_CONFIG_HOME file
def write_to_register(write_obj: str):
	f = open("msr/XDG_CONFIG_HOME", "a")
	f.write(write_obj)
	f.close()

# get load time and body_size given request response
def get_register_info(url: str, resp) -> str:
	load_time = resp.elapsed.total_seconds()
	body_size = get_body_size(resp)
	return url + ', ' + str(body_size) + ', ' + str(load_time) + '\n'

# version prints a semver string to STDOUT 
def version():
	print(semver.VersionInfo.parse("1.0.1"))

# register returns validity of url (0 if valid, -1 if invalid)
def check_validity(url: str) -> int: 
	try:
		status=validators.url(url)
	except:
		return -1
	status = 0 if status else -1
	return status

# add_to_registry inserts valid urls into database
def add_to_registry(url: str) -> int:
	if check_validity(url) == 0:
		write_to_register(url + '\n')
		return 0
	return -1

# add multiple urls to registry at a time 
def blast(urls: List[str], max_workers=8):
	with FuturesSession(executor=ProcessPoolExecutor(max_workers=max_workers)) as session:
		futures = [session.get(url) for url in urls]
		for future in as_completed(futures):
			try:
				resp = future.result()
				write_to_register(get_register_info(resp.request.url, resp))
			except:
				print("invalid url")

# completes register and fills in info for each url
def make_register():
	register_urls = read_file('msr/XDG_CONFIG_HOME')
	open('XDG_CONFIG_HOME', 'w').close() 
	need_to_process = []
	for url in  register_urls:
		if len(url.split(',')) == 1:
			 if url not in explored_set:
			 	explored_set.add(url)
			 	need_to_process.append(url)
		else:
			write_to_register(url + '\n') if url[-1] != '\n' else write_to_register(url)
	blast(need_to_process, max_workers=35)

# generate a pretty-printed table given headers and columns 
def generate_table(header_one: str, header_two: str, col_one: int, col_two: int):
	register_urls = read_file('msr/XDG_CONFIG_HOME')
	table = PrettyTable([header_one, header_two])
	for url in register_urls:
		url_split = url.split(',')
		if len(url_split) == 3 and url_split[0] not in in_table_set:
			in_table_set.add(url_split[0])
			table.add_row([url_split[col_one], url_split[col_two]])
	print(table)

# displays a pretty-printed table of URL and Body Size
def measure():
	make_register()
	generate_table('URL', 'Size', 0, 1)

# displays a pretty-printed table of URL and Page Load Time
def race():
	make_register()
	generate_table('URL', 'Page Load Time', 0, 2)

# process command line args
def main():
	functionality_set = {"version", "measure", "race"}
	if len(sys.argv) == 3 and sys.argv[1] == "register":
		return add_to_registry(sys.argv[2])
	elif len(sys.argv) == 2 and sys.argv[1] in functionality_set:
		if sys.argv[1] == "version":
			version()
		elif sys.argv[1] == "measure":
			measure()
		elif sys.argv[1] == "race":
			race()
	else:
		print("invalid command line arguement")