#!/usr/bin/env python
# coding: utf-8

# In[ ]:


file = open('UCD_Catalog_final.csv','r')
with open('UCD_Catalog_final.csv','r') as readfile:
    j = 0
    
    with open ("regulate_list_for_course.txt",'w+') as toWrite:
        for i in readfile:
            toWrite.write(i)
            print (i)
            #print()
            j +=1
    print(j)
file.close()


# In[ ]:


import re
TEXT = ""
with open ("regulate_list_for_course.txt",'r') as toWrite:
    for i in toWrite:
        TEXT += str(i)
    #print(str(TEXT).format())
    database = re.sub('"', ' ',TEXT)
    print(type(database))
    database = database[22:]
    print(database)


# In[ ]:


index_list = []
for i in range(len(database)):
    if database[i] == ']':
        index_list.append(i)
        #print (database[i-1])
print(index_list)


# In[ ]:


i = 0
j = 0
k = 0
the_amazing_list = []
for i in range(len(index_list)):
    if i != 0 :
        the_amazing_list.append(database[index_list[i-1]+1:index_list[i]+1])
    elif i == 0 :
        the_amazing_list.append(database[:index_list[i]+1])
print(the_amazing_list)


# In[ ]:


with open('REAL.py','w+') as toWrite:
    toWrite.writelines(the_amazing_list)


# In[ ]:





# In[ ]:




