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
print(pr_gen([1,99]))
