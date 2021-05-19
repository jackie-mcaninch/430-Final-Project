import sys
import time

#Helper method for counting number of points in a region designated by 4 bounds
def pts_in_region(u, r, d, l, xd):
    pts_found = 0
    for x in range(int(l+.5), int(r+.5)):
      if xd[x]<u and xd[x]>d:
          pts_found += 1
      if pts_found > 1:
          return 2
    return pts_found


#Helper method for finding the number of points which have been isolated
def all_isolated(h_lines, v_lines, xd, n):
  #SORT INTO SEPARATE H/V LISTS
  h = [.5]
  v = [.5]
  for line in sorted(h_lines):
    h.append(line)
  for line in sorted(v_lines):
    v.append(line)
  h.append(n+.5)
  v.append(n+.5)

  #TEST EACH REGION
  for i in range(1, len(v)):
    l = v[i-1]
    r = v[i]
    for j in range(1, len(h)):
      d = h[j-1]
      u = h[j]
      val = pts_in_region(u,r,d,l,xd)
      if val>1:
          return False
  return True

def solution_exists_h(h_lines, v_lines, xd, n):
  for j in range(1,n):
    if j+.5 in h_lines:
      continue
    h_lines.add(j+.5)
    if all_isolated(h_lines, v_lines, xd, n):
      return j
    h_lines.remove(j+.5)
  return -1

def solution_exists_v(h_lines, v_lines, xd, n):
  for j in range(1,n):
    if j+.5 in v_lines:
        continue
    v_lines.add(j+.5)
    if all_isolated(h_lines, v_lines, xd, n):
      return j
    v_lines.remove(j+.5)
  return -1

#Optimization method for decreasing the number of necessary lines
def optimize(h_lines, v_lines, xd, n):
    not_done = False
    i1 = 1
    while i1 < n:
        success = False
        #TEST REMOVING HORIZONTAL AT I1
        try:
            h_lines.remove(i1+.5)
            i2 = 1
            while i2 < n:
                #TEST REMOVING HORIZONTAL AT I2
                try:
                    h_lines.remove(i2+.5)
                    val = solution_exists_h(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced h {i1+.5} and h {i2+.5} with h {val+.5}")
                        if val<=i1:
                            not_done = True
                        break
                    val = solution_exists_v(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced h {i1+.5} and h {i2+.5} with v {val+.5}")
                        if val<=i1:
                            not_done = True
                    if success == False:
                        h_lines.add(i2+.5)
                except KeyError: pass
                if success:
                    break
                #TEST REMOVING VERTICAL AT I2
                try:
                    v_lines.remove(i2+.5)
                    val = solution_exists_h(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced h {i1+.5} and v {i2+.5} with h {val+.5}")
                        if val<=i1:
                            not_done = True
                        break
                    val = solution_exists_v(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced h {i1+.5} and v {i2+.5} with v {val+.5}")
                        if val<=i1:
                            not_done = True
                    if success == False:
                        v_lines.add(i2+.5)
                except KeyError: pass
                if success:
                    break
                i2 += 1
            if success == False:
                h_lines.add(i1+.5)
        except KeyError: pass
        success == False
        
        #TEST REMOVING VERTICAL AT I1
        try:
            v_lines.remove(i1+.5)
            i2 = 1
            while i2 < n:
                #TEST REMOVING HORIZONTAL AT I2
                try:
                    h_lines.remove(i2+.5)
                    val = solution_exists_h(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced v {i1+.5} and h {i2+.5} with h {val+.5}")
                        if val<=i1:
                            not_done = True
                        break
                    val = solution_exists_v(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced v {i1+.5} and h {i2+.5} with v {val+.5}")
                        if val<=i1:
                            not_done = True
                        break
                    h_lines.add(i2+.5)
                except KeyError: pass
                if success:
                    break
                #TEST REMOVING VERTICAL AT I2
                try:
                    v_lines.remove(i2+.5)
                    val = solution_exists_h(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced v {i1+.5} and v {i2+.5} with h {val+.5}")
                        if val<=i1:
                            not_done = True
                        break
                    val = solution_exists_v(h_lines, v_lines, xd, n)
                    if val>0:
                        success = True
                        print(f"success! replaced v {i1+.5} and v {i2+.5} with v {val+.5}")
                        if val<=i1:
                            not_done = True
                        break
                    v_lines.add(i2+.5)
                except KeyError: pass
                if success:
                    break
                i2 += 1
            if success == False:
                v_lines.add(i1+.5)
        except KeyError: pass
        i1 += 1        
    return not_done



#Main method

#CREATE FILES FOR READING AND WRITING
file_name = sys.argv[1]
num = file_name[8:10]
input = open(file_name,"r")
output = open("local2_solution"+str(num)+".txt","w")

#READ AND STORE POINT VALUES
n = int(input.readline())
x_dict = {}
for m in range(n):
  line = (input.readline()).split()
  x = int(line[0])
  y = int(line[1])
  x_dict[x] = y

#CREATE FEASIBLE SET OF LINES
h_lines = set()
v_lines = set()
for i in range(1,n):
  h_lines.add(i+.5)

#OPTIMIZATION
start = time.perf_counter()
while optimize(h_lines, v_lines, x_dict, n):
    pass
end = time.perf_counter()
print(f"TOTAL RUNTIME: {end - start:0.4f} seconds")

#WRITE OUTPUT
output.write(str(len(v_lines)+len(h_lines)))
for line in v_lines:
  output.write("\nv "+str(line))
for line in h_lines:
  output.write("\nh "+str(line))

#CLOSE FILES
input.close()
output.close()