#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from bs4 import BeautifulSoup
import requests
import os,csv
import socket
import re
import pandas as pd


# In[ ]:


import urllib3


# In[ ]:


url = 'https://ucdavis.pubs.curricunet.com/Catalog/departments-programs-degrees' # This is the URL I used to download the data from the UCD catalog
text = requests.get(url).text
soup = BeautifulSoup(text,'lxml')


# In[ ]:


major_link = soup.find_all('div', attrs={'id': ['bodytop']})
#print(major_link)
# major_link = str(major_link)
# print(major_link)
all_seed = [item['href']
            for i in major_link
            for item in i.find_all('a')
            if 'href' in item.attrs]
majorlist_link = []
for links in all_seed:
    if len(links) > 9:# and 'raduate' not in links:
        majorlist_link.append(links)
print(len(majorlist_link))


# In[ ]:


all_seed_name = [item
                for i in major_link
                for item in i.find_all('span')
                if 'class' in item.attrs]
all_seed_name = (list(all_seed_name))


# In[ ]:


New_all_seed_name = []
for name in all_seed_name:
    name = str(name)
    name = '1'+ name[1:-1]+'1'
    front_sign = 0
    back_sign = 0
    for sign in name:
        if sign == '>':
            front_sign = name.index(sign)
        elif sign == '<':
            back_sign = name.index(sign)
        else:
            pass
    New_all_seed_name.append(name[front_sign + 1:back_sign])


# In[ ]:


New_all_major_name = []
for names in New_all_seed_name:
    #if not 'raduate' in names:
    if True:
        New_all_major_name.append(names)
print(len(New_all_major_name))


# In[ ]:


first_final_dict = {}
second_final_dict = {}
third_final_dict = {}
for i in range(len(majorlist_link)):
        first_final_dict.update({majorlist_link[i]:New_all_major_name[i]})
        
for key in first_final_dict.keys():    
    if not 'raduate' in key:
        second_final_dict.update({key:first_final_dict[key]})
for val in second_final_dict.keys():
    if not 'raduate' in second_final_dict[val]:
        third_final_dict.update({val:second_final_dict[val]})
#print(third_final_dict)


# In[ ]:


def output_of_major(keylist):
    #url = 'https://ucdavis.pubs.curricunet.com/Catalog/computer-science'
    url = 'https://ucdavis.pubs.curricunet.com' + keylist
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'lxml')
    result = soup.find_all('div', attrs={'class': ['tab-pane active'], 'class': ['container-fluid']})
    result = str(result)

    i = 1
    left_side = []
    right_side = []

    for i in range(len(result)):
        if result[i] == '>' and result[i + 1] != '<':
            left_side.append(i)
        if result[i] == '<' and result[i - 1] != '>':
            right_side.append(i)
        # print(left_side)
        # print('\n'*3)
    try:
        del right_side[right_side.index(1)]
        # print(right_side)
    except:
        pass
    dict1 = {}
    dict = {}
    for each_sign in range(len(right_side)):
        dict.update({left_side[each_sign]: right_side[each_sign]})
    # print(dict)
    for x, y in dict1.items():
        if not (x + 1) == y:
            dict.update({x: y})
    # print(dict)

    merg_list = []
    for x in dict.keys():
        merg_list.append(result[x + 1:dict[x]])

    course = []
    for ListLen in merg_list:
        if len(ListLen) == 3:
            begin_num = merg_list.index(ListLen)
            merg_list = merg_list[begin_num:]
            break

    for ListLen in merg_list:
        if 3 <= len(ListLen) <= 4:
            course.append(ListLen)
    # elif '(' in ListLen or '-' in ListLen:
    #    pass
    course_fix = []
    course_fix_bad = []
    k = 0
    for i in course:
        # print(i)
        if len(re.findall('-', i)) != 0:
            k = 1
            # print(i)
            course_fix_bad.append(i)
        if len(re.findall('\(', i)) != 0:
            k = 1
            course_fix_bad.append(i)
    # print(course_fix_bad)
    for i in course:
        if not i in course_fix_bad:
            course_fix.append(i)
    #print(course_fix)   

    New_course = ['']
    for i in course_fix:
        if (i[0]).isalpha():
            New_course.append(i)
        if (i[0]).isdigit():
            New_course[-1] += i
    del New_course[0]
    # print(New_course)
    New_course1 = []
    for i in New_course:
        if 5 <= len(i) <= 7:
            # del i
            New_course1.append(i)
    # print(New_course)
    sorted(New_course1)
    course_set = ([])
    course_set = set(New_course1)
    #print(course_set)
    return sorted(course_set)


# In[ ]:


import time
start = time.time()

first_final_course_dict = {}
i = 0
for result in third_final_dict.keys():
    #print(output_of_major(result))
    if len(output_of_major(result)) >= 0:
        #print(result)
        first_final_course_dict.update({result:output_of_major(result)})
#print(first_final_course_dict)
end = time.time()
print(end - start)


# In[ ]:


print(first_final_course_dict)


# In[ ]:


def main_catalog1():
    #with open('UCD_major.ipynb','w+') as major:
     #   major.readlines()
    f1 = open("UCD_Catalog1.csv", "w+")
    with open("UCD_Catalog1.csv", "w") as toWrite:
        fieldnames = ['MajorID','MajorName']
        writer = csv.DictWriter(toWrite, fieldnames = fieldnames)
        writer.writeheader()
        for x,y in third_final_dict.items():
            writer.writerow({'MajorID' : x, 'MajorName':y})
    f1.close()
main_catalog1()

UCD = pd.read_csv('UCD_Catalog1.csv', header=0)
UCD.columns = ['MajorID','MajorName']
print(UCD.iloc[200])
UCD = UCD.set_index(['MajorID'])
print(UCD)


# In[ ]:


def main_course():
    file = open("UCD_Catalog_course.csv", "w+")
    with open("UCD_Catalog_course.csv", "w") as toWrite:
        fieldnames = ['MajorID','MajorCourse']
        writer = csv.DictWriter(toWrite, fieldnames = fieldnames)
        writer.writeheader()
        for x,y in first_final_course_dict.items():
            writer.writerow({'MajorID' : x, 'MajorCourse':y})
    file.close()    
main_course()

UCD_course = pd.read_csv('UCD_Catalog_course.csv', header=0)
UCD_course.columns = ['MajorID','MajorCourse']
print(UCD_course.iloc[215])
UCD_course = UCD_course.set_index(['MajorID'])
print(UCD_course.head(10))


# In[ ]:


UCD_course_merge = pd.merge(UCD,UCD_course, on='MajorID')
#print(UCD_course_merge)
UCD_course_merge = UCD_course_merge.reset_index(drop = True)
UCD_course_merge = UCD_course_merge.set_index('MajorName')
print(UCD_course_merge)


# In[ ]:


UCD_course_merge.to_csv('UCD_Catalog_final.csv')
#UCD_course_merge.to_excel('UCD_Catalog_final.xls')


# In[ ]:




