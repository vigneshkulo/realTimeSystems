import math
from fractions import gcd

fp = open('HW1table1.txt', 'r')

i = 0
status = 0
maxExec = 0 
totalUtil = 0 
hyperPeriod = 0

period = []
initF = []
frameL = []
frameArray = []
execT = []
relD = []

print "-----------------------------"
print "* Part A: Utilization of task"
print "-----------------------------"
for line in fp:
	data = line.split()
	D = data[4]
	e = data[3]
	p = data[2]
	e = e[:-1]
	p = p[:-1]

	relD.append(int(D))
	period.append(int(p))
	execT.append(float(e))

	if float(e) > maxExec:
		maxExec = float(e)
	util = float(e)/float(p)
	totalUtil += util
	i+=1
	print " Task %02d: " % i, util
'''
print "-------------------------------------"
print "* Part B: Total Util   : ", totalUtil
period = [10.0, 12.0, 25.0]
relD = [10.0, 12.0, 25.0]
execT = [2, 4.5, 9.0]
'''
'''
period = [3.0, 5.0, 8.0]
relD = [3.0, 5.0, 8.0]
execT = [0.625, 2.0, 3.0]
period = [5.0, 3.0, 7.0, 16.0]
relD = [5.0, 3.0, 7.0, 16.0]
execT = [1, 1, 2.5, 1]
'''
'''
period = [10.0, 12.0, 25.0]
relD = [10.0, 12.0, 25.0]
execT = [1.0, 6.0, 9.0]
period = [10.0, 12.0, 25.0]
relD = [10.0, 12.0, 20.0]
execT = [2.0, 6.0, 9.0]
'''
totUtil = 0.0

j = 0
w = []
t = []
print "-------------------------------------"
print "* Possible t values"
print "-------------------------------------"

for i in range(1, len(period)+1):
#	print "I: %d ->" % i,
	for k in range(1, i+1):
		for j in range(1, int(math.floor(min(period[i-1], relD[i-1])/period[k-1])) + 1):
			t.append(j*period[k-1])
#			print "[[%d, %d] -> (t = %.3f)]" % (k, j, j*period[k-1]),
#	print

t = list(set(t))
t.sort()
t = [int(i) for i in t]
print t
print "-------------------------------------"
for i in range(1, len(period)+1):
	for t1 in t:
	#	print "* t =", t1
		if(t1 > relD[i-1]):
			continue
		tot = 0
		w.append(execT[i-1])
		tot += execT[i-1] 
		#print "* w%d(%d) = %.3f" % (i, t1, execT[i-1]),
		print "* w%d(%d)" % (i, t1),
		for k in range(1, i):
			tot += (math.ceil(t1/period[k-1]) * execT[k-1])
		#	print "+ (ceil(%d/%.3f) * %.3f)" % (t1, period[k-1], execT[k-1]),
		print "= %f <= %.3f" % (tot, t1),
		if(tot > t1):
			print "-> Violation",
		print
	print "-------------------------------------"
