# a simple class to load user datapoints from database

import MySQLdb
from user import User
import json

config_file  = "config.json"
class DataLoader(object):

	def __init__(self):
		self.config = json.load(open(config_file))

	def fetch_data(self, field):
		users = []
		database = self.config["DATABASE"]
		db = MySQLdb.connect(host=database["host"], port=45000, user=database["user"], passwd=database["password"], db=database["db"])
		cursor = db.cursor()
		cols = "user_id, field, number_posts_type_1, number_posts_type_2, number_comments, avg_post_score, avg_comment_score, avg_post_size, avg_comment_size, upvotes, downvotes, views, age, reputation, id"
		cursor.execute("SELECT %s from users WHERE field = '%s'" % (cols, field))
		for row in cursor.fetchall():
			user = User(row[0])
			user.post_type_1_count = row[2]
	                user.post_type_2_count = row[3]
                	user.avg_post_score = row[5]
                	user.avg_post_size = row[7]
                	user.tags_count = {}
                	user.comments_count = row[4]
                	user.avg_comment_size = row[8]
                	user.avg_comment_score = row[6]
               		user.upvotes = row[9]
                	user.downvotes = row[10]
                	user.views = row[11]
                	user.age = row[12]
                	user.reputation = row[13] 
			id = row[14]
			
			tag_cursor = db.cursor()
			tag_cursor.execute("SELECT tag, tag_count FROM tags where user_id = %d" % row[0])

			for r in tag_cursor:
				user.tags_count[r[0]] = r[1]
			users += [user]
		
		return users 
			


#d = DataLoader()
#d.fetch_data("beer")









