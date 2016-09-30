#!/usr/bin/env python3

from __future__ import print_function
import sys
import json
import os.path
import datetime
import requests
from lxml import html

from json_minify import json_minify
import check

def main(config, verbose):
	if not os.path.isfile(config):
		print("Error: configfile %s was not found" % config, file=sys.stderr)
	conf_file = open(config,'r')
	conf = json.loads(json_minify(conf_file.read()))
	conf_file.close()

	check.exists_not_empty(conf, ['host', 'user', 'password', 'dest_dir', 'file_prefix'])
	check.abs_path(conf['dest_dir'],'dest_dir')
	check.dir_exists(conf['dest_dir'],'dest_dir')
	
	url = 'https://%s/diag_backup.php' % conf['host']
	
	session = requests.Session()
	session.verify = False
	
	# request the login-form to get the csrf-magic-token for login submission
	page = session.get(url)
	page.raise_for_status()
	csrf_magic = fetch_csrf_magic(page)
	if csrf_magic == None:
		print("Error: fetching of the csrf-magic from the login-form failed, see above")
		sys.exit(1)
	
	#POST login form
	page = session.post(url, data = {
		'login': 'Login',
		'usernamefld': conf['user'],
		'passwordfld': conf['password'],
		'__csrf_magic': csrf_magic,
	})
	page.raise_for_status()
	csrf_magic = fetch_csrf_magic(page)
	if csrf_magic == None:
		print("Error: fetching of the csrf-magic from the download-form failed, see above")
		sys.exit(1)
	
	#requesting config
	page = session.post(url, data = {
		'Submit': 'download',
		'donotbackuprrd': 'yes',
		'__csrf_magic': csrf_magic,
	})
	page.raise_for_status()
	
	#preparing absolute filename
	filename = conf['file_prefix'] + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + '.xml'
	filepath = os.path.join(conf['dest_dir'], filename)
	
	#writing to file
	file = open(filepath,'w')
	file.write(page.text)
	file.close()

def fetch_csrf_magic(page):
	tree = html.fromstring(page.content)
	elements = tree.xpath('//input[@name="__csrf_magic"]/@value')
	if len(elements) != 1:
		print("Error: while fetching the csrf value, %d elements where fetched" % len(elements))
		return None
	return elements[0]

if __name__=="__main__":
	import argparse
	
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-v", "--verbose", action = "count", default = 0,
		help =	"increase verbosity for manual run\n"
			"use multiple times for more verbosity\n"
			">=1: comments, which step is executing\n"
			">=2: lvcreate and lvremove stdout and rsync -v\n"
			">=3: rsync --progress")
	parser.add_argument("-c", "--config", help = "use specific config-file (default: /etc/pfsense_backup/config.json)", default = "/etc/pfsense_backup/config.json")
	args = parser.parse_args()
	
	main(args.config, args.verbose)
