x = 12
y = 15
def gcd(x,y) -> int:
    while x != y :
        if x>y:
            x = x-y
        else:
            y = y-x
    return x
print(gcd(x,y))