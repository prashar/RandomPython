import hashlib 
import binascii
import bisect
import random 
import math

class Stats(object):
	def __init__(self):
		self.total = 0.0 
		self.values = []
		self._mean = None
		self._variance = None

	def add(self,value):
		self.values.append(float(value))
		self.total = self.total + float(value)
		self._mean = None
		self._variance = None

	def mean(self):
		if self._mean is None:
			self._mean = self.total / float(len(self.values))
		return self._mean 
	
	def variance(self):
		if self._variance is None:
			mean = self.mean()
			self._variance = 0.0 
			for value in self.values:
				diffval  = (value - mean) 
				self._variance = self._variance + (diffval * diffval)
			self._variance = self._variance / float(len(self.values) -1)
		return self._variance

	def stddev(self):
		return math.sqrt(self.variance())

class ConsistentHashTable(object):
	def __init__(self,nodelist):
		""" The object passed in would be a list of strings 'ABC' or 'BCD' or something """
		""" We will hash each string and store the (hash,name) as a tuple. """
		baselist = [(hashlib.md5(str(node)).digest(),node) for node in nodelist]
		""" Lets sort the list out so the hashed values are in sorted hex order """
		self.nodelist = sorted(baselist,key=lambda x: x[0])
		self.keylist = sorted(baselist,key=lambda x: x[1])
		self.hashlist = [hashnode[0] for hashnode in self.nodelist]

	def __str__(self):
		return ",".join("(%s, %s)\n" % (binascii.hexlify(nodeinfo[0]),nodeinfo[1])
				  for nodeinfo in self.nodelist)

	def find_nodes(self,key,count=1,avoid=None):
		""" Return a list of count nodes from the hashtable
		that have a higher hash than key's hash. The nodes chosen
		cannot be in the avoided list and returned list size has to less than count """
		if(avoid is None):
			avoid = set() 
		# Find the hash of the key we are looking at
		hash_value = hashlib.md5(str(key)).digest() 
		# Find the next highest value after hash_value
		init_index = bisect.bisect(self.hashlist,hash_value)
		next_index = init_index
		results = []
		avoided = []
		while(len(results) < count):
			""" wrap around the start """
			if(next_index == len(self.nodelist)):
				next_index=0 
			""" Get the actual string name of the node passed in """
			node = self.nodelist[next_index][1]
			if node in avoid:
				if node not in avoided:
					avoided.append(node)
			else:
				results.append(node)
			next_index = next_index + 1 
			if(next_index == init_index):
				""" terminate the loop """
				break 
		return results,avoided 

def GetWord():
	return (chr(ord('A') + random.randint(0,25))+
		 chr(ord('A') + random.randint(0,25)) +
		 chr(ord('A') + random.randint(0,25)))

def WordList(count):
	result = [] 
	while(len(result) < count):
		result.append(GetWord())
	return result 

def testDistribution(nodeset,hashtable,numkeys=1000):
	nodecount = dict([(node,0) for node in nodeset])
	for x in range(0,numkeys):
		node = hashtable.find_nodes(GetWord(),1)[0][0]
		nodecount[node] = nodecount[node] + 1 
	stats = Stats() 
	for node,count in nodecount.items():
		stats.add(count)
	print ("%d random hash keys assigned to %d nodes "
               "are distributed across the nodes "
               "with a standard deviation of %0.2f (compared to a mean of %d)." %
               (numkeys, len(nodeset), stats.stddev(), numkeys / len(nodeset)))

def Main():
	A = ['ABC','CDE','FGH']
	node_names = WordList(50)
	table = ConsistentHashTable(node_names) ;
	print(table)   
	#results,avoided = table.find_nodes('splurg',2) 
	#print(results)
	testDistribution(node_names,table) 
	

if __name__ == '__main__':
	Main() 