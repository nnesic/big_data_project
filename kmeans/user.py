# simple user model class

class User(object):

        def __init__(self, id):
                self.id = id
                self.post_type_1_count = 0
                self.post_type_2_count = 0
                self.avg_post_score = 0
                self.avg_post_size = 0
                self.tags_count = {}
                self.comments_count = 0
                self.avg_comment_size = 0
                self.avg_comment_score = 0
                self.upvotes = 0
                self.downvotes = 0
                self.views = 0
                self.age = 0
                self.reputation = 0

