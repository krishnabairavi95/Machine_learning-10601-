
# coding: utf-8

# In[432]:


import csv
import sys
input=sys.argv[1]
needed_col=[-1]
a=[]


with open('small_test.csv') as file:     
   reader = csv.reader(file)
   for column in reader:
       content = list(str(column[-1]) for i in needed_col)
       a.append(content)
   #print(a)
   a=a[1:]
#print(content)
total_elements=len(a)
print (total_elements)

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
    #for x in unique_list:
#   print (x)


# In[436]:


unique_elements=unique(a)
print(unique_elements)
print(a)
#print (unique_output)
#import itertools
#unique_elements=list(itertools.chain.from_iterable(unique_output))
#unique_element_2=unique(a[2])
#unique_elements=[unique_element_1,unique_element_2]
#print (unique_elements)


# In[437]:


def countX(lst, x): 
    return lst.count(x)


# In[441]:

#print (unique_elements)

#needed_column= [0,1]
class_correct_1= countX(a,unique_elements[0])
class_correct_2= countX(a,unique_elements[1])
class_correct=[class_correct_1,class_correct_2]
print (class_correct_1)


# In[442]:


minority_voted_class= min(class_correct)
print (minority_voted_class)
error_rate= minority_voted_class/total_elements
print (error_rate)


# In[443]:


#total_elements


# In[444]:


prob=[]
Entropy=[]             
label_entropy=[]
import math
for i in range(0,len(class_correct)):
    prob.append(class_correct[i]/total_elements)
    Entropy.append(-(prob[i]*math.log(prob[i],2)))
    label_entropy.append(Entropy[i])
    b=(sum(label_entropy))
print(b)


# In[445]:


output_file = sys.argv[2]
output_file_object = open(output_file, "w")
output_file_object.write("entropy: %s" %b)
output_file_object.write("\nerror: %s" %error_rate)
#print (b,file=output_file)
#print ("error:",error_rate,file=output_file)
output_file_object.close()


# In[381]:


#fh = open("data.txt","w")
#print("42 is the answer, but what is the question?", file=fh)
 #fh.close()

