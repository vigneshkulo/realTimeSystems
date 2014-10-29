from fractions import gcd
import math

fp = open('HW1table1.txt', 'r')
hyperPeriod = 0
status = 0
maxExec = 0 
totalUtil = 0 

i = 0
relativeDeadline = []
executionTime = []
period = []
initF = []
frameL = []
frameArray = []

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

	relativeDeadline.append(int(D))
	period.append(int(p))
	executionTime.append(float(e))

	if float(e) > maxExec:
		maxExec = float(e)
	util = float(e)/float(p)
	totalUtil += util
	i+=1
	print " Task %02d: " % i, util

print "-------------------------------------"
print "* Part B: Total Util   : ", totalUtil

def lcm(*numbers):
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, numbers, 1)

hyperPeriod = lcm(*period)
print "* Part C: Hyper Period : ", hyperPeriod

for i in range(1, int(hyperPeriod)+1):
	if( hyperPeriod % i == 0):
		frameL.append(i)	

for f in frameL:
	status = 0
	for i in range(0, len(period)):
	#	print "* Frame Size:", f,
	#	print ": (2 * %4d) - gcd(%4d, %4d) <= %4d" % (f, period[i], f, relativeDeadline[i]),
	#	print ": %4d - %4d <= %4d" % ((2*f), gcd(period[i], f), relativeDeadline[i]),
		if(not((2*f - gcd(period[i], f)) <= relativeDeadline[i])):
			status = 1
	#		print " -> False"
	#	else:
	#		print " -> True"
#	print
	if(0 == status):
		frameArray.append(f)	

for f in frameArray:
	if(f >= maxExec):	
		initF.append(f)

print "* Part D(A): Frame Sizes for after all Constraints:", initF 
print "* Part D(B): Frame Sizes for INF Constraints only :", frameArray 
print "-------------------------------------"

def BFS(C, F, source, sink):
    queue = [source]         # the BFS queue                 
    paths = {source: []}     # 1 path ending in the key
    while queue:

        u = queue.pop(0)     # next node to explore (expand) 
        for v in range(len(C)):   # for each possible next node
 
            # path from u to v?     and   not yet at v?
            if C[u][v] - F[u][v] > 0 and v not in paths:
                 paths[v] = paths[u] + [(u,v)]
                 if v == sink:
                      return paths[v]  # path ends in the key!

                 queue.append(v)   # go from v in the future 
    return None

def max_flow(C, source, sink):
    n = len(C) # C is the capacity matrix
    F = [[0] * n for i in range(n)] # F is the flow matrix
    # residual capacity from u to v is C[u][v] - F[u][v]

    while True:
        path = BFS(C, F, source, sink)
        if not path: break   # no path - we're done!

        edge_flows = [C[u][v]-F[u][v] for u,v in path]
        path_flow = min( edge_flows )
       
       # print "Augmenting by", path_flow
        for u,v in path: # traverse path to update flow
            F[u][v] += path_flow     # forward edge up 
            F[v][u] -= path_flow     # backward edge down 

    return sum([F[source][i] for i in range(n)])

for f in reversed(frameArray):
	fList = []
	vList = []

	fNum = hyperPeriod / f

	# Includes Source and Sink Initially
	totVer = 2  

	for i in range(1, len(period)+1):
		vNum = hyperPeriod / period[i-1]
		for j in range(0, vNum):
			totVer += 1

	totVer += fNum

	adjMat  = [[0 for i in range(totVer)] for j in range(totVer)]

	totalExec = 0
	for i in range(1, len(period)+1):
		vNum = hyperPeriod / period[i-1]
		for j in range(0, vNum):
			vName = "Task" + str(i) + "Job" + str(j+1)
			totalExec += executionTime[i-1]
		#	print "* %s : adj[%d][%d] = %f" % (vName, 0, len(vList) + 1, executionTime[i-1])
			adjMat[0][len(vList) + 1] = executionTime[i-1]
			vList.append(vName)

	for i in range(0, fNum):
		fName = "Frame" + str(i+1)
		fList.append(fName)
	#	print "* %s : adj[%d][%d] = %d" % (fName, len(vList) + i + 1, len(vList) + 1 + fNum, f)
		adjMat[len(vList) + i + 1][len(vList) + 1 + fNum] = f


	start = 0
	deadline = 0
	print "* Part E: "
	print "* Frame Size     :", f,
	print ", #Job Vertices  : ", len(vList),
	print ", #Frame Vertices: ", len(fList),
	print ", #Total Vertices: ", totVer

	for i in range(1, len(period)+1):
		vNum = hyperPeriod / period[i-1]
		for j in range(0, vNum):
			vName = "Task" + str(i) + "Job" + str(j+1)
			startJ = j * period[i-1]
			deadlineJ = startJ + relativeDeadline[i-1]
		#       print "* Job %s: [%d to %d]" % (vName, startJ, deadlineJ)
			for k in range(0, fNum):
				fName = "Frame" + str(k+1)
				startF = k * f
				deadlineF = startF + f
				if((startJ <= startF) and (deadlineJ >= deadlineF)):
				#	print "%s -> %s" % (vName, fName),
				#	print ": adj[%d][%d]" % (vList.index(vName)+1, len(vList) + fList.index(fName)+1)
				#	fOut.write("%s Scheduled in %s\n" % (vName, fName))
					adjMat[vList.index(vName)+1][len(vList) + fList.index(fName)+1] = f

	'''
	print '-' * 40
	print "* Adjacency Matrix: "
	for i in range(totVer):
		for j in range(totVer):
			print "%f" % adjMat[i][j], " ",
		print ""

	print '-' * 40
	'''

	source = 0  # s
	sink = totVer - 1    # t

	max_flow_value = max_flow( adjMat, source, sink )
	print "* Max flow: ", max_flow_value
	print "* Tot Exec: ", totalExec
	if(totalExec == max_flow_value):
		print "* Max Flow Attained"
	else:
		print "* Max Flow Not Attained"
	print '-' * 40
