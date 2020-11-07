#!/usr/bin/env python

"""
Track /var/log/dynconfd.log and restart the service dynconfd when the suspicious error log appear


Usage (Under Bash context):
Option 1 - run on background (recommended)
nohup python dynconf_workaround.py &

Option 2 - run in realtime (if SSH connection is end the script is end as well)
python dynconf_workaround.py
"""


__version__ = "0.1"
__all__ = ["temp workaround for dynconf problem"]
__author__ = "DvirPerets"
__home_page__ = "https://www.linkedin.com/in/dvirperets"

import os, time, re
filename = "/var/log/ltm"
file = open(filename,'r')
#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

#loop through the file to find suspicious log
# New results!!! ex2pw.ozar.main resolves to $
while True:
	where = file.tell()
	line = file.readline()
	if not line:
       		time.sleep(1)
       		file.seek(where)
    	else:
		print line, # already has newline
		if re.match('New results!!! .* resolves to $', line) is not None:
			print "suspicious log line found, restarting dynconfd service:"
			os.system('tmsh -c "restart sys service dynconfd"')		
