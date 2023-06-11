

from poly import Poly
import common

def ntt_naive(p, root):
    """Compute forward cyclic n-NTT of n-coefficient polynomial.

    Compute pntt_i = sum_{j=0}^{n} p[j]*root^{ij} for 0 <= i < n

    Parameters
    ----------
    p : Poly
        input polynomial with n coefficients.
    root: int
        n-th root of unity modulo q.
    Returns
    ----------
    Poly
        p evaluated at root^0, ..., root^n-1, i.e., p transformed into NTT domain.
    """
    q = p.q
    pntt = Poly.zero(p.n, q)
    for i in range(p.n):
        for j in range(p.n):
            pntt.coeffs[i] = (pntt.coeffs[i] +  p.coeffs[j]*pow(root, i*j, q)) % q
    return pntt

def invntt_naive(pntt, root):
    """Compute cyclic inverse NTT.

    Compute p_i =  1/n * sum_{j=0}^{n} pntt[j]*root^{-ij} for 0 <= i < n

    Parameters
    ----------
    pntt : Poly
        input in NTT domain, i.e., evaluation of p at root^0, ..., root^n-1.
    root: int
        n-th root of unity modulo q.
    Returns
    ----------
    Poly
        p in normal domain.
    """
    q = pntt.q
    p = Poly.zero(pntt.n, q)
    for i in range(pntt.n):
        for j in range(pntt.n):
            p.coeffs[i] = (p.coeffs[i] + pntt.coeffs[j]*pow(root, -i*j, q)) % q
    ninv = pow(p.n, -1, q)
    for i in range(p.n):
        p.coeffs[i] = (p.coeffs[i] * ninv) % q
    return p

def polymul_cyclic_ntt(a, b):
    """Perform NTT-based multiplication of two polynomials in the ring Zq[x]/(x^n-1), i.e., cyclic.

    For computing the product we evaluate the n-coefficient polynomials and b
    at n powers of a n-th root of unity, then multiply coefficient wise,
    and interpolate the product using the inverse NTT.
    Primitive n-th root of unity modulo q needs to exist.

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
    assert ((q-1) % (n)) == 0

    # we need a n-th root of unity
    root = common.primitiveRootOfUnity(n, q)

    # For implementing a cyclic NTT we need to evaluate a and b at n roots of unity.

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
    # q has the condition that  ( q - 1 ) % n is 0, i.e. n is a factor of ( q - 1 )
    # Additionaly, q has to be a prime number

    a = Poly([3, 2, 1], q=7)
    b = Poly([0, 1, 1], q=7)

    print("a(x) =", a)
    print("b(x) =", b)

    root = common.primitiveRootOfUnity(a.n, a.q)
    print("Root used =", root)

    print("a(x) (evaluation domain) =", ntt_naive(a, root))
    print("b(x) (evaluation domain) =", ntt_naive(b, root))

    result = polymul_cyclic_ntt(a, b)
    print("Result =", result)