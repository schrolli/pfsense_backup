import sys
import os.path

def exists_not_empty(haystack, needles, array_name = ''):
	for needle in needles:
		if needle not in haystack or not haystack[needle]:
			if array_name == '':
				array_name = 'config-root'
			print("Config Error: key %s in %s is missing or empty" % (needle,array_name),file=sys.stderr)
			sys.exit(1)
def bool_exists(haystack, needles, array_name = ''):
	for needle in needles:
		if needle not in haystack:
			if array_name == '':
				array_name = 'config-root'
			print("Config Error: key %s in %s is missing or empty" % (needle,array_name),file=sys.stderr)
			sys.exit(1)
def int_exists(haystack, needles, array_name = ''):
	for needle in needles:
		if needle not in haystack or haystack[needle] <= 0:
			if array_name == '':
				array_name = 'config-root'
			print("Config Error: key %s in %s is missing or empty" % (needle,array_name),file=sys.stderr)
			sys.exit(1)

def dir_exists(path, key):
	if (not os.path.isdir(path)):
		print("Error: folder for key '%s' doesn't exist: %s" % (key, path), file=sys.stderr)
		sys.exit(1)

def abs_path(path, key):
	if not os.path.isabs(path):
		print("Error: the path for config-key %s has to be absolute!" % key, file=sys.stderr)
		sys.exit(1)
