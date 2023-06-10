"""Computing Mult"""
def kat(x,y):
    """perform katsu"""
    if x<10 or y<10:
        return x*y
    xs = str(x)
    ys = str(y)
    md = max(len(xs),len(ys))//2
    xh = int(xs[:-md])
    xl= int(xs[-md:])
    yh = int(ys[:-md])
    yl = int(ys[-md:])
    a = kat(xh,yh)
    d = kat(yl,xl)
    e = kat(yl+yh,xh+xl)-a-d
    return a*(10**(2*md))+d+e*(10**(md))
x = int(input("give first number"))
y = int(input("give second number"))
print(kat(x,y))