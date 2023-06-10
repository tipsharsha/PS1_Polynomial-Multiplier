import sage
def NTT(x,g,q) -> list:
    n = len(x)
    t = int(len(x)//2)
    m =1
    while m<n:
        k =0
        for i in range(0,m):
            S = g[m+i]
            for j in range(k,k+t):
                U = x[j]
                V = x[j+t]*(S%q)
                x[j] = U+V%q
                x[j+t]= U -V%q
            k = k +2*t
        t = t/2
        m =2*m
    return x
g = sage.
for y in range (1,12):
    g.append(pow(3,y))
q = 998244353
x =[1, 2, 3, 4, 5, 6]   
print(NTT(x,g,q))