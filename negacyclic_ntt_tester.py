
from numpy.polynomial import polynomial 
from poly import Poly
import common

def ntt_naive(p, root):
    """Compute forward negacyclic n-NTT of n-coefficient polynomial.

       Compute pntt_i = sum_{j=0}^{n} p[j]*root^{j}*root^{2ij} for 0 <= i < n.
    This is the same as first twisting to Zq[x]/(x^n-1) and then performing a cyclic NTT.

    Parameters
    ----------
    p : Poly
        input polynomial with n coefficients.
    root: int
        2n-th root of unity modulo q.
    Returns
    ----------
    Poly
        p in NTT domain.
    """
    q = p.q
    pntt = Poly.zero(p.n, q)
    for i in range(p.n):
        for j in range(p.n):
            pntt.coeffs[i] = (pntt.coeffs[i] +  p.coeffs[j]*pow(root, j, q)*pow(root, 2*i*j, q)) % q
    return pntt

def invntt_naive(pntt, root):
    """Compute negacyclic inverse NTT.

    Compute p_i =  1/n * root^{-i} * sum_{j=0}^{n} pntt[j]*root^{-2ij} for 0 <= i < n

    Parameters
    ----------
    pntt : Poly
        input in NTT domain.
    root: int
        2n-th root of unity modulo q.
    Returns
    ----------
    Poly
        p in normal domain.
    """
    q = pntt.q
    p = Poly.zero(pntt.n, q)
    for i in range(pntt.n):
        for j in range(pntt.n):
            p.coeffs[i] = (p.coeffs[i] + pntt.coeffs[j]*pow(root, -2*i*j, q)) % q
    ninv = pow(p.n, -1, q)
    for i in range(p.n):
        p.coeffs[i] = (p.coeffs[i] * ninv * pow(root, -i, q)) % q
    return p

def polymul_negacyclic_ntt(a, b):
    """Perform NTT-based multiplication of two polynomials in the ring Zq[x]/(x^n+1), i.e., negacyclic.

    For computing the product, we first twist a and b to Zq[x]/(x^n-1) by
    multiplying by powers of the 2n-th root of unity,
    then evaluate at n powers of a n-th root of unity,
    then multiply coefficient-wise,
    then interpolate the product using the inverse NTT,
    then twist back to Zq[x]/(x^n+1) by multiplying by power of the inverse
    2n-th root of unity.
    Primitive 2n-th (and consequently, n-th) root of unity modulo q needs to exist.

    Parameters
    ----------
    a : Poly
        first multiplicand with n coefficients.
    b : Poly
        second multiplicand with n coefficients.
    Returns
    ----------
    Poly
        product a*b with n coefficients.
    """
    assert a.n == b.n
    assert a.q == b.q
    n = a.n
    q = a.q
    assert common.isPrime(q)
    # We need a 2n-th root of unity rather than an n-th root of unity
    assert ((q-1) % (2*n)) == 0

    # we need a n-th root of unity
    root = common.primitiveRootOfUnity(2*n, q)

    # transform a and b to NTT domain
    antt = ntt_naive(a, root)
    bntt = ntt_naive(b, root)

    # point-wise multiplication
    cntt = antt.pointwise(bntt)

    # transform the result back to normal domain
    c = invntt_naive(cntt, root)

    return c

if __name__ == "__main__":
    # Consider polynomials a and b
    # Coeffiecients are in reverse order (a0, a1, a2, ...)
    # q is the size of the field (N)
    # n-1 is the degree of the polynomials
    # q has the condition that  ( q - 1 ) % 2n is 0, i.e. 2n is a factor of ( q - 1 )
    # Additionaly, q has to be a prime number
    coeff_a =[3, 2, 1]
    coeff_b = [0, 1, 1]
    a = Poly(coeff_a, q=7)
    b = Poly(coeff_b, q=7)

    print("a(x) =", a)
    print("b(x) =", b)

    root = common.primitiveRootOfUnity(2*a.n, a.q)
    print("Root used =", root)

    print("a(x) (evaluation domain) or NTT Domain =", ntt_naive(a, root))
    print("b(x) (evaluation domain) or NTT Domain =", ntt_naive(b, root))
    # print("a(x) (evaluation domain) or NTT Domain without padding =", ntt_naive_nopad(a, root))
    # print("b(x) (evaluation domain) or NTT Domain withut padding=", ntt_naive_nopad(b, root))

    result = polymul_negacyclic_ntt(a, b)
    result_norm = polynomial.polymul(tuple(coeff_a[::-1]),tuple(coeff_b[::-1]))
    result_nor = [x% 7 for x in result_norm]
    print("Result =", result)
    print(f" with normal poly mul {result_norm}")
    print(f" with normal poly mul and mod q {result_nor}")