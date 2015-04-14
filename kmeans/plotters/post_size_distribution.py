from kmeans.user import User
from kmeans.datapoint_loader import DataLoader
#from pylab import *
import sys
import matplotlib.pyplot as plt
import matplotlib as matplotlib

loader = DataLoader()

def per_field(field, users = None):
	
	if users == None:
		users = loader.fetch_data(field)

	post_sizes = {}
	post_sizes_counts = {}
	for user in users:
		size = user.avg_post_size
		if(size > 0 and size < 6000 ): 
			category = int(size) / 100 * 100
			if category not in post_sizes:
				post_sizes[category] = 0
			if category not in post_sizes_counts:
				post_sizes_counts[category] = 0
			post_sizes[category] += user.downvotes
			post_sizes_counts[category] += 1

	counts = []
	sizes = []
	downvotes = []
	

	for point in post_sizes:
		counts += [post_sizes_counts[point]]
		downvotes += [post_sizes[point]]
		sizes += [point]


	for i in range(0, len(downvotes)):
		downvotes[i] = downvotes[i] * 1.0 / counts[i]
	


	# turn counts to percentages
	#for i in range(0, len(downvotes)):
	#	downvotes[i] = downvotes[i] * 100.0 / total_count
	plt.bar(sizes, counts,  width=100)





def all(fields) :

	users = []
	for field in fields:
		users += loader.fetch_data(field)
	per_field("sth", users)
	plt.xlabel('Post size(characters)')
	plt.ylabel('Number of posts')
	plt.title('Post size distribution')
	#plt.legend(fields)
	plt.grid(True)
	plt.savefig("age-%s.png" % field)
	plt.show()

def one(field): 
	
	per_field(field)
	plt.xlabel('Post size(characters)')
	plt.ylabel('Number of posts')
	plt.title('Post size distribution')
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

