
# coding: utf-8

# In[1]:

import numpy as np


# In[17]:

def getans(arr1,arr2):
    count = len(arr1)
    arr2.sort()
    start_index = 0
    end_index = len(arr2)-1
    last_start = 0
    while start_index<=end_index:
        if arr2[end_index]*(start_index+1-last_start)>=50:
            count+=1
            last_start = start_index
            start_index+=1
            end_index-=1
        else:
            start_index+=1
    return count


# In[21]:

f = open('input_ques2.txt','r')
f2 = open('output.txt','w+')
num_cases = f.readline()
for ix in range(int(num_cases)):
    n = f.readline()
    arr_1 = []
    arr_2 = []
    count = 0
    for k in range(int(n)):
        t = f.readline()
        val = int(t)
        if val>=50:
            arr_1.append(val)
        else:
            arr_2.append(val)
    #print arr_1, arr_2
    count = getans(arr_1,arr_2)
    name = "Case #"+str(ix+1)+": "+str(count)
    f2.write(name)
    f2.write("\n")
f2.close()


# In[19]:




# In[ ]:



