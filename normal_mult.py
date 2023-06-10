import time
from csv import writer
from random import randint
start_time = time.time()
n = 3**23
for _ in range (1,100):
    num = randint(3**23,3**46)
    print((num%n))
time_passed =time.time()-start_time
print(f"{time_passed} seconds")
List = [time_passed]
with open('time_norm.csv', 'a') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(List)
    f_object.close()