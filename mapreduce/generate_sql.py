import sys

if len(sys.argv) != 3:
	print "usage: <directory> <field name>"
	exit()

print "USE stackexchange;"
directory = sys.argv[1]
field = sys.argv[2]
if directory[-1] != '/':
	directory += '/'

class User(object):

        def __init__(self, id):
                self.id = id
                self.post_type_1_count = 0
                self.post_type_2_count = 0
                self.aggregate_post_score = 0
                self.aggregate_post_size = 0
                self.tags_count = {}
		self.comments_count = 0
		self.aggregate_comment_size = 0
		self.aggregate_comment_score = 0
		self.upvotes = 0
		self.downvotes = 0
		self.views = 0
		self.age = 0
		self.reputation = 0


users = {}
# process users
users_file = open(directory+"users.result")
for line in users_file.readlines():

	line = line.split()
	id = int(line[0])
	user = User(id)
	user.reputation = int(line[1])
	user.views = int(line[2])
	user.upvotes = int(line[3])
	user.downvotes = int(line[4])
	user.age = int(line[5])
	users[id] = user
users_file.close()
# process posts
posts_file = open(directory+"posts.result")
for line in posts_file.readlines():
	
	line = line.split()
	id = int(line[0])
	user = users[id]
	user.post_type_1_count = int(line[1])
	user.post_type_2_count = int(line[2])
	user.aggregate_post_score = int(line[3])
	user.aggregate_post_size = int(line[4])
	if len(line) > 5:
                        #this means we got tags
                        for i in range (5, len(line), 2):
                                tag = line[i]
                                count = int((line[i+1]))
                                user.tags_count[tag] = count
posts_file.close()

# process comments
comments_file = open(directory + "comments.result")
for line in comments_file.readlines():
	
	line = line.split()
	id = int(line[0])
	user = users[id]
	user.comments_count = int(line[1])
	user.aggregate_comment_score = int(line[2])
	user.aggregate_comment_size  = int(line[3])

for id in users:
	user = users[id]
	posts = user.post_type_1_count + user.post_type_2_count
	if posts == 0:
		posts = 1
	comments = user.comments_count * 1.0
	if comments == 0:
		comments = 1
	print "INSERT INTO users (user_id, field, number_posts_type_1, number_posts_type_2, number_comments, avg_post_score, avg_comment_score, avg_post_size, avg_comment_size, upvotes, downvotes, views, age, reputation)VALUES (%d, '%s', %d, %d, %d, %f, %f, %f, %f, %d, %d, %d, %d, %d);" % (user.id, field, user.post_type_1_count, user.post_type_2_count, user.comments_count, 1.0*user.aggregate_post_score/posts, 1.0*user.aggregate_comment_score/comments, 1.0*user.aggregate_post_size/posts, 1.0*user.aggregate_comment_size/comments, user.upvotes, user.downvotes, user.views, user.age, user.reputation) 
	for tag in user.tags_count:
		print "INSERT INTO tags (user_id, tag, tag_count) VALUES ((SELECT id from users where users.user_id = %d and field = '%s'), '%s', %d);" % (user.id, field, tag, user.tags_count[tag])
