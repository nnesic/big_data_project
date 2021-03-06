from kmeans.user import User
from kmeans.datapoint_loader import DataLoader
#from pylab import *
import sys
import matplotlib.pyplot as plt
import matplotlib as matplotlib

loader = DataLoader()

def age_in_field(field):
	
	users = loader.fetch_data(field)
	points = {}

	for user in users:
		if user.age not in points:
			points[user.age] = 0
		points[user.age] += 1

	age = []
	count = []
	
	for point in points:
		if point >= 13:
			age += [point]
			count += [points[point]]
	total_count = sum(count)
	# turn counts to percentages
	for i in range(0, len(count)):
		count[i] = count[i] * 100.0 / total_count
	plt.plot(age, count)





def all(fields) :

	for field in fields:
		age_in_field(field)

	plt.xlabel('age')
	plt.ylabel('% of users')
	plt.title('Age distribution of users ')
	plt.legend(fields)
	plt.grid(True)
	plt.savefig("age-%s.png" % field)
	plt.show()

def one(field): 
	
	age_in_field(field)
	plt.xlabel('age')
	plt.ylabel('# of users')
	plt.title('Age distribution of users ')
	plt.grid(True)
	plt.savefig("age-%s.png" % field)
	plt.show()

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)
fields = ["beer", "anime", "apple", "askubuntu", "christianity", "datascience", "gaming", "mathoverflow", "parenting", "tor"]
six_fields = ["anime", "apple", "christianity", "datascience", "gaming","parenting"]
if len(sys.argv) == 2:

	field = sys.argv[1]
	one(field)

else:
	all(six_fields)

