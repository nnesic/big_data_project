from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import json

processes = {}


class ProcessHandler(tornado.web.RequestHandler):
    
    def post(self):
        #import pdb; pdb.set_trace()
        data = json.loads(self.request.body)
        
        id = int(data['id'])
        if id not in processes:
            processes[id] = Processor(id)
        proc = processes[id]
        
        action = data["action"]
        if action == "points":
            print "got points"
            points = data["points"]
            proc.set_points(points)
            self.write("ok")
            return
        elif action == "centroids":
            print "got centroids"
            centroids = data["centroids"]
            proc.set_centroids(centroids)
            self.write("ok")
            return

        elif action == "evaluate":
            print "got eval"
            distances = proc.calculate_distance_from_centroids()
            response = {"id": proc.id, "distances": distances}
            self.write(json.dumps(response))
            return

        elif action == "go":
            print "got go"
            recalculated_centroids = proc.do_the_thing()
            response = {"id": proc.id, "recalculated_centroids": recalculated_centroids}
            self.write(json.dumps(response))
            print "done"
            return

        elif action == "done":
            print "got done"
            processes.pop(id)

        
        self.write(json.dumps(processes))



class Processor(object):

    def __init__(self, id):
        self.id = id
        self.points = []
        self.centroids = []

    def set_centroids(self, centroids):
        self.centroids = []
        for point in centroids:
            p = Point()
            p.coordinates = map(lambda x: float(x), point)
            self.centroids += [p]

    def set_points(self, points):
        self.points = []
        for point in points:
            p = Point()
            p.coordinates = map(lambda x: float(x), point)
            self.points += [p]

    def do_the_thing(self):
        print "doing the thing"
        self.assign_points()
        return self.recalculate_centroids()

    def assign_points(self):
        """ find the nearest centroid for each point """
        # clear all point counts
        for cent in self.centroids:
            cent.point_count = 0
            
        for point in self.points:
            min_distance = 1000000000000
            min_i = -1
            for i in range(0, len(self.centroids)):
                cent = self.centroids[i]
                dist = 0
                for j in range (0, len(cent.coordinates)):
                    dist += (cent.coordinates[j] - point.coordinates[j])**2
                dist = dist**0.5
                if dist < min_distance:
                    min_distance = dist
                    min_i = i

            point.centroid = min_i
            self.centroids[min_i].point_count += 1
        #print str(self.points)


    def recalculate_centroids(self):
        """returns the adjustment that we need to do to each centroid"""
        recalculations = []
        for i in range(0, len(self.centroids)):
            cent = self.centroids[i]
            temp = []
            for j in range(0, len(cent.coordinates)):
                sum = 0
                for point in self.points:
                    if point.centroid != i:
                        continue
                    sum += point.coordinates[j]
                temp += [sum]
            recalculations += [{"adjustments": temp, "point_count": cent.point_count}]

        #print recalculations
        return recalculations
    

    def calculate_distance_from_centroids(self):
        """for every centroid, returns what is the average distance """
        self.assign_points()
        distances = [0] * len(self.centroids)
        resp = []
        for point in self.points:
            d = 0
            cent = self.centroids[point.centroid]
            cent.point_count += 1
            for i in range(0, len(self.centroids)):
                d += (point.coordinates[i] - cent.coordinates[i])**2
            d = d**0.5
            distances[point.centroid] += d

        for i in range(0, len(distances)):
            d = distances[i]
            cent = self.centroids[i]
            resp += [{"total": d, "point_count": cent.point_count}]

        return resp










class Point(object):

    def __init__(self):
        self.centroid = None     # this will be the index of centroids
        self.coordinates = [] 
        self.point_count = 0     # only used by centroids to keep track of how many points were assigned to it this itteration

    def __str__(self):
        return str(self.coordinates) + " " +str(self.centroid)

    def __repr__(self):
        return str(self.coordinates) + " " + str(self.centroid)





application = tornado.web.Application([
    (r"/worker/", ProcessHandler)
])
 
if __name__ == "__main__":
    application.listen(51001)
    tornado.ioloop.IOLoop.instance().start()