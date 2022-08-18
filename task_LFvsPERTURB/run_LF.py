import os
import csv
import numpy as np
import statistics as sc

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
            result.append(line[0].split("\t"))
    SR_name_sources = result[0]
    SR_name_receptors =[]
    for i in range(1,np.shape(result)[0]):
        SR_name_receptors.append(result[i][0])
    return [SR_name_sources,SR_name_receptors,result,filename]

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

#A = open_SR_tab("LF_data/Tables/1990_reduced_nitrogenLF.csv")

def open_dep(list_years,pol):
    values = []
    receptors = []
    for p in range(len(list_years)):
        if p==2015:
            pass
        else:
            tab = np.genfromtxt("LF_data/data_scaling/result"+list_years[p]+"_"+pol+".txt",dtype=str)
            rec = []
            val = []
            for i in range(np.shape(tab)[0]):
                rec.append(tab[i][0])
                val.append(tab[i][1])
            receptors.append(rec)
            values.append(val)
    return [receptors,values]

#A = open_dep(["1999","2002"],"DDEP_RDN")

def sum_jurek_tab(list_years,pol):
    receptors = []
    values = []
    total = []
    for p in range(len(list_years)):
        if p==2015:
            pass
        else:
            path = "LF_data/Tables/"+list_years[p]+"_"+pol+"LF.csv"
            temp = open_SR_tab(path)
            receptors.append(temp[1])
            #print(convert(temp[2])[:,-3])
            values.append(convert(temp[2])[:,-3])
    return [receptors,values]

#A = sum_jurek_tab(["1999","2002"],"reduced_nitrogen")

def sorting_bis(heiko_sources,heiko_result,jurek_sources,jurek_result):
    new_index_heiko = []
    heiko_sorted_sources = []
    heiko_sorted_result = np.zeros((np.shape(heiko_result)))
    for i in range(len(jurek_sources)):
        if jurek_sources[i] in heiko_sources:
            new_index_heiko.append(heiko_sources.index(jurek_sources[i]))
        else:
            pass
    for i in range(np.shape(heiko_result)[0]):
        heiko_sorted_result[i] = heiko_result[new_index_heiko[i]]
    for i in range(len(heiko_sources)):
        heiko_sorted_sources.append(heiko_sources[new_index_heiko[i]])
    return [heiko_sorted_sources,heiko_sorted_result]

def filtering(receptors_1,values_1,receptors_2,values_2):
    index_list = []
    #print(receptors_1)
    #print(values_1)
    for i in range(len(receptors_1)):
        if receptors_1[i] in receptors_2:
            pass
        else:
            index_list.append(i)
    new_receptors_1 = np.delete(receptors_1,index_list,axis=0)
    new_values_1 = np.delete(values_1,index_list,axis=0)
    return [new_receptors_1,new_values_1]

def scaling(list_years,pol_dep,pol_sr):
    SR = sum_jurek_tab(list_years,pol_sr)
    receptors_SR = SR[0]
    values_SR = SR[1]
    for p in range(len(receptors_SR)):
        print(np.shape(receptors_SR[p]))
        print(np.shape(values_SR[p]))
        print("----------")
    if pol_sr == "reduced_nitrogen":
        dep_1 = open_dep(list_years,"DDEP_RDN")
        dep_2 = open_dep(list_years,"WDEP_RDN")
        receptors_dep_1 = dep_1[0]
        values_dep_1 = dep_1[1]
        receptors_dep_2 = dep_2[0]
        values_dep_2 = dep_2[1]
        values_dep = []
        receptors_dep = []
        for p in range(len(values_dep_1)):
            if np.shape(values_dep_1[p]) == np.shape(values_dep_2[p]):
                tab = np.zeros((np.shape(values_dep_1[p])))
                for i in range(np.shape(tab)[0]):
                    tab[i] = float(values_dep_1[p][i])+float(values_dep_2[p][i])
                values_dep.append(tab)
                receptors_dep.append(receptors_dep_1[p])
            else:
                print("error")
    else:
        dep = open_dep(list_years,pol_dep)
        receptors_dep = dep[0]
        values_dep = dep[1]

    new_receptors_SR = []
    new_values_SR = []
    for p in range(len(values_SR)):
        temp = filtering(receptors_SR[p],values_SR[p],receptors_dep[p],values_dep[p])
        new_receptors_SR.append(temp[0])
        new_values_SR.append(temp[1])
    new_receptors_dep = []
    new_values_dep = []
    for p in range(len(values_dep)):
        temp = filtering(receptors_dep[p],values_dep[p],new_receptors_SR[p],new_values_SR[p])
        new_receptors_dep.append(temp[0])
        new_values_dep.append(temp[1])
    new_receptors_dep_2 = []
    new_values_dep_2 = []
    for p in range(len(values_SR)):
        temp = sorting_bis(list(new_receptors_dep[p]),new_values_dep[p],list(new_receptors_SR[p]),new_values_SR[p])
        new_receptors_dep_2.append(temp[0])
        new_values_dep_2.append(temp[1])
    scale_factor = []
    for p in range(len(new_values_SR)):
        ratio = []
        for i in range(len(new_receptors_dep_2[p])):
            ratio.append(10*float(new_values_dep_2[p][i])/float(new_values_SR[p][i]))
        scale_factor.append(ratio)
    for p in range(len(new_receptors_SR)):
        print(new_receptors_SR[p])
        print(new_receptors_dep_2[p])
    return [new_receptors_dep,scale_factor]

A = scaling(["1999","2018"],"nan","reduced_nitrogen")
print(A)

