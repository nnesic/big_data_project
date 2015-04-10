from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import requests
from datapoint_loader import DataLoader
import random
import threading
from copy import deepcopy
import time
from canvas_generator import CanvasGenerator


ids = []
config = json.load(open("config.json"))
num_workers = len(config["HOSTS"]["workers"])
worker_port = config["HOSTS"]["worker_port"]
max_iterations = 2000

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

		attribute_max = {}
		attribute_min = {}

		# normalize data
		# for each property, find min and max value, and project to a 0 - 1 range
		for attribute in users[0].__dict__:
			if attribute in ['id', "tags_count", "user_id"]:
				continue
			a_min = 1000000000
			a_max = - 100000000
			for user in users:
				if user.__getattribute__(attribute) > a_max:
					a_max = user.__getattribute__(attribute)
				if user.__getattribute__(attribute) < a_min:
					a_min = user.__getattribute__(attribute)
			attribute_max[attribute] = a_max
			attribute_min[attribute] = a_min
			# normalize and add to data points
			for i in range(0, len(users)):
				val =  1.0 * users[i].__getattribute__(attribute) - a_min 
				points[i] += [val / (a_max - a_min)]

		total_points = 5000
		difference = total_points - len(points)
		for i in range(0, difference):
			points += [points[0]]

		# points = [[3, 3], [4, 3], [12, 3], [13, 3]]	 

		# distribute the points
		distributed_points = []
		for i in range(0, num_workers):
			distributed_points += [[]]

		for i in range(0, len(points)):
			distributed_points[i%num_workers] += [points[i]]


		# start with 2 centroids? 
		num_centroids = 9
		iterations = 0
		another_iteration = True
		centroids_by_number = {}
		centroids_scores = {}

		start = time.time()		
		# send the points over
		for i in range(0, num_workers):
			headers = {'content-type': 'application/json'}
			payload = {"id": job_id, "action": "points", "points": distributed_points[i]}
			requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][i], worker_port), data=json.dumps(payload), headers=headers)


		while (num_centroids < 10):
			# pick random points as centroids
			# centroids = random.sample(points, num_centroids)
			# nope; instead generate points randomly
			centroids = []
			for i in range(0, num_centroids):
				centroids += [[]]
				for j in range(0, len(points[0])):
					centroids[i] += [random.random()]
			#print centroids


			# centroids = [[4, 1], [4, 4]]
			while (iterations < max_iterations and another_iteration):
				
				new_centroids = self.get_new_centroids(centroids, job_id)
					
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

			break
			scores = self.evaluate_centroids(centroids, job_id)
			centroids_by_number[num_centroids] = deepcopy(centroids)
			centroids_scores[num_centroids] = scores
			num_centroids += 1


		end = time.time()

		ret =  "points: %d \n" % len(points)
		ret += "time: %f" % (end - start)
		self.write(ret)
		return
		#set centroids to be the min scored set
		min_score = 1000000000000
		min_num = 0
		for num in centroids_scores:
			print "%d  %f" % (num, centroids_scores[num])
			if centroids_scores[num] < min_score:
				min_score = centroids_scores[num]
				min_num = num
		centroids = centroids_by_number[min_num]


		# tell the workers we are done
		for i in range(0, num_workers):
			payload = {"id": job_id, "action": "done"}
			requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][i], worker_port), data=json.dumps(payload), headers=headers)

		ret = ""
		
		# for num in centroids_by_number:
		# 	centroids = centroids_by_number[num]
		# 	# now, restore the centroids information into the original ranges
		# 	keys = users[0].__dict__.keys()
		# 	keys.pop(keys.index("id"))
		# 	keys.pop(keys.index("tags_count"))
		# 	for i in range(0, len(keys)):
		# 		attribute = keys[i]
		# 		if attribute in ['id', "tags_count"]:
		# 			continue
		# 		a_min = attribute_min[attribute]
		# 		a_max = attribute_max[attribute]

		# 		for cent in centroids:
		# 			cent[i] = cent[i] * (a_max - a_min) + a_min


		# 	# header line 
		# 	ret += "<table> <tr> <td> </td>" 
		# 	for i in range(0, len(centroids)):
		# 		ret += "<td> Group %d </td> \n" % i
		# 	ret += '</tr>\n'

		# 	for i in range(0, len(keys)):
		# 		attribute = keys[i]
		# 		ret += "<tr><td>" + attribute + "</td>\n"
		# 		for j in range(0, len(centroids)):
		# 			ret += "<td> %.3f </td>\n" % centroids[j][i]
		# 		ret += "</tr>"
		# 		ret += '\n'
		# 	ret += "</table>"
		# 	ret +="<br><br>"
		for num in centroids_by_number:
			centroids = centroids_by_number[num]
			attributes = users[0].__dict__.keys()
			attributes.pop(attributes.index("id"))
			attributes.pop(attributes.index("tags_count"))
			#attributes.pop(keys.index("user_id"))
			cg = CanvasGenerator(attributes, centroids)
			ret += cg.get_canvas()
		end = time.time()
		print "points: %d" % len(users)
		print "time: %f" % (end - start)
		self.write(ret)
		print  "done"




	def get_new_centroids(self, centroids, job_id):
		"""Sends the centroids to workers, and aggregates their responses into new centroids"""
		responses = []
		adjustments = []
		pt_counts = []
		for i in range(0, len(centroids)):
			adjustments += [[]]
			for j in range(0, len(centroids[0])):
				adjustments[i] += [0]
			pt_counts += [0]

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

		return new_centroids



	def evaluate_centroids(self, centroids, job_id):
		"""Sends the centroids to workers, gets average distance of points to them, and calculates the Davies-Bouldin index"""
		responses = []

		for i in range(0, num_workers):
			responses += [None]
		thread_list = []
		for i in range(0, num_workers):
			t = threading.Thread(target=eval_centroids, args = (responses, i, centroids, job_id))
			thread_list.append(t)
			t.start()			
		for thread in thread_list:
			thread.join()

		# get the average distance of points to the centroid
		pt_counts = [0] * len(centroids)
		total_distance = [0] * len(centroids)
		for r in responses:
			for i in range(0, len(centroids)):
				pt = json.loads(r.content)["distances"][i]
				total_distance[i] += pt["total"]
				pt_counts[i] += pt["point_count"]
		average_distance = []
		for i in range(0, len(total_distance)):
			average_distance += [total_distance[i] * 1.0 / max(pt_counts[i], 1)]

		summation = 0
		import pdb
		for i in range(0, len(centroids)):
			max_thing = 0
			for j in range(0, len(centroids)):
				if i == j:
					continue
				# distance ci, cj
				denom = 0
				for c in range(0, len(centroids[0])):
					denom += (centroids[i][c] - centroids[j][c])**2
				denom = denom**0.5
				if denom == 0:
					pdb.set_trace()
				nom = average_distance[i] + average_distance[j]
				if nom * 1.0 / denom > max_thing:
					max_thing = nom * 1.0 / denom
			summation += max_thing
		summation = summation / len(centroids)

		return summation 


def eval_centroids(responses, index, centroids, job_id):
	try:
		headers = {'content-type': 'application/json'}

		payload = {"id": job_id, "action": "centroids", "centroids": centroids}
		r = requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][index], worker_port), data=json.dumps(payload), headers=headers)

		payload = {"id": job_id, "action": "evaluate"}
		r = requests.post("http://%s:%d/worker/" % (config["HOSTS"]["workers"][index], worker_port), data=json.dumps(payload), headers=headers)
	
	except Exception as e:
		print e.message
		
	responses[index] = r


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



