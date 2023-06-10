import random
def prchk(n) -> bool:
    """check prime"""
    if n > 1:
        for i in range(2, int(n/2)+1):
            if (n % i) == 0:
                return False
    else:
        return False
    return True

def pr_gen(rang):
    """prime gen"""
    x = 100
    while not prchk(x):
        x = random.randint(rang[0],rang[1])
    return x
flag = False
for k in range (1,171):
    if prchk(k*11+1):
        flag = True
        break
if flag:
      print(k)

print(prchk(23))