from fractions import gcd
import math
class Node:
  def __init__(self):
    self.name = None
    self.period = 0
    self.absD = 0
    self.execT = 0
    self.next = None

class LinkedList:
  def __init__(self):
    self.head = None

  def addNode(self, period, absD, execT, name):
    curr = self.head
    if curr is None:
      n = Node()
      n.absD = absD
      n.period = period
      n.name = name
      n.execT = execT
      self.head = n
      return

    if curr.period > period:
      n = Node()
      n.absD = absD
      n.period = period
      n.name = name
      n.execT = execT
      n.next = curr
      self.head = n
      return

    if curr.period == period:
      n = Node()
      n.absD = absD
      n.period = period
      n.name = name
      n.execT = execT
      if int(curr.name[1]) > int(name[1]):
              n.next = curr
              self.head = n
              return
      elif int(curr.name[1]) < int(name[1]):
	      while curr.next is not None:
		if int(curr.name[1]) > int(name[1]):
		  break
		curr = curr.next
	      n.next = curr.next
	      curr.next = n
	      return

      while curr.next is not None:
        if int(curr.name[3:]) > int(name[3:]):
          break
        curr = curr.next
      n.next = curr.next
      curr.next = n
      return

    while curr.next is not None:
      if curr.next.period > period:
        break
      if curr.next.period == period:
        if int(curr.next.name[3:]) > int(name[3:]):
		break
      curr = curr.next

	
    n = Node()
    n.absD = absD
    n.period = period
    n.name = name
    n.execT = execT
    n.next = curr.next
    curr.next = n
    return

  def removeHead(self):
    curr = self.head
    self.head = curr.next

period = [3, 5, 8]
relD = [3, 5, 8]
execT = [1, 2, 3]
interval = 32

print "-------------------------------------"
print "* 1(c): RM Schedule"
print "-------------------------------------"
for i in range(1, len(period)+1):
        vNum = interval / period[i-1]
	if(0 != (interval % period[i-1])):
		vNum+=1
        for j in range(0, vNum):
                vName = "T" + str(i) + "J" + str(j+1)
	#	print " %s" % vName,
#	print

jobList = LinkedList() 
for i in range(0, interval+1):
	for j in range(0, len(period)):
		if(0 == (i % period[j])):
			vName = ("T"+ str(j+1) + "J" + str((i / period[j]) + 1))
			'''
			print i,j+1, i+relD[j], period[j],
			print "%s" % vName 
			'''
			jobList.addNode(period[j], i+relD[j], execT[j], vName)

	head = jobList.head
	print "* Time %2d: %s: [%d, %d] " % (i, head.name, head.execT, head.absD), 
	if(i >= head.absD):
		print "-> Deadline Missed ",
	print "-> Queue:",
	while head is not None:
		print "%s[%d,%d]" % (head.name, (head.execT),(head.absD)),
		head = head.next
	print
	head = jobList.head
	head.execT -= 1
	if(0 == head.execT):
		jobList.removeHead()

print "-------------------------------------"
