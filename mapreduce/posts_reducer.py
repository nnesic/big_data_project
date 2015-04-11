#!/usr/bin/env python

import sys


class User(object):

        def __init__(self, id):
                self.id = id
                self.post_type_1_count = 0
                self.post_type_2_count = 0
                self.aggregate_post_score = 0
                self.aggregate_post_size = 0
                self.tags_count = {}
sys.stderr.write("made it to reducer!\n") 
users = {}
for line in sys.stdin:
	try:	
		vals = line.split()
        	user_id = int(vals[0])
		post_type_1 = int(vals[1])
    		post_type_2 = int(vals[2])
		aggregate_post_score = int(vals[3])
		aggregate_post_size = int(vals[4])
		tags = {}
		if len(vals) > 5:
			#this means we got tags
 			for i in range (5, len(vals), 2):
				tag = vals[i]
				count = int((vals[i+1]))
				tags[tag] = count

		if user_id not in users:
			users[user_id] = User(user_id)
		user = users[user_id]
		user.post_type_1_count += post_type_1
		user.post_type_2_count += post_type_2
		user.aggregate_post_score += aggregate_post_score
		user.aggregate_post_size += aggregate_post_size
		for tag in tags:
			if tag not in user.tags_count:
				user.tags_count[tag] = 0
			user.tags_count[tag] += tags[tag]
	except Exception as e:
		sys.stderr.write(e.message + "\n")


for i in users:
        user = users[i]
        out = "%d %d %d %d %d " % (user.id, user.post_type_1_count, user.post_type_2_count, user.aggregate_post_score, user.aggregate_post_size)
        for tag in user.tags_count:
                out += "%s %d " % (tag, user.tags_count[tag])
        print out


