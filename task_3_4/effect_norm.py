import os
import csv
import numpy as np

def open_SR_tab(filename):
    """
    input:
    - filename: the path of a SR table that you want to open
    return:
    -list with:
        SR_name_sources: A list with the different sources
        SR_name_receptors: A list with the different receptors
        result: the tab with values
        filename: the path associate to the table
    """
    result=[]
    with open(filename) as data:
        for line in csv.reader(data):
            #print(line[0])
            result.append(line)
    SR_name_sources = result[0]
    SR_name_receptors =[]
    for i in range(1,np.shape(result)[0]):
        SR_name_receptors.append(result[i][0])
    return [SR_name_sources,SR_name_receptors,result,filename]

reduced_95 = open_SR_tab("/home/aurelienh/Desktop/Int/task_3_4/result/output_SR_reduced_1995-2005_2019.csv")
reduced_10 = open_SR_tab("/home/aurelienh/Desktop/Int/task_3_4/result/output_SR_reduced_2010-2020_2019.csv")

def convert(tab):
    """
    After open the SR tab the values are in tab but there are strings. So we need to keep just the values and transform the string into float.
    input:
    - tab: the third element of the return of function open_SR_tab or fusion_open_SR_table.
    return:
    - the new float tab
    """
    float_tab = np.zeros((np.shape(tab)[0]-1,np.shape(tab)[1]-1))
    for i in range(1,np.shape(tab)[0]):
        for j in range(1,np.shape(tab)[1]):
            if tab[i][j]=="":
                float_tab[i-1][j-1]=0
            else:
                float_tab[i-1][j-1] = float(tab[i][j])
    return float_tab

value_95 = convert(reduced_95[2])
value_10 = convert(reduced_10[2])