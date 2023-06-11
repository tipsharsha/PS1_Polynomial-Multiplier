"""wdwa"""
from numpy.polynomial import polynomial 
p1 = (8,6,8,7,4,8,8,11)
p2 =(10,12,15,3,3,7,3,15)
coeff_a =[3, 2, 1]
coeff_b = [0, 1, 1]
result_norm = polynomial.polymul(tuple(coeff_a[::-1]),tuple(coeff_b[::-1]))
print(result_norm)
