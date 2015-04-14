from kmeans.user import User
from kmeans.datapoint_loader import DataLoader
#from pylab import *
import sys
import matplotlib.pyplot as plt
import matplotlib as matplotlib

loader = DataLoader()

def per_field(field):
	
	users = loader.fetch_data(field)
	points = {}
	count_points = {}
	for user in users:
		if user.age not in points:
			points[user.age] = 0
		if user.age not in count_points:
			count_points[user.age] = 0
		points[user.age] += user.downvotes
		count_points[user.age] += 1

	counts = []
	age = []
	downvotes = []
	

	for point in points:
		if point >= 13:
			age += [point]
			downvotes += [points[point]]
			counts += [count_points[point]]

	for i in range(0, len(downvotes)):
		downvotes[i] = downvotes[i] * 1.0 / counts[i]
	# turn counts to percentages
	#for i in range(0, len(downvotes)):
	#	downvotes[i] = downvotes[i] * 100.0 / total_count
	plt.plot(age, downvotes)





def all(fields) :

	for field in fields:
		per_field(field)

	plt.xlabel('age')
	plt.ylabel('Average number of downvotes')
	plt.title('Average number of downvotes per age')
	plt.legend(fields)
	plt.grid(True)
	plt.savefig("age-%s.png" % field)
	plt.show()

def one(field): 
	
	per_field(field)
	plt.xlabel('age')
	plt.ylabel('Average number of downvotes')
	plt.title('Average number of downvotes per age')
	plt.grid(True)
	plt.savefig("age-%s.png" % field)
	plt.show()

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)
fields = ["beer", "anime", "apple", "askubuntu", "christianity", "datascience", "gaming", "mathoverflow", "parenting", "tor"]
six_fields = ["anime", "datascience", "apple", "christianity", "gaming","parenting"]
if len(sys.argv) == 2:

	field = sys.argv[1]
	one(field)

else:
	all(six_fields)

