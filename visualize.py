import sys
import matplotlib.pyplot as plt
import numpy as np

key = sys.argv[1]
pts = open("instance"+str(key)+".txt", "r")
n = int(pts.readline())
y = []
for m in range(n):
    line = (pts.readline()).split()
    y.append(float(line[1]))
plt.scatter(np.linspace(1,n,num=n),y,c="blue")
pts.close()

if (sys.argv[2]=="local1"):
    sol = open("local1_solution"+str(key)+".txt", "r")
    print("success... sol = local1")
elif (sys.argv[2]=="local2"):
    sol = open("local2_solution"+str(key)+".txt", "r")
elif (sys.argv[2]=="greedy"):
    sol = open("greedy_solution"+str(key)+".txt", "r")
n = int(sol.readline())
for m in range(n):
    line = (sol.readline()).split()
    type = line[0]
    value = float(line[1])
    if type=="h":
      plt.axhline(y=value, c="red")
    elif type=="v":
      plt.axvline(x=value, c="green")
      
plt.show()
sol.close()