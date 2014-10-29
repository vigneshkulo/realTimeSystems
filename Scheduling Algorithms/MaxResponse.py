from __future__ import division
from fractions import gcd
import math

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
executionTime = []
relativeDeadline = []

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

vNum = 0

for i in range(1, len(period)+1):
	vNum = int(hyperPeriod / period[i-1])
	for j in range(0, vNum):
		vName = "Task" + str(i) + "Job" + str(j+1)
	#	print vName

print "-------------------------------------"

class Node:
  def __init__(self):
    self.name = None
    self.absD = None
    self.execT = 0.0
    self.next = None

class LinkedList:
  def __init__(self):
    self.head = None

  def addNode(self, absD, execT, name):
    curr = self.head
    if curr is None:
      n = Node()
      n.absD = absD
      n.name = name
      n.execT = execT
      self.head = n
      return

    if curr.absD > absD:
      n = Node()
      n.absD = absD
      n.name = name
      n.execT = execT
      if int(curr.name[1:curr.name.index('J')]) > int(name[1:name.index('J')]):
              n.next = curr
              self.head = n
              return
      while curr.next is not None:
        if int(curr.name[1:curr.name.index('J')]) > int(name[1:name.index('J')]):
          break
        curr = curr.next
      n.next = curr.next
      curr.next = n
      return

    if curr.absD == absD:
      n = Node()
      n.absD = absD
      n.name = name
      n.execT = execT
      if int(curr.name[1:curr.name.index('J')]) > int(name[1:name.index('J')]):
              n.next = curr
              self.head = n
              return
      while curr.next is not None:
        if int(curr.name[1:curr.name.index('J')]) > int(name[1:name.index('J')]):
          break
        curr = curr.next
      n.next = curr.next
      curr.next = n
      return

    while curr.next is not None:
      if curr.next.absD > absD:
        break
      if curr.next.absD == absD:
	break
      curr = curr.next
    n = Node()
    n.absD = absD
    n.name = name
    n.execT = execT
    n.next = curr.next
    curr.next = n
    return

  def removeHead(self):
    curr = self.head
    self.head = curr.next
'''
period = [3.0, 5.0, 8.0]
relD = [3.0, 5.0, 8.0]
execT = [1.0, 2.0, 3.0]
'''
interval = hyperPeriod
interval = 1000
totUtil = 0.0
for i in range(0, len(period)):
#	print "%f / %f  = %f" % (executionTime[i], period[i], executionTime[i]/period[i])
	totUtil += (executionTime[i]/period[i])

print "-------------------------------------"
print "* 1(a): Total Utilization: %f" %(totUtil)
print "-------------------------------------"
for i in range(1, len(period)+1):
        vNum = int(interval / period[i-1])
	if(0 != (interval % period[i-1])):
		vNum+=1
	print "* Task %d: " % i,
        for j in range(0, vNum):
                vName = "T" + str(i) + "J" + str(j+1)
		print " %s" % vName,
	print
print "-------------------------------------"
print "* 1(b): EDF Schedule"
print "-------------------------------------"

maxResp = [0.0 for i in range(len(period))] 
r = 0.0
jobList = LinkedList() 
for i in range(0, interval+1):
	for j in range(0, len(period)):
		if(0 == (i % period[j])):
			vName = ("T"+ str(j+1) + "J" + str(int(i / period[j]) + 1))
			'''
			print i,j+1, i+relativeDeadline[j], period[j],
			print "%s" % vName 
			'''
			jobList.addNode(i+relativeDeadline[j], executionTime[j], vName)

	if jobList.head is not None:
	#	print "* Time %2d: %s: [%f, %d] " % (i, jobList.head.name, jobList.head.execT, jobList.head.absD), 
	#	print "-> Queue:",
		head = jobList.head
		while head is not None:
	#		print "%s[%f,%d]" % (head.name, (head.execT),(head.absD)),
			head = head.next

		r = 1
		while(r > 0):
			if(jobList.head is not None):
				if(jobList.head.execT >= r):
					jobList.head.execT -= r
	#				if(i >= jobList.head.absD):
	#					print "-> Deadline Missed ",
					if(0 == jobList.head.execT):
						start = (int(jobList.head.name[jobList.head.name.index('J')+1:])-1) * period[int(jobList.head.name[1:jobList.head.name.index('J')]) - 1]
						maxResp[int(jobList.head.name[1:jobList.head.name.index('J')]) - 1] = max(maxResp[int(jobList.head.name[1:jobList.head.name.index('J')]) - 1], (i-start))
						jobList.removeHead()
					r = 0
				else:
					r -= jobList.head.execT
	#				if(i >= jobList.head.absD):
	#					print "-> Deadline Missed ",
					start = (int(jobList.head.name[jobList.head.name.index('J')+1:])-1) * period[int(jobList.head.name[1:jobList.head.name.index('J')]) - 1]
					maxResp[int(jobList.head.name[1:jobList.head.name.index('J')]) - 1] = max(maxResp[int(jobList.head.name[1:jobList.head.name.index('J')]) - 1], (i-start))
					jobList.removeHead()
			else:
				r = 0
	#	print
#	else:
	#	print "* Time %2d: Queue is Empty" % (i) 

print "-------------------------------------"
print maxResp
