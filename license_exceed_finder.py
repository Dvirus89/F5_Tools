#!/usr/bin/env python

"""
Track ltm log file and execute tcpdump when license throughput exceeded

Usage (Under Bash context):
Option 1 - run on background (recommended)
nohup python license_exceed_finder.py &

Option 2 - run in realtime (if SSH connection is end the script is end as well)
python license_exceed_finder.py
"""


__version__ = "0.1"
__all__ = ["license_exceed_finder"]
__author__ = "DvirPerets"
__home_page__ = "https://www.linkedin.com/in/dvirperets"

import os, time
filename = "/var/log/ltm"
file = open(filename,'r')
#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

#loop through the file to find licensed exceptions
while True:
	where = file.tell()
	line = file.readline()
	if not line:
       		time.sleep(1)
       		file.seek(where)
    	else:
		print line, # already has newline
		if "exceeded 75" in line:
			print "License Exceeded, capturing traffic"
			os.system('tcpdump -U -c 30000 -s0 -i 0.0:nnn -w /var/tmp/burst.pcap')
			break		
