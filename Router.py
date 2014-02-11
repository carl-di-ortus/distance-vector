#!/usr/bin/python3
import RoutingTable

class Router:
	
	def __init__(self, quantity=0, tablesize=0):
		self.router = {}
		
		for i in range(quantity):
			self.router[i] = RoutingTable.RoutingTable(tablesize)
	
#	def broadcastVector(vector, t):
#		for k in range(len(vector)):
#			for l in range(len(vector)):
#				if network.router[vector[k][1]].table[vector[l][1]][vector[l][0]] == 0:
#					continue
#				elif network.router[vector[k][1]].table[vector[l][1]][vector[l][0]] == -1:
#					network.router[vector[k][1]].table[vector[l][1]][vector[l][0]] = vector[l][2] + network.router[vector[k][1]].table[vector[l][1]][vector[k][0]]
#				elif network.router[vector[k][1]].table[vector[l][1]][vector[l][0]] > vector[l][2]:
#					if vector[l][2] != -1:
#						network.router[vector[k][1]].table[vector[l][1]][vector[l][0]] = vector[l][2] + network.router[vector[k][1]].table[vector[l][1]][vector[k][0]]
	
