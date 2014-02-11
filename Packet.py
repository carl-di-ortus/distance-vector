#!/usr/bin/python3

class Packet:
	
	def __init__(self, source, destination, ttl):
		self.source = source
		self.destination = destination
		self.ttl = ttl
		self.timer = 0
