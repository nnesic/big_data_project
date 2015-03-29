from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import requests
from datapoint_loader import DataLoader


ids = []
config = json.load(open("config.json"))
num_workers = len(config["HOSTS"]["workers"])

class MainHandler(tornado.web.RequestHandler):

	def get(self, field):
		# find an id to assign to the job
		job_id = 0
		while job_id in ids:
			job_id += 1
		globals()["ids"] += [job_id]

		# load the points
		loader = DataLoader()
		users = loader.fetch_data(field)

		#these will be the points we send over
		points = []
		for user in users:
			points += [[]]

		# normalize data
		# for each property, find min and max value, and project to a 0 - 1 range
		for attribute in users[0].__dict__:
			print attribute
			if attribute == 'id':
				continue
			min = 1000000000
			max = - 100000000
			for user in users:
				if user.__getattribute__(attribute) > max:
					max = user.__getattribute__(attribute)
				if user.__getattribute__(attribute) < min:
					min = user.__getattribute__(attribute)

			# normalize and add to data points
			for i in range(0, len(users)):
				val = 1.0 * users[i].__getattribute__(attribute) - min 
				points[i] += [val / max]

		print points

		headers = {'content-type': 'application/json'}
		#points = [[0, 1], [1, 0], [1, 1], [2, 1], [2, 2], [3, 1]]
		centroids = [[0, 0], [3,2]]

		#send points 
		# payload = {"id": job_id, "action": "points", "points": points}
		# r = requests.post("http://localhost:50001/worker/", data=json.dumps(payload), headers=headers)

		# payload = {"id": job_id, "action": "centroids", "centroids": centroids}
		# r = requests.post("http://localhost:50001/worker/", data=json.dumps(payload), headers=headers)

		# payload = {"id": job_id, "action": "go"}
		# r = requests.post("http://localhost:50001/worker/", data=json.dumps(payload), headers=headers)
		# self.write(r.content)
		self.write("ok")




application = tornado.web.Application([
    (r"/master/([\w]+)", MainHandler)
])
 

if __name__ == "__main__":
    application.listen(51000)
    tornado.ioloop.IOLoop.instance().start()



