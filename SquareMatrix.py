from Matrix import * 
from itertools import permutations


class SquareMatrix(Matrix):
	
	@multimethod
	def __init__(self, 
				 rows: int, 
				 fill_value = 0):
		super().__init__(rows, rows, fill_value)

	@__init__.register
	def __init__(self, 
				 mat: list):
		super().__init__(mat)
		if self._rows != self._cols:
			raise ValueError("Input is not a square matrix")

	@classmethod
	def __idx_of_minimum(cls, lst):
		# Utility method for det
		return lst.index(min(lst))

	@classmethod
	def __parity_of_permutation(cls, lst):
		# Utility method for det
		# Returns +1 or -1 depending on the permutation `lst`
	    parity = 1
	    lst = list(lst)
	    for i in range(0,len(lst) - 1):
	        if lst[i] != i:
	            parity *= -1
	            mn = SquareMatrix.__idx_of_minimum(lst[i:]) + i
	            
	            lst[i], lst[mn] = lst[mn], lst[i]
	    return parity 

		
	def det(self):
		# Determinant using Leibnitz formula
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

	def __pow__(self, exponent):
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
		summ = 0
		for i in range(self._rows):
			summ += self._grid[i][i]
		return summ

	def minor(self, row_number, col_number):
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
		res = SquareMatrix(self._rows)
		for i in range(self._rows):
			for j in range(self._rows):
				res[i][j] = ((-1) ** (i + j)) * self.minor(j, i)
		return res

	def inv(self):
		determinant = self.det()
		if determinant:
			return self.adj() / determinant
		else:
			raise ValueError("Not Invertible")
