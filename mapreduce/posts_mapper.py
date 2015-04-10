#!/usr/bin/env python

import sys
import os
import xml.etree.ElementTree as ET

#input_string = sys.stdin.read()


class User(object):

	def __init__(self, id):
		self.id = id
		self.post_type_1_count = 0
		self.post_type_2_count = 0
		self.aggregate_post_score = 0
		self.aggregate_post_size = 0
		self.tags_count = {}		

for f in filter(lambda x: x.startswith("postsaa"), os.listdir("/home/nera/SharedDir")):
	sys.stderr.write(f + "\n")
	users = {}
	fajl = open("/home/nera/SharedDir/" + f)
	input_string = fajl.read()
	root = ET.fromstring(input_string)
	for child in root.getchildren():
		try:
			user_id = int(child.get("OwnerUserId"))
			post_type = int(child.get("PostTypeId"))
			score = int(child.get("Score"))
			post_size = len(child.get("Body"))
			tags = child.get("Tags")

			if user_id not in users:
				users[user_id] =  User(user_id)
			user = users[user_id]
			if post_type == 1:
				user.post_type_1_count += 1
			else:
				user.post_type_2_count += 1
			user.aggregate_post_score += score
			user.aggregate_post_size += post_size

			if tags != None:
				tags = tags.replace("<", " ").replace(">", " ").split()	
				for tag in tags:
					if tag not in user.tags_count:
						user.tags_count[tag] = 0
					user.tags_count[tag] += 1
		except Exception as e:
			pass
			#sys.stderr.write(e.message + "\n")
	fajl.close()
	for i in users:
		user = users[i]
		out = "%d %d %d %d %d " % (user.id, user.post_type_1_count, user.post_type_2_count, user.aggregate_post_score, user.aggregate_post_size)
		for tag in user.tags_count:
			out += "%s %d " % (tag, user.tags_count[tag])
		print out


