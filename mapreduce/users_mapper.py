#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET

input_string = sys.stdin.read()


root = ET.fromstring(input_string)
print # id reputation views upvotes downvotes age
for child in root.getchildren():
        try:
                user_id = int(child.get("Id"))
		reputation = int(child.get("Reputation"))
		views = int(child.get("Views"))
		upvotes = int(child.get("UpVotes"))
		downvotes = int(child.get("DownVotes"))
		age = child.get("Age")
		if age != None:
			age = int(age)
		else:
			age = 0 
       		print "%d %d %d %d %d %d " % (user_id, reputation, views, upvotes, downvotes, age)
	except Exception as e:
                sys.stderr.write(e.message + "\n")

