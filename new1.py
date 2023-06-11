coef =[5,1,10,20,4,22,22,7,0,11,9]
co = [0]*11
for i in range(0,11):
    for j in range (0,11):
        co[j] +=21*(pow(12,i*j)*coef[i])
a =[x % 23 for x in co]
print(co)
print(a)