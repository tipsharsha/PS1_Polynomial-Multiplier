"""Barrett Redution Algorithm"""
import pyverilog
import time
from csv import writer
from random import randint
start_time = time.time()
n = 3**23
k = n.bit_length()#finds the bit length of the modulus 
r = (1<<k*2)//n#right shift 1 by bit length *2 to compute 4^k
def bar(x) -> int:
    t = x - ((x*r)>>k*2)#shift left by 2k to divide by 4^k
    if t<n :
        return(t)
    else:
        return(t-n)
for _ in range (1,100):
    num = randint(3**23,3**46)
    print(f"{bar(num)}")
time_passed = time.time() - start_time
print(f" {time_passed} seconds ")
List = [time_passed]
with open('time_bar.csv', 'a') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(List)
    f_object.close()