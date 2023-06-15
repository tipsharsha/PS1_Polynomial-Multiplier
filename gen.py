""""wad"""
import pandas


number_str = input("Enter a number: ")
print(number_str)
x = int(number_str)

my_list = []

for i in range(1,x):
   my_list.append(i)

print(my_list)

gen = {}

for i in range(1,x):
    my_list_copy = my_list.copy()
    for j in range(1,x):
        k = (i ** j) % x
        for p in range(len(my_list_copy)):
            if k == my_list_copy[p]:
                my_list_copy.pop(p)
                break
    if len(my_list_copy) == 0:
        gen[i] = i
gen_data = pandas.DataFrame(gen)
# print(gen_data)
