from __future__ import division
from fractions import gcd
import math

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
      n.next = curr
      self.head = n
      return

    if curr.absD == absD:
      n = Node()
      n.absD = absD
      n.name = name
      n.execT = execT
      if int(curr.name[1]) > int(name[1]):
              n.next = curr
              self.head = n
              return
      while curr.next is not None:
        if int(curr.name[1]) > int(name[1]):
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

period = [3.0, 5.0, 8.0]
relD = [3.0, 5.0, 8.0]
execT = [1.0, 2.0, 3.0]
interval = 32
totUtil = 0.0
for i in range(0, len(period)):
#	print "%f / %f  = %f" % (execT[i], period[i], execT[i]/period[i])
	totUtil += (execT[i]/period[i])

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

r = 0.0
jobList = LinkedList() 
for i in range(0, interval+1):
	for j in range(0, len(period)):
		if(0 == (i % period[j])):
			vName = ("T"+ str(j+1) + "J" + str((i / period[j]) + 1))
			'''
			print i,j+1, i+relD[j], period[j],
			print "%s" % vName 
			'''
			jobList.addNode(i+relD[j], execT[j], vName)

	if jobList.head is not None:
		print "* Time %2d: %s: [%f, %d] " % (i, jobList.head.name, jobList.head.execT, jobList.head.absD), 
		print "-> Queue:",
		head = jobList.head
		while head is not None:
			print "%s[%f,%d]" % (head.name, (head.execT),(head.absD)),
			head = head.next

		r = 1
		while(r > 0):
			if(jobList.head is not None):
				if(jobList.head.execT >= r):
					jobList.head.execT -= r
					if(i >= jobList.head.absD):
						print "-> Deadline Missed ",
					if(0 == jobList.head.execT):
						jobList.removeHead()
					r = 0
				else:
					r -= jobList.head.execT
					if(i >= jobList.head.absD):
						print "-> Deadline Missed ",
					jobList.removeHead()
			else:
				r = 0
		print

		'''
		print "-> After Queue:",
		head = jobList.head
		while head is not None:
			print "%s[%f,%d]" % (head.name, (head.execT),(head.absD)),
			head = head.next
		print
		print
		'''
	else:
		print "* Time %2d: Queue is Empty" % (i), 
print "-------------------------------------"
print "* 1(d): EDF Reduction:",

period = [3.0, 5.0, 8.0]
relD = [3.0, 5.0, 8.0]
execT = [1.0, 2.0, 3.0]
totUtil = 0.0 
j = 0
while(1):
	totUtil = 0.0
	for i in range(0, len(period)):
	#	print "%f / %f  = %f" % (execT[i], period[i], execT[i]/period[i])
		totUtil += (execT[i]/period[i])
	if(abs(totUtil - 1) < 0.00000001):
		break
	else:
		execT[0] -= 0.001

print " Exec Time: %f, Util: %f" % (execT[0], totUtil)
print "-------------------------------------"
