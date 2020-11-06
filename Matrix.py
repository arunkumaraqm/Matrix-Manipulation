# Refer: https://pypi.org/project/multimethod/
# for multimethod docs
from multimethod import *

class Matrix:

	# Constructor overloading using decorators 
	# from third party library called multimethod
	@multimethod
	def __init__(self, 
				 rows: int, 
				 cols: int, 
				 fill_value = 0):
		self._rows = rows
		self._cols = cols
		self._grid = [[fill_value 
						for j in range(self._cols)] 
						for i in range(self._rows)]

	@__init__.register
	def __init__(self, 
				 mat: list):
		self._grid = mat
		self._rows = len(self._grid)
		self._cols = len(self._grid[0])
		return

	def __neg__(self): 
		# unary minus
		res = Matrix(self._rows, self._cols)
		for i in range(self._rows):
			for j in range(self._cols):
				res[i][j] = -self[i][j]
		return res

	# operator overloading
	def __add__(self, other):
		if self.dims != other.dims:
			raise ValueError("Matrices have different dimensions")

		summ = Matrix(self._rows, self._cols)
		for i in range(self._rows):
			for j in range(self._cols):
				summ[i][j] = self[i][j] + other[i][j]

		return summ

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		r1, c1 = self.dims
		r2, c2 = other.dims
		if c1 != r2:
			raise ValueError("Matrices not compatible for multiplication.")

		res = Matrix(r1, c2)
		for i in range(r1):
			for j in range(c2):
				for k in range(r2):
					res[i][j] += self[i][k] * other[k][j]
		return res

	def __getitem__(self, idx):	
		return self._grid[idx]
	
	def __setitem__(self, idx, val):
		self._grid[idx] = val

	def __str__(self):
		return '\n'.join(str(row) for row in self._grid) + '\n'

	def transpose(self):
		res = Matrix(self._cols, self._rows)

		for i in range(self._rows):
			for j in range(self._cols):
				res[j][i] = self[i][j] 

		return res

	@property
	def dims(self):
		return (self._rows, self._cols)


"""
# matmul test
mat1 = [
	[-1, 2, -3],
	[4, -5, 6],
]
mat2 = [
	[3, -4],
	[2, 1],
	[-1, 0],
]

one = Matrix(mat1)
two = Matrix(mat2)
print(one * two) 
print(Matrix([[4, 6], [-4, -21]]))
"""