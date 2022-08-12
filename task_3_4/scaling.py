import os
import numpy as np
import csv

#first_year = 1999
#last_year =2014
#tab = np.genfromtxt("/home/aurelienh/Desktop/Int/task_3_4/temp/result1995_WDEP_OXN.txt",dtype=str)

def open_dep(first_year,last_year,pol):
    values = []
    receptors = []
    for p in range(first_year,last_year+1):
        tab = np.genfromtxt("/home/aurelienh/Desktop/Int/task_3_4/temp/result"+str(p)+"_"+pol+".txt",dtype=str)
        rec = []
        val = []
        for i in range(np.shape(tab)[0]):
            rec.append(tab[i][0])
            val.append(tab[i][1])
        receptors.append(rec)
        values.append(val)
    return [receptors,values]

def fusion_open_SR_table(filename_1,filename_2):
    """
    Do the same as the function open_SR_tab but for the jurek's SR tab.
    In fact there are two Jurek's tab (one with OSPAR receptors and one with the HELCOM receptors).
    We need to merge the two
    return:
    -the same list than open_SR_tab with the merge
    """
    result=[]
    with open(filename_1) as data:
        for line in csv.reader(data):
            result.append(line[0].split(";"))
    with open(filename_2) as data:
        compteur=0
        for line in csv.reader(data):
            if compteur == 0:
                pass
            else:
                result.append(line[0].split(";"))
            compteur = compteur + 1
    SR_name_emitters = result[0]
    SR_name_receptors =[]
    for i in range(1,np.shape(result)[0]):
        l = 0
        while result[i][0][l] !=" ":
            l = l+1
        SR_name_receptors.append(result[i][0][:l])
    new_SR_name_emitters = []
    for i in range(1,len(SR_name_emitters)):
        k=0
        while SR_name_emitters[i][k] == " ":
            k=k+1
        new_SR_name_emitters.append(SR_name_emitters[i][k:])
    return [new_SR_name_emitters,SR_name_receptors,result,filename_1,filename_2]

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

def sum_jurek_tab(first_year,last_year,pol):
    receptors = []
    values = []
    total = []
    for p in range(first_year,last_year+1):
        path_jurek_helcom = "/home/aurelienh/Desktop/Int/task_3_4/data/data_jurek_helcom/"+pol+"_"+str(p)+".csv"
        path_jurek_ospar = "/home/aurelienh/Desktop/Int/task_3_4/data/data_jurek_ospar/"+pol+"_"+str(p)+".csv"
        temp = fusion_open_SR_table(path_jurek_helcom,path_jurek_ospar)
        receptors.append(temp[1])
        values.append(convert(temp[2]))
    for p in range(len(values)):
        year_sum = []
        for i in range(np.shape(values[p])[0]):
            #print(receptors[p][i])
            sigma = sum(values[p][i][:]/10)
            year_sum.append(sigma)
        total.append(year_sum)
    return [receptors,total]

def sorting(heiko_sources,heiko_result,jurek_sources,jurek_result):
    """
    Now, we applied the function filter_heiko_tables on heiko's tab and the function filter_jurek_tables on the jurek's tab.
    We need to be sure if the sources are in the same order in the jurek's tab than in the heiko's tab.
    This function re order the tab.
    input:
    - heiko_sources: the first element of the return of the function filter_heiko_tables.
    - heiko_result: the second element of the return of the function flter_heiko_tables.
    - jurek_sources: the first element of the return of the function filter_jurek_tables.
    - jurek_result: the second element of the return of the function flter_jurek_tables.
    return:
    - A list with heiko's tab and sources. The heiko tab is now sorted to fit with the jure's tab. First element is the filtered sources and second element is the filtered value tab.
    """
    new_index_heiko = []
    heiko_sorted_sources = []
    heiko_sorted_result = heiko_result
    for i in range(len(jurek_sources)):
        new_index_heiko.append(heiko_sources.index(jurek_sources[i]))
    for i in range(np.shape(heiko_result)[0]):
        heiko_sorted_result[i] = heiko_result[new_index_heiko[i]]
    for i in range(len(heiko_sources)):
        heiko_sorted_sources.append(heiko_sources[new_index_heiko[i]])
    return [heiko_sorted_sources,heiko_sorted_result]

def scaling(first_year,last_year,pol_dep,pol_sr):
    SR = sum_jurek_tab(first_year,last_year,pol_sr)
    receptors_SR = SR[0]
    values_SR = SR[1]
    dep = open_dep(first_year,last_year,pol_dep)
    receptors_dep = dep[0]
    values_dep = dep[1]
    new_receptors_dep = []
    new_values_dep = []
    for p in range(len(values_SR)):
        temp = sorting(list(receptors_dep[p]),values_dep[p],list(receptors_SR[p]),values_SR[p])
        new_receptors_dep.append(temp[0])
        new_values_dep.append(temp[1])
        """print(new_receptors_dep)
        print(receptors_SR)
        print("----------")"""
    scale_factor = []
    """for p in range(len(receptors_SR)):
        print(new_receptors_dep[p])
        print(receptors_SR[p])
        print("------------------")"""
    for p in range(len(values_SR)):
        ratio = []
        for i in range(len(new_receptors_dep)):
            ratio.append(float(new_values_dep[p][i])/float(values_SR[p][i]))
        scale_factor.append(ratio)
    return [new_receptors_dep,scale_factor]


