"""
Contains the class SquareMatrix
"""
from Matrix import * 
from itertools import permutations # for det method
from typing import Iterable # for function annotation

class SquareMatrix(Matrix):

	"""
	A class for 2D square matrices supporting basic square matrix operations.
	Attributes:
		_rows (int)
		_cols (int): always equal to _rows
		_grid (list of lists): contains the elements of the matrix
	"""
	
	# Constructor overloading using decorators 
	# from third party library called multimethod
	@multimethod
	def __init__(self, 
				 rows: int, 
				 fill_value = 0):
		"""
		Constructor #1
		
		Args:
		    rows (int): no. of rows
		    fill_value (int, optional): value to populate matrix with; defaults to 0
		"""
		super().__init__(rows, rows, fill_value)

	@__init__.register
	def __init__(self, 
				 mat: list):
		"""
		Constructor #2
		
		Args:
		    mat (list): a list of lists containing elements
		
		Raises:
			ValueError: Input is not a square matrix
		"""
		super().__init__(mat)
		if self._rows != self._cols:
			raise ValueError("Input is not a square matrix")

	@classmethod
	def __idx_of_minimum(cls, lst: list) -> int:
		"""
		Utility method for det
		
		Args:
		    lst (list) 
		
		Returns:
		    int: index of minimum
		"""
		return lst.index(min(lst))

	@classmethod
	def __parity_of_permutation(cls, lst: Iterable) -> int:
		"""
		Utility method for det
		
		Args:
		    lst (Iterable): a permutation
		
		Returns:
		    int: +1 or -1 depending on the permutation `lst`
		"""
		parity = 1
		lst = list(lst)
		for i in range(0, len(lst) - 1):
			if lst[i] != i:
				parity *= -1
				mn = SquareMatrix.__idx_of_minimum(lst[i:]) + i
				
				lst[i], lst[mn] = lst[mn], lst[i]
		return parity 

		
	def det(self):
		"""
		Determinant using Leibnitz formula
		https://en.wikipedia.org/wiki/Leibniz_formula_for_determinants
		Returns:
			number
		"""
		
		rows = self._rows
		sign = +1
		summ = 0

		for perm in permutations(range(rows), rows):
			mul = 1
			sign = SquareMatrix.__parity_of_permutation(perm)

			for i in range(rows):
				mul *= self[i][perm[i]]

			summ += sign * mul
		return summ

	def __pow__(self, exponent: int):
		"""
		Power using matrix multiplication
		
		Args:
			exponent (int)
		
		Returns:
			SquareMatrix
		
		Raises:
			ValueError: Negative powers not supported
		"""
		if exponent < 0:
			raise ValueError("Negative powers not supported")
		elif exponent == 0:
			return SquareMatrix(self._rows, 1)
		else:
			res = self
			for i in range(1, exponent):
				res *= self
			return res

	def trace(self):
		"""
		
		Returns:
			number: sum of diagonal elements
		"""
		summ = 0
		for i in range(self._rows):
			summ += self._grid[i][i]
		return summ

	def minor(self, row_number: int, col_number: int):
		"""
		Minor of the matrix about (row_number, col_number)
		
		Args:
			row_number (int): row to delete
			col_number (int): col to delete
		
		Returns:
			SquareMatrix: of row size one less than self
		
		Raises:
			IndexError: One or both indices out of range
		"""
		if 	not(0 <= row_number < self._rows) or \
			not(0 <= col_number < self._cols): 
			raise IndexError("One or both indices out of range.")

		submat = SquareMatrix(self._rows - 1)

		# submat = self without row `row_number` and col `col_number`
		included_row_nos = list(range(self._rows)); del included_row_nos[row_number]
		included_col_nos = list(range(self._cols)); del included_col_nos[col_number]

		for i_submat, i_mat in zip(range(submat._rows), iter(included_row_nos)):
			for j_submat, j_mat in zip(range(submat._rows), iter(included_col_nos)):
				submat[i_submat][j_submat] = self[i_mat][j_mat]
		
		return submat.det()


	def adj(self):
		"""
		Adjugate of the matrix
		res[i][j] = ((-1) ** (i + j)) * mat.minor(j, i)
		
		Returns:
			SquareMatrix
		"""
		res = SquareMatrix(self._rows)
		for i in range(self._rows):
			for j in range(self._rows):
				res[i][j] = ((-1) ** (i + j)) * self.minor(j, i)
		return res

	def inv(self):
		"""
		Inverse of the matrix = Adjugate / Determinant
		
		Returns:
			SquareMatrix
		
		Raises:
			ValueError: Not Invertible (when determinant = 0)
		"""
		determinant = self.det()
		if determinant:
			return self.adj() / determinant
		else:
			raise ValueError("Not Invertible")

if __name__ == '__main__':
	help(SquareMatrix.trace)