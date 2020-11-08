#!/usr/bin/env python

"""
Track /var/log/dynconfd.log and restart the service dynconfd when the suspicious error log appear


Usage (Under Bash context):
Option 1 - run on background (recommended)
nohup python dynconf_workaround.py &

Option 2 - run in realtime (if SSH connection is end the script is end as well)
python dynconf_workaround.py
"""

import os, time, re, smtplib
filename = "/var/log/dynconfd.log"
file = open(filename,'r')
#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

#loop through the file to find suspicious log
while True:
	where = file.tell()
	line = file.readline()
	if not line:
       		time.sleep(1)
       		file.seek(where)
    	else:
		#print line, # already has newline
		if re.match('New results!!! .* resolves to $', line) is not None:
			print "suspicious log line found, sending email"
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("email@gmail.com", "password")
			server.sendmail(
			  "email@gmail.com",
			  "to@gmail.com",
			  "suspicious log line found in dynconfd!")
			server.quit()
			print "suspicious log line found, tcpdump port 53"
			os.system('tcpdump -U -c 30 -s0 -i 0.0:nnn "port 53" -w /var/tmp/resolve_error.pcap')
			print "suspicious log line found, sleeping 5 sec and restarting dynconfd service:"
			time.sleep(5)
			os.system('tmsh -c "restart sys service dynconfd"')
			print "sleeping 10 sec and looping again"
			time.sleep(10)

