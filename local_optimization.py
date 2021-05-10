import sys
import time

#Helper method for counting number of points in a region designated by 4 bounds
def pts_in_region(u, r, d, l, xd):
    pts_found = 0
    for x in range(int(l+.5), int(r+.5)):
      if xd[x]<u and xd[x]>d:
          pts_found += 1
    return pts_found


#Helper method for finding the number of points which have been isolated
def num_isolated(lines, xd):
  #SORT INTO SEPARATE H/V LISTS
  h_lines = [.5]
  v_lines = [.5]
  for line in sorted(lines.keys()):
    if lines[line]<2:
      h_lines.append(line)
    if lines[line]>0:
      v_lines.append(line)
  h_lines.append(n+.5)
  v_lines.append(n+.5)
  #TEST EACH REGION
  successes = 0
  for i in range(1, len(v_lines)):
    l = v_lines[i-1]
    r = v_lines[i]
    for j in range(1, len(h_lines)):
      d = h_lines[j-1]
      u = h_lines[j]
      val = pts_in_region(u,r,d,l,xd)
      if val==1:
        successes += 1
  return successes


#Helper methods for maintaining the 0-1-2 code in line dictionary
def remove_vert(lines, index):
  val = lines[index]
  if lines[index]==2:
    lines.pop(index)
  elif lines[index]==1:
    lines[index] = 0
  return val

def add_vert(lines, index):
  try:
    if lines[index]==0:
      lines[index] = 1
    else:
      raise ValueError
  except KeyError:
    lines[index] = 2
    
def remove_hor(lines, index):
  val = lines[index]
  if lines[index]==0:
    lines.pop(index)
  elif lines[index]==1:
    lines[index] = 2
  return val

def add_hor(lines, index):
  try:
    if lines[index]==2:
      lines[index] = 1
    else:
      raise ValueError
  except KeyError:
    lines[index] = 0

#Optimization method for decreasing the number of necessary lines
def optimize(lines, x_dict, n):                                                                         ##############################################
  notDone = False
  dual1 = False
  dual2 = False
  
  #CHOOSE THE FIRST LINE TO REMOVE
  i1 = 1
  while i1 < n:
    success = False
    try:
      if dual1:
        #TRY OTHER LINE AT I1
        dual1 = False
        i1 -= 1
        val1 = remove_hor(lines, i1+.5)
      elif lines[i1+.5]==1:
        #BOTH H AND V LINES EXIST AT I1, SIGNAL DUAL1 TO TRY BOTH
        val1 = 1
        lines[i1+.5] = 0
        dual1 = True
      else:
        #ONLY ONE LINE EXISTS FOR I1
        val1 = lines.pop(i1+.5)
    except KeyError:
      #NO LINE EXISTS FOR I1, SKIP
      i1 += 1
      continue
    
    #CHOOSE THE SECOND LINE TO REMOVE
    i2 = 1
    while i2 < n:
      try:
        if dual2:
          #TRY OTHER LINE AT I2
          dual2 = False
          i2 -= 1
          val2 = remove_hor(lines, i2+.5)
        elif lines[i2+.5]==1:
          #BOTH H AND V LINES EXIST AT I2, SIGNAL DUAL2 TO TRY BOTH
          val2 = 1
          lines[i2+.5] = 0
          dual2 = True
        else:
          #ONLY ONE LINE EXISTS FOR I2
          val2 = lines.pop(i2+.5)
      except KeyError:
        #NO LINE EXISTS FOR I2, SKIP
        i2 += 1
        continue

      #CHOOSE NEW LINE TO ADD
      for j in range(1,n):
        #TRY ADDING VERTICAL AT J
        try:
          add_vert(lines, j+.5)
          val = num_isolated(lines, x_dict)
          if val==n:
            #NEW LINE SET STILL ISOLATES ALL POINTS
            success = True
            print("success! replaced",i1+.5,"and",i2+.5,"with v",j+.5)
            if j<=i1:
              #LINE HAS BEEN ADDED TO CHECKED REGION, MUST CHECK AGAIN
              notDone = True
            break
          #NEW LINE SET DID NOT ISOLATE ALL POINTS, TRY HORIZONTAL
          remove_vert(lines, j+.5)
        #VALUE ERROR THROWN IF LINE ALREADY EXISTS
        except ValueError: pass
    
        #TRY ADDING HORIZONTAL AT J
        try:
          add_hor(lines, j+.5)
          val = num_isolated(lines, x_dict)
          if val==n:
            #NEW LINE SET STILL ISOLATES ALL POINTS
            success = True
            print("success! replaced",i1+.5,"and",i2+.5,"with h",j+.5)
            if j<=i1:
              #LINE HAS BEEN ADDED TO CHECKED REGION, MUST CHECK AGAIN
              notDone = True
            break
          #NEW LINE SET DID NOT ISOLATE ALL POINTS, TRY NEXT COMBINATION
          remove_hor(lines, j+.5)
        #VALUE ERROR THROWN IF LINE ALREADY EXISTS
        except ValueError: pass
      if success:
        #LINE AT I2 STAYS REMOVED
        break
      #IF NO SUCCESS FOUND, RESTORE LINE AT I2
      lines[i2+.5] = val2
      i2 += 1
    if success:
      #LINE AT I1 STAYS REMOVED, MOVE TO NEXT COMBINATION
      i1 += 1
      continue
    #IF NO SUCCESS FOUND, RESTORE LINE AT I1
    lines[i1+.5] = val1
    i1 += 1
  return notDone



#Main method

#CREATE FILES FOR READING AND WRITING
file_name = sys.argv[1]
num = file_name[8:10]
input = open(file_name,"r")
output = open("local_solution"+str(num)+".txt","w")

#READ AND STORE POINT VALUES
n = int(input.readline())
x_dict = {}
for m in range(n):
  line = (input.readline()).split()
  x = int(line[0])
  y = int(line[1])
  x_dict[x] = y

#CREATE FEASIBLE SET OF LINES
lines = {} #keys will designate the x/y value of the line, and value the type
#values can be: (0) horizontal, (1) horizontal and vertical, or (2) vertical
#this data structure is used for quick O(1) lookups
for i in range(1,n):
  lines[i+.5]=0

#OPTIMIZATION
start = time.perf_counter() 
while optimize(lines, x_dict, n):
  pass
end = time.perf_counter()
print(f"TOTAL RUNTIME: {end - start:0.4f} seconds")

#COLLECT LINES
v_lines = []
h_lines = []
for line in sorted(lines.keys()):
  if lines[line]>0:
    v_lines.append(line)
  if lines[line]<2:
    h_lines.append(line)

#WRITE OUTPUT
output.write(str(len(v_lines)+len(h_lines)))
for line in v_lines:
  output.write("\nv "+str(line))
for line in h_lines:
  output.write("\nh "+str(line))

#CLOSE FILES
input.close()
output.close()