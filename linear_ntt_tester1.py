
from poly import Poly
from numpy.polynomial import polynomial 
import numpy
import common
import sys

def ntt_naive(p, root):
    """Compute forward (2n-1) NTT of n-coefficient polynomial.

    Compute pntt_i = sum_{j=0}^{n} p[j]*root^{ij} for 0 <= i < 2n-1

    Parameters
    ----------
    p : Poly
        input polynomial with n coefficients.
    root: int
        (2n-1)-th root of unity modulo q.
    Returns
    ----------
    Poly
        p evaluated at root^0, ..., root^(2n-2), i.e., p transformed into NTT domain.
    """
    q = p.q
    pntt = Poly.zero(2*p.n-1, q)
    for i in range(2*p.n-1):
        for j in range(p.n):
            pntt.coeffs[i] = (pntt.coeffs[i] +  p.coeffs[j]*pow(root, i*j, q)) % q
    return pntt
def ntt_naive_nopad(p, root):
    """Compute forward (2n-1) NTT of n-coefficient polynomial.

    Compute pntt_i = sum_{j=0}^{n} p[j]*root^{ij} for 0 <= i < 2n-1

    Parameters
    ----------
    p : Poly
        input polynomial with n coefficients.
    root: int
        (2n-1)-th root of unity modulo q.
    Returns
    ----------
    Poly
        p evaluated at root^0, ..., root^(2n-2), i.e., p transformed into NTT domain.
    """
    q = p.q
    pntt = Poly.zero(p.n, q)
    for i in range(p.n):
        for j in range(p.n):
            pntt.coeffs[i] = (pntt.coeffs[i] +  p.coeffs[j]*pow(root, i*j, q)) % q
    return pntt


def invntt_naive(pntt, root):
    """Compute inverse NTT.

    Note that the inputs here are in NTT domain, i.e., have (2n-1) coefficients.

    Compute p_i =  1/n * sum_{j=0}^{2n-1} pntt[j]*root^{-ij} for 0 <= i < 2n-1

    Parameters
    ----------
    pntt : Poly
        input in NTT domain, i.e., evaluation of p at root^0, ..., root^(2n-2).
    root: int
        (2n-1)-th root of unity modulo q.
    Returns
    ----------
    Poly
        p in normal domain.
    """
    # pntt is already padded, i.e., pntt.n is 2*a.n-1
    q = pntt.q
    p = Poly.zero(pntt.n, q)
    for i in range(pntt.n):
        for j in range(pntt.n):
            p.coeffs[i] = (p.coeffs[i] + pntt.coeffs[j]*pow(root, -i*j, q)) % q

    ninv = pow(p.n, -1, q)
    for i in range(p.n):
        p.coeffs[i] = (p.coeffs[i] * ninv) % q
    return p


def polymul_ntt(a, b):
    """Perform NTT-based multiplication of two polynomials in the ring Zq[x].

    For computing the product we evaluate the n-coefficient polynomials and b
    at (2n-1) powers of a (2n-1)-th root of unity, then multiply coefficient wise,
    and interpolate the product using the inverse NTT.
    Primitive (2n-1)-th root of unity modulo q needs to exist.

    Parameters
    ----------
    a : Poly
        first multiplicand with n coefficients.
    b : Poly
        second multiplicand with n coefficients.
    Returns
    ----------
    Poly
        product a*b with 2n-1 coefficients.
    """
    assert a.n == b.n
    assert a.q == b.q
    n = a.n
    q = a.q
    assert common.isPrime(q)
    assert ((q-1) % (2*n-1)) == 0

    # For implementing a general purpose NTT (not cyclic, negacyclic), we need
    # to evaluate a and b at 2n-1 roots of unity.

    # we need a 2n-th root of unity
    root = common.primitiveRootOfUnity(2*n-1, q)

    # transform a and b to NTT domain
    antt = ntt_naive(a, root)
    bntt = ntt_naive(b, root)

    # point-wise multiplication
    cntt = antt.pointwise(bntt)

    # trnasform the result back to normal domain
    c = invntt_naive(cntt, root)

    return c

if __name__ == "__main__":
    # Consider polynomials a and b
    # Coeffiecients are in reverse order (a0, a1, a2, ...)
    # q is the size of the field (N)
    # n-1 is the degree of the polynomials
    # q has the condition that  ( q - 1 ) % (2n - 1) is 0, i.e. ( 2n - 1 ) is a factor of ( q - 1 )
    # Additionally, q has to be a prime
    coeff_a = [3,2,1]
    coeff_b = [0,1,1]
    a = Poly(coeff_a, q=11)
    b = Poly(coeff_b, q=11)

    print("a(x) =", a)
    print("b(x) =", b)

    root = common.primitiveRootOfUnity(2*a.n-1, a.q)
    print("Root used =", root)

    print("a(x) (evaluation domain) or NTT Domain =", ntt_naive(a, root))
    print("b(x) (evaluation domain) or NTT Domain =", ntt_naive(b, root))
    print("a(x) (evaluation domain) or NTT Domain without padding =", ntt_naive_nopad(a, root))
    print("b(x) (evaluation domain) or NTT Domain withut padding=", ntt_naive_nopad(b, root))

    result = polymul_ntt(a, b)
    result_norm = polynomial.polymul(tuple(coeff_a[::-1]),tuple(coeff_b[::-1]))
    print("Result =", result)
    print(f" with normal poly mul {result_norm}")