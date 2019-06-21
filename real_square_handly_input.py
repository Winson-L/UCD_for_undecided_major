#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import real_2_21_19
import re
from collections import Counter


# In[ ]:


i = 1 
course_list = []
course_set = set([])
while i >0:
    course = input('What is the course name?\n')
    if len(course) >= 5:
        course = course.upper()
        course_list.append(course)
    else:
        break
course_set = set(course_list)
#print(course_set)
b = 0
num = 0
j = 0
new_course_set = []
for each in course_set:
    num = 0
    while b < len(each):
        if each[b].isdigit():
            #print(b)
            break
        b += 1
    for thing in each:
        if thing.isdigit():
            num += 1
    #print(num)
    if num == 2:
        new_each = each[:b] + '0'+ each[b:]
        new_course_set.append(new_each)
    elif num == 1:
        new_each = each[:b] + '00'+ each[b:]
        new_course_set.append(new_each)
    else:
        new_course_set.append(each)
print(new_course_set)


# In[ ]:


possible_major = []
for j in new_course_set:
    with open('REAL.py','r') as toRead:
        for i in toRead:
            i = re.sub(r'\n','',i)
        #print(i)
        #print(type(i))
            if len(re.findall(j,i)) != 0:
                for k in range(len(i)):
                    if i[k] == '[':
                    #print(i[:k-2])
                        possible_major.append(i[:k-2])
#print(possible_major)


# In[ ]:


dict={}
good_fit=int(input('What is the minimum classes you require for the fit? (Min is 1)\n'))
set_possible_major = set(possible_major)
for i in set_possible_major:
    j = possible_major.count(i)
    if j >= good_fit:
        dict.update({i:j})
x = Counter(dict)
print(x.most_common())


# In[ ]:


with open('C:/Users/Elaine/Desktop/course_to_major_result.txt','w+') as toWrite:
    for i in x.most_common():
        text = str(i)[1:-1]
        text = re.sub(',',' ',text)
        text = re.sub("'",'',text)
        sep = [i[:-1],i[-1]]
        toWrite.write(text)
        toWrite.write('\n')


# In[ ]:





# In[ ]:




