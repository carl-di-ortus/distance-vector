#!/usr/bin/python3
import Router
import Packet
import sys

t = 0
printer = -1

#make the network
network = Router.Router(10, 10)

#initialize topology with neighbours
#distance to self = 0
#for i in range(10):
#	for j in range(10):
#		network.router[i].table[i][j] = 0
network.router[0].table[1][0] = 1
network.router[0].table[3][0] = 2
network.router[0].table[4][0] = 10
network.router[1].table[0][1] = 1
network.router[1].table[2][1] = 4
network.router[2].table[1][2] = 4
network.router[2].table[5][2] = 1
network.router[3].table[0][3] = 2
network.router[3].table[6][3] = 3
network.router[4].table[0][4] = 10
network.router[4].table[5][4] = 2
network.router[4].table[7][4] = 1
network.router[4].table[8][4] = 5
network.router[5].table[2][5] = 1
network.router[5].table[4][5] = 2
network.router[6].table[3][6] = 3
network.router[7].table[4][7] = 1
network.router[7].table[8][7] = 6
network.router[8].table[4][8] = 5
network.router[8].table[7][8] = 6

def getShortestPath(source, destination):
	if source == destination:
		return -1
	distance = -1
	for i in range(len(network.router[source].table)):
		if network.router[source].table[destination][i] > 0:
			if distance == -1:
				distance = network.router[source].table[destination][i]
			elif network.router[source].table[destination][i] < distance:
				distance = network.router[source].table[destination][i]
	return distance
	
def updatePendingChanges(t):
	for i in range(10):
		removable = []
		for j in range(len(network.router[i].pending)):
			destination = network.router[i].pending[j][1]
			through = network.router[i].pending[j][0]
			distance = network.router[i].pending[j][2]
			sent = network.router[i].pending[j][3]
			element = network.router[i].pending[j][:]
			if i == destination:
				removable.append(element)
				continue
			if network.router[i].table[through][i] == -1:
				#if can't reach through proxy
				network.router[i].table[destination][through] = -1
				removable.append(element)
				network.router[i].situationChanged = True
				continue
			if network.router[i].table[destination][through] == 0:
				removable.append(element)
				continue
			
			if t-sent >= network.router[i].table[through][i]:
				if network.router[i].table[destination][through] == -1:
					network.router[i].table[destination][through] = distance + network.router[i].table[through][i]
					removable.append(element)
					network.router[i].situationChanged = True
				elif network.router[i].table[destination][through] > distance:
					if network.router[i].table[destination][through] == distance + network.router[i].table[through][i]:
						removable.append(element)
						continue
					network.router[i].table[destination][through] = distance + network.router[i].table[through][i]
					removable.append(element)
					network.router[i].situationChanged = True
				#elif network.router[through].situationChanged:
				#	network.router[i].table[destination][through] = network.router[through].table[destination][through] + network.router[i].table[through][i] + distance
				#	network.router[i].situationChanged = True
				#elif network.router[i].situationChanged:
				#	network.router[i].table[destination][through] = distance + network.router[i].table[through][i] + network.router[through].table[destination][through]
				#	network.router[i].situationChanged = True
				else:
					network.router[i].table[destination][through] = distance + network.router[i].table[through][i]
					removable.append(element)
					network.router[i].situationChanged = True
		for k in range(len(removable)):
			network.router[i].pending.remove(removable[k])
	return

def broadcastVector(vector, t):
	if len(vector)==0:
		return
	toadd = list(vector)
	for j in range(len(toadd)):
		toadd[j].append(t)
	for i in range(len(vector)):
		source = vector[i][0]
		destination = vector[i][1]
		if network.router[destination].table[source][destination] > -1:
			for j in range(len(toadd)):
				network.router[destination].pending.append(toadd[j])

def increaseTime(t, printer=-1):
	for source in range(10):
		vector = []
		for destination in range(10):
			distance = getShortestPath(source, destination)
			if (distance>0):
				vector.append([source, destination, distance])
		if network.router[source].vector != vector:
			network.router[source].vector = vector[:]
			network.router[source].changeTime = t
			network.router[source].situationChanged = True
		else:
			network.router[source].situationChanged = False
	for i in range(10):
		# here should be a call to visual router table
		if network.router[i].situationChanged:
			broadcastVector(list(network.router[i].vector), t)
			network.router[i].situationChanged = False
	updatePendingChanges(t)
	# this should handle the time delay!
	if printer != -1:
		sys.stdout.write("\x1b[2J\x1b[H")
		print("System time: ", t)
		printTable(printer)
	return t+1

def changeLink(source, destination, distance):
	history = network.router[source].table[destination][source]
	network.router[source].situationChanged = True
	network.router[destination].situationChanged = True
	for i in range(10):
		if network.router[source].table[i][destination] > 0:
			network.router[source].table[i][destination] = network.router[source].table[i][destination] - history + 2*distance
		else:
			network.router[source].table[i][destination] = -1
		if network.router[destination].table[i][source] > 0:
			network.router[destination].table[i][source] = network.router[destination].table[i][source] - history + 2*distance
		else:
			network.router[destination].table[i][source] = -1
	network.router[source].table[destination][source] = distance
	network.router[destination].table[source][destination] = distance

def printTable(source):
	for destination in range(10):
		tmpTable = network.router[source].table[destination].copy()
		for i in range(10):
			if tmpTable[i]==-1:
				del tmpTable[i]
		print("Destination", destination, tmpTable)

def getTable(source, destination):
	tmpTable = network.router[source].table[destination].copy()
	for i in range(10):
		if tmpTable[i]==-1:
			del tmpTable[i]
	return tmpTable
		
def createPacket(source, destination, ttl):
	if source == destination:
		print("loopback packet")
	return Packet.Packet(source, destination, ttl)

def sendPacket(packet, t):
	if packet.source == packet.destination:
		print("packet is in place")
		return t
	table = getTable(packet.source, packet.destination)
	through = -1
	minTime = -1
	for key in table.keys():
		if minTime == -1:
			minTime = table[key]
		elif table[key] < minTime:
			minTime = table[key]
	for key in table.keys():
		if table[key] == minTime:
			through = key
	if through == -1 or minTime == -1:
		packet.timer += 1
		t = increaseTime(t)
		return t
	if through == packet.source:
		for i in range(network.router[packet.source].table[packet.destination][packet.source]):
			t = increaseTime(t)
			packet.timer += 1
			if packet.timer > packet.ttl:
				return t
		packet.source = packet.destination
	else:
		for i in range(network.router[packet.source].table[through][packet.source]):
			t = increaseTime(t)
			packet.timer += 1
			if packet.timer > packet.ttl:
				return t
		packet.source = through
	#if packet.source == packet.destination:
	#	print("packet reached the destination in time")
	#print("sys-time: ", t)
	return t
	
def traceRoute(packet, t):
	print("Source:", packet.source, "timer:", packet.timer)
	while packet.source != packet.destination and packet.timer < packet.ttl:
		t = sendPacket(packet, t)
		if packet.timer > packet.ttl:
			print("packet timeout")
		else:
			print("Hop to:", packet.source, "timer:", packet.timer)
	print("finish")
	return t

def skip(t, sec):
	for i in range(sec):
		t = increaseTime(t)
	return t
