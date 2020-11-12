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

	def adj(self):
		pass

	def inv(self):
		pass

if __name__ == '__main__':

	from numpy.linalg import det as npdet
	mat = SquareMatrix([
			[1, 2],
			[3, 4]
			])
	print(mat.det(), npdet(mat.to_nested_list()))

	mat = SquareMatrix([
			[1, 2, 3],
			[4, 5, 6],
			[7, 8, 9],
			])
	print(mat.det(), npdet(mat.to_nested_list()))

	mat = SquareMatrix([
			[1, 2, 4, 2],
			[3, 4, 93, 10],
			[28, 34, 12, 90],
			[29, 3, 0, 1],
			])
	print(mat.det(), npdet(mat.to_nested_list()))