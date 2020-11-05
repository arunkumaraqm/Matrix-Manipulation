class Matrix:

	# constructor
	def __init__(self, rows, cols, fill_value = 0):
		self.rows = rows
		self.cols = cols
		self.grid = [[fill_value 
						for j in range(self.cols)] 
						for i in range(self.rows)]

	def __neg__(self): 
		# unary minus
		res = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				res[i][j] = -self[i][j]
		return res

	# operator overloading
	def __add__(self, other):
		if self.rows != other.rows or self.cols != other.cols:
			raise ValueError("Matrices have different dimensions")

		summ = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				summ[i][j] = self[i][j] + other[i][j]

		return summ

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		pass # exception handlling when
		# matrices not multipliable

	def __getitem__(self, idx):
		return self.grid[idx]
	
	def __setitem__(self, idx, val):
		self.grid[idx] = val

	def __str__(self):
		return '\n'.join(str(row) for row in self.grid) + '\n'

	def transpose(self):
		res = Matrix(self.cols, self.rows)

		for i in range(self.rows):
			for j in range(self.cols):
				res[j][i] = self[i][j] 

		return res


class SquareMatrix(Matrix):
	def __init__(self, rows, fill_value = 0):
		pass

	def det(self):
		pass

	def pow(self, exponent):
		pass

	def trace(self):
		pass

	def adj(self):
		pass

	def inv(self):
		pass


one = Matrix(2,3, 2)
two = Matrix(2,3, -100)
one[1][2] = 5
one += two
print(one)
