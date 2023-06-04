import numpy as np

point1 = np.array((1,2,3))
point2 = np.array((121,21222,12))
dist =np.linalg.norm(point1-point2)# function squares and adds all the distances
print(dist,np.linalg.norm(point1))
