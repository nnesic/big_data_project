from user import User
from datapoint_loader import DataLoader
from pylab import *

loader = DataLoader()

def age_vs_reputation_in_field(field):
	users = loader.fetch_data(age_in_field)
	
	for user in users:
		if user.age not in points:
			points[user.age] = 0
		points[user.age] += 1

	age = []
	reputation = []
	for point in points:
		if point >= 13:
			age += [point]
			reputation += [points[point]]

	plot(age, reputation)

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
age_vs_reputation_in_field(field)

