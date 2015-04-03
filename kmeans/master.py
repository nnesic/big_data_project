from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import requests
from datapoint_loader import DataLoader
import random
import threading


ids = []
config = json.load(open("config.json"))
num_workers = len(config["HOSTS"]["workers"])
worker_port = config["HOSTS"]["worker_port"]
max_iterations = 200

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
			if attribute in ['id', "tags_count"]:
				continue
			a_min = 1000000000
			a_max = - 100000000
			for user in users:
				if user.__getattribute__(attribute) > a_max:
					a_max = user.__getattribute__(attribute)
				if user.__getattribute__(attribute) < a_min:
					a_min = user.__getattribute__(attribute)

			# normalize and add to data points
			for i in range(0, len(users)):
				val =  1.0 * users[i].__getattribute__(attribute) - a_min 
				points[i] += [val / (a_max - a_min)]

		# points = [[3, 3], [4, 3], [12, 3], [13, 3]]	 Testing

		# distribute the points
		distributed_points = []
		for i in range(0, num_workers):
			distributed_points += [[]]

		for i in range(0, len(points)):
			distributed_points[i%num_workers] += [points[i]]


		# start with 2 centroids? 
		num_centroids = 2
		centroids = []

		# pick random points as centroids
		for i in range(0, num_centroids):
			id = random.randint(0, len(points) - 1)
			centroids += [points[id]]
		
		# centroids = [[4, 1], [4, 4]]						Testing 

		iterations = 0
		another_iteration = True
		adjustments = []
		pt_counts = []
		for i in range(0, len(centroids)):
			adjustments += [[]]
			for j in range(0, len(centroids[0])):
				adjustments[i] += [0]
			pt_counts += [0]


		
		# send the points over
		for i in range(0, num_workers):
			headers = {'content-type': 'application/json'}
			payload = {"id": job_id, "action": "points", "points": distributed_points[i]}
			requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][i], worker_port), data=json.dumps(payload), headers=headers)


		while (iterations < max_iterations and another_iteration):
			# threading mubmo jumbo
			responses = []

			for i in range(0, num_workers):
				responses += [None]

			thread_list = []

			for i in range(0, num_workers):
				t = threading.Thread(target=do_work, args = (responses, i, centroids, job_id))
				thread_list.append(t)
				t.start()			
				

			for thread in thread_list:
				thread.join()

	     	#aggregate all the adjustments from workers
			for r in responses:
				for i in range(0, len(centroids)):
					pt = json.loads(r.content)["recalculated_centroids"][i]
					for j in range(0, len(centroids[0])):
						adjustments[i][j] += pt["adjustments"][j]
					pt_counts[i] += pt["point_count"]

			new_centroids = []

			# calculate new centroids
			for i in range(0, len(centroids)):
				new_point = []
				for j in range(0, len(centroids[0])):
					new_point += [adjustments[i][j] * 1.0 / max(1, pt_counts[i])]
				if new_point == [0, 0]:				# if no points are assigned to the centroid, we don't want it to go to 0, 0
					new_point = centroids[i]
				new_centroids += [new_point]
			
			# calculate the difference between the two centroids
			differences = []
			for i in range(0, len(centroids)):
				summup = 0
				for j in range(0, len(centroids[0])):
					summup += (new_centroids[i][j] - centroids[i][j])**2
				differences += [summup**0.5]
			max_difference = 0
			for diff in differences:
				if diff > max_difference:
					max_difference = diff

			if max_difference < 0.001:
				another_iteration = False

			centroids = new_centroids
			iterations += 1

		
		# tell the workers we are done
		for i in range(0, num_workers):
			payload = {"id": job_id, "action": "done"}
			requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][i], worker_port), data=json.dumps(payload), headers=headers)

		# now, restore the centroids information into the original ranges
		keys = users[0].__dict__.keys()
		keys.pop(keys.index("id"))
		keys.pop(keys.index("tags_count"))
		for i in range(0, len(keys)):
			attribute = keys[i]
			if attribute in ['id', "tags_count"]:
				continue
			a_min = 1000000000
			a_max = - 100000000
			for user in users:
				if user.__getattribute__(attribute) > a_max:
					a_max = user.__getattribute__(attribute)
				if user.__getattribute__(attribute) < a_min:
					a_min = user.__getattribute__(attribute)

			for cent in centroids:
				cent[i] = cent[i] * (a_max - a_min) + a_min

		# keys = ["x", "y"]				Testing
		# pretty print!
		ret = "<table> <tr> <td> </td>" 
		# header line 
		for i in range(0, len(centroids)):
			ret += "<td> Group %d </td> \n" % i
		ret += '</tr>\n'

		for i in range(0, len(keys)):
			attribute = keys[i]
			ret += "<tr><td>" + attribute + "</td>\n"
			for j in range(0, len(centroids)):
				ret += "<td> %.3f </td>\n" % centroids[j][i]
			ret += "</tr>"
			ret += '\n'
		ret += "</table>"



		self.write(ret)
		print  "done"
		#self.write("ok")

def do_work(responses, index, centroids, job_id):
	try:
		headers = {'content-type': 'application/json'}

		payload = {"id": job_id, "action": "centroids", "centroids": centroids}
		r = requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][index], worker_port), data=json.dumps(payload), headers=headers)

		payload = {"id": job_id, "action": "go"}
		r = requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][index], worker_port), data=json.dumps(payload), headers=headers)
	
	except Exception as e:
		print e.message
		
	responses[index] = r


application = tornado.web.Application([
    (r"/master/([\w]+)", MainHandler)
])
 

if __name__ == "__main__":
    application.listen(51000)
    tornado.ioloop.IOLoop.instance().start()



