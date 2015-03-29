from kmeans.user import User
from kmeans.datapoint_loader import DataLoader
from pylab import *
import sys

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

	plot(age, count)

	xlabel('age')
	ylabel('# of users')
	title('Age distribution in %s ' % field)
	grid(True)
	savefig("age-%s.png" % field)
	show()


if len(sys.argv) != 2:
	print "Usage: <field name>"
	exit()

field = sys.argv[1]
age_in_field(field)

