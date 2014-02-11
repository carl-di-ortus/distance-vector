#!/usr/bin/python3

class RoutingTable:
	
	def __init__(self, tablesize=0):
		self.table = {}
		self.situationChanged = True
		self.vector = []
		self.changeTime = 0
		self.pending = []
		
		for i in range(tablesize):
			# destination
			self.table[i] = {}
			
			for j in range(tablesize):
				# via
				self.table[i][j] = -1
	
