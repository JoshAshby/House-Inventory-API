"""
Basic math type implimentation for Python. Very basic, nothing fancy.

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""

#Don't ask... this error is just better than a standard raise
class MathError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		
class thorVector(object):
	def __init__(self, data):
		self.data = data
	
	def __repr__(self):
		return repr(self.data)
		
	def __getitem__(self, index):
		return self.data[index]

	def __len__(self):
		return len(self.data)
	
	def __add__(self, other):
		data = []
		if type(other) == self.__class__:
			for j in range(len(self.data)):
				data.append(self.data[j] + other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')
		
	def __sub__(self, other):
		data = []
		if len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] - other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')

	def __mul__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] * other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			result = None
			for j in range(len(self.data)):
				data.append(self.data[j] * other.data[j])
			for i in range(len(self.data)-1):
				result = data[i] + data [i-1]
			return self.__class__(result)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
	
	def __div__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] / other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] / other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
		
	def __pow__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] ** other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] ** other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
			
	def __radd__(self, other):
		data = []
		if type(other) == self.__class__:
			for j in range(len(self.data)):
				data.append(self.data[j] + other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')
		
	def __rsub__(self, other):
		data = []
		if len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] - other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')

	def __rmul__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] * other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			result = None
			for j in range(len(self.data)):
				data.append(self.data[j] * other.data[j])
			for i in range(len(self.data)-1):
				result = data[i] + data [i-1]
			return self.__class__(result)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
	
	def __rdiv__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] / other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] / other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
		
	def __rpow__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] ** other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] ** other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')