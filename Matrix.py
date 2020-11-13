"""
Contains the class Matrix
"""

# Refer: https://pypi.org/project/multimethod/
# for multimethod docs
from multimethod import *
from copy import deepcopy

class Matrix:

	"""
	A class for 2D matrices supporting basic matrix operations.
	Attributes:
		_rows (int)
		_cols (int)
		_grid (list of lists): contains the elements of the matrix
	"""

	# Constructor overloading using decorators 
	# from third party library called multimethod
	@multimethod
	def __init__(self, 
				 rows: int, 
				 cols: int, 
				 fill_value = 0):
		"""
		Constructor #1
		
		Args:
		    rows (int): no. of rows
		    cols (int): no. of columns
		    fill_value (int, optional): value to populate matrix with; defaults to 0
		"""
		self._rows = rows
		self._cols = cols
		self._grid = [[fill_value 
						for j in range(self._cols)] 
						for i in range(self._rows)]

	@__init__.register
	def __init__(self, 
				 mat: list):
		"""
		Constructor #2
		
		Args:
		    mat (list): a list of lists containing elements
		"""
		self._grid = deepcopy(mat)
		self._rows = len(self._grid)
		self._cols = len(self._grid[0])

	def __neg__(self): 
		"""
		Unary minus operator
		
		Returns:
		    Matrix
		"""
		res = Matrix(self._rows, self._cols)
		for i in range(self._rows):
			for j in range(self._cols):
				res[i][j] = -self[i][j]
		return res

	def __add__(self, other): 
		"""
		Addition operator.
		
		Args:
		    other (Matrix): Second operand
		
		Returns:
		    Matrix: sum
		
		Raises:
		    ValueError: Matrices have different dimensions
		"""
		if self.dims != other.dims:
			raise ValueError("Matrices have different dimensions")

		summ = Matrix(self._rows, self._cols)
		for i in range(self._rows):
			for j in range(self._cols):
				summ[i][j] = self[i][j] + other[i][j]

		return summ

	def __sub__(self, other):
		"""
		Subtraction operator.
		
		Args:
		    other (Matrix): Second operand
		
		Returns:
		    Matrix: difference
		
		Raises:
		    ValueError: Matrices have different dimensions
		"""
		return self + (-other)

	def __truediv__(self, scalar):
		"""
		Division operator.
		
		Args:
		    scalar (number)
		
		Returns:
		    Matrix: quotient
		
		Raises:
		    ZeroDivisionError: Cannot divide by zero.
		"""
		if scalar == 0:
			raise ZeroDivisionError("Cannot divide by zero.")
		res = Matrix(self._rows, self._cols)
		for i in range(self._rows):
			for j in range(self._cols):
				res[i][j] = self[i][j] / scalar
		return res

	def __mul__(self, other):
		"""
		Matrix Multiplication
		
		Args:
		    other (Matrix): Second operand
		
		Returns:
		    Matrix: product
		
		Raises:
		    ValueError: Matrices not compatible for multiplication.
		"""
		#TODO Scalar mul
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

	def __getitem__(self, idx: int):	
		"""
		
		Args:
		    idx (int): index
		
		Returns:
		    list: row indicated by idx
		"""
		return self._grid[idx]
	
	def __setitem__(self, idx: int, val):
		"""
		
		Args:
		    idx (int): index
		    val (number)
		"""
		self._grid[idx] = val

	def __repr__(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		return '\n'.join(str(row) for row in self._grid) + '\n'

	def transpose(self):
		"""
		Transpose of the matrix.
		
		Returns:
		    Matrix
		"""
		res = Matrix(self._cols, self._rows)

		for i in range(self._rows):
			for j in range(self._cols):
				res[j][i] = self[i][j] 

		return res

	def to_nested_list(self):
		"""
		
		Returns:
		    list: copy of _grid
		"""
		return deepcopy(self._grid)

	@property
	def dims(self):
		"""
		Dimensions
		
		Returns:
		    tuple
		"""
		return (self._rows, self._cols)