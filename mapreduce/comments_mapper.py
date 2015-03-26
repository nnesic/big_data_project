#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET

input_string = sys.stdin.read()


class User(object):

        def __init__(self, id):
                self.id = id
                self.comment_count = 0
                self.aggregate_comment_score = 0
                self.aggregate_comment_size = 0


users = {}
root = ET.fromstring(input_string)
for child in root.getchildren():
        try:
                user_id = int(child.get("UserId"))
		score = int(child.get("Score"))
                post_size = len(child.get("Text"))

                if user_id not in users:
                        users[user_id] =  User(user_id)
                user = users[user_id]
                user.comment_count += 1
                user.aggregate_comment_score += score
                user.aggregate_comment_size += post_size

        except Exception as e:
                sys.stderr.write(e.message + "\n")
for i in users:
        user = users[i]
        print "%d %d %d %d" % (user.id, user.comment_count, user.aggregate_comment_score, user.aggregate_comment_size) 

