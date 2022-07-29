"""
This program make a normalization for the SR tables between 1995 and 2020 (you can select the first year and the last year for the normalization, the method for the normalization) and the year that you want to normalize.
Author: Henon Aurelien (meteo france), aurelien.henon@meteo.fr
Date: 2022

"""

import os
import csv
import numpy as np
import statistics as sc

def open_SR_tab(filename):
    result=[]
    with open(filename) as data:
        for line in csv.reader(data):
            result.append(line[0].split("\t"))
    SR_name_emitters = result[0]
    SR_name_receptors =[]
    for i in range(1,np.shape(result)[0]):
        SR_name_receptors.append(result[i][0])
    return [SR_name_emitters,SR_name_receptors,result,filename]

def fusion_open_SR_table(filename_1,filename_2):
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
    float_tab = np.zeros((np.shape(tab)[0]-1,np.shape(tab)[1]-1))
    for i in range(1,np.shape(tab)[0]):
        for j in range(1,np.shape(tab)[1]):
            if tab[i][j]=="":
                float_tab[i-1][j-1]=0
            else:
                float_tab[i-1][j-1] = float(tab[i][j])
    return float_tab

def filter_heiko_tables(heiko_sources,heiko_result,jurek_sources,jurek_result):
    non_present_sources = []
    index_non_present_sources = []
    for i in range(len(heiko_sources)):
        if heiko_sources[i] in jurek_sources:
            pass
        else:
            non_present_sources.append(heiko_sources[i])
            index_non_present_sources.append(i)
    new_heiko_result = np.delete(heiko_result,index_non_present_sources,axis=1)
    new_heiko_sources = np.delete(heiko_sources,index_non_present_sources,axis=0)
    new_heiko_tab = [new_heiko_sources,new_heiko_result]
    return new_heiko_tab

def filter_jurek_tables(heiko_sources,heiko_result,jurek_sources,jurek_result):
    non_present_sources = []
    index_non_present_sources = []
    for i in range(len(jurek_sources)):
        if jurek_sources[i] in heiko_sources:
            pass
        else:
            non_present_sources.append(jurek_sources[i])
            index_non_present_sources.append(i)
    new_jurek_result = np.delete(jurek_result,index_non_present_sources,axis=1)
    new_jurek_sources = np.delete(jurek_sources,index_non_present_sources,axis=0)
    new_jurek_tab = [new_jurek_sources,new_jurek_result]
    return new_jurek_tab

def sorting(heiko_sources,heiko_result,jurek_sources,jurek_result):
    new_index_heiko = []
    heiko_sorted_sources = []
    heiko_sorted_result = heiko_result
    for i in range(len(jurek_sources)):
        new_index_heiko.append(heiko_sources.index(jurek_sources[i]))
    for i in range(np.shape(heiko_result)[0]):
        for j in range(np.shape(heiko_result)[1]):
            heiko_sorted_result[i][j] = heiko_result[i][new_index_heiko[j]]
    for i in range(len(heiko_sources)):
        heiko_sorted_sources.append(heiko_sources[new_index_heiko[i]])
    return [heiko_sorted_sources,heiko_sorted_result]

def unit_normalization(path_heiko,path_jurek_helcom,path_jurek_ospar):
    #traitement des donnees
    heiko_tab = open_SR_tab(path_heiko)
    jurek_tab = fusion_open_SR_table(path_jurek_helcom,path_jurek_ospar)
    heiko_sources = heiko_tab[0][1:]
    jurek_sources = jurek_tab[0]
    heiko_result = convert(heiko_tab[2])
    jurek_result = convert(jurek_tab[2])

    filtered_heiko_tab = filter_heiko_tables(heiko_sources,heiko_result,jurek_sources,jurek_result)
    filtered_heiko_sources = filtered_heiko_tab[0]
    filtered_heiko_result = filtered_heiko_tab[1]

    filtered_jurek_tab = filter_jurek_tables(filtered_heiko_sources,filtered_heiko_result,jurek_sources,jurek_result)
    filtered_jurek_sources = filtered_jurek_tab[0]
    filtered_jurek_result = filtered_jurek_tab[1]

    sorted_heiko_tab = sorting(list(filtered_heiko_sources),filtered_heiko_result,list(filtered_jurek_sources),filtered_jurek_result)
    final_heiko_sources = sorted_heiko_tab[0]
    final_heiko_result = sorted_heiko_tab[1]
    final_jurek_sources = filtered_jurek_sources
    final_jurek_result = filtered_jurek_result

    #debut de la normalisation:
    emi = final_heiko_result[-1]
    tc = np.zeros((np.shape(final_jurek_result)))
    for i in range(np.shape(tc)[0]):
        for j in range(np.shape(tc)[1]):
            if emi[j] == 0:
                tc[i][j] = float("nan")
            else:
                tc[i][j] = final_jurek_result[i][j]/emi[j]
    return [final_jurek_sources,tc]

def reshape(sources_1,result_1,sources_2,result_2):
    step_1 = filter_heiko_tables(sources_1,result_1,sources_2,result_2)
    new_sources_1 = step_1[0]
    new_result_1 = step_1[1]
    step_2 = filter_jurek_tables(new_sources_1,new_result_1,sources_2,result_2)
    new_sources_2 = step_2[0]
    new_result_2 = step_2[1]
    step_3 = sorting(list(new_sources_1),new_result_1,list(new_sources_2),new_result_2)
    new2_sources_1 = step_3[0]
    new2_result_1 = step_3[1]
    return [new2_sources_1,new2_result_1,new_sources_2,new_result_2]

def normalization(type_pol,method,first_year_str,last_year_str,choice_4):
    first_year = int(first_year_str)
    last_year = int(last_year_str)
    tc = []
    tc_sources=[]
    if type_pol == "oxidised_nitrogen" or type_pol == "dry_oxidised_nitrogen" or type_pol == "wet_oxidised_nitrogen":
        for i in range(first_year,last_year+1):
            if i == 2015:
                pass
            else:
                path_heiko = "data/data_emi_normalization/"+str(i)+"_oxidised_nitrogen.csv"
                path_jurek_helcom = "data/data_jurek_helcom/"+type_pol+"_"+str(i)+".csv"
                path_jurek_ospar = "data/data_jurek_ospar/"+type_pol+"_"+str(i)+".csv"
                tc.append(unit_normalization(path_heiko,path_jurek_helcom,path_jurek_ospar)[1])
                tc_sources.append(unit_normalization(path_heiko,path_jurek_helcom,path_jurek_ospar)[0])
    elif type_pol == "reduced_nitrogen" or type_pol == "dry_reduced_nitrogen" or type_pol == "wet_reduced_nitrogen":
        for i in range(first_year,last_year+1):
            if i == 2015:
                pass
            else:
                path_heiko = "data/data_emi_normalization/"+str(i)+"_reduced_nitrogen.csv"
                path_jurek_helcom = "data/data_jurek_helcom/"+type_pol+"_"+str(i)+".csv"
                path_jurek_ospar = "data/data_jurek_ospar/"+type_pol+"_"+str(i)+".csv"
                tc.append(unit_normalization(path_heiko,path_jurek_helcom,path_jurek_ospar)[1])
                tc_sources.append(unit_normalization(path_heiko,path_jurek_helcom,path_jurek_ospar)[0])
    table_a_normaliser = fusion_open_SR_table("data/data_jurek_helcom/"+type_pol+"_"+choice_4+".csv","data/data_jurek_ospar/"+type_pol+"_"+choice_4+".csv")
    table_a_normaliser_result = convert(table_a_normaliser[2])
    table_a_normaliser_sources = table_a_normaliser[0]
    new_list_tc = []
    new_list_tc_sources = []
    new_list_table_a_normaliser_sources = []
    new_list_table_a_normaliser_result = []
    for p in range(len(tc)):
        temp = reshape(tc_sources[p],tc[p],table_a_normaliser_sources,table_a_normaliser_result)
        new_tc_sources = temp[0]
        new_tc = temp[1]
        new_table_a_normaliser_sources = temp[2]
        new_table_a_normaliser_result = temp[3]
        new_list_tc_sources.append(new_tc_sources)
        new_list_tc.append(new_tc)
        new_list_table_a_normaliser_sources.append(new_table_a_normaliser_sources)
        new_list_table_a_normaliser_result.append(new_table_a_normaliser_result)
    normalized_table = []
    for p in range(len(new_list_table_a_normaliser_result)):
        tempo = np.zeros((np.shape(new_list_table_a_normaliser_result[p])))
        for i in range(np.shape(tempo)[0]):
            for j in range(np.shape(tempo)[1]):
                tempo[i][j] = new_list_tc[p][i][j]*new_list_table_a_normaliser_result[p][i][j]
        normalized_table.append(tempo)
    #print(new_list_table_a_normaliser_sources)
    return [new_list_tc_sources,new_list_tc,new_list_table_a_normaliser_sources,normalized_table,table_a_normaliser[1]]

def mean(tab_sources,tab_result,tab_receptors):
    list_all_sources = []
    list_position = []
    for p in range(len(tab_sources)):
        for i in range(len(tab_sources[p])):
            if tab_sources[p][i] in list_all_sources:
                pass
            else:
                list_all_sources.append(tab_sources[p][i])
    #list_index_sources = np.zeros((len(tab_sources),len(list_all_sources)))
    for k in range(len(list_all_sources)):
        temp = []
        for p in range(len(tab_sources)):
            if list_all_sources[k] in tab_sources[p]:
                temp.append(p)
            else:
                pass
        list_position.append(temp)
    tab_moyenne = np.zeros((len(tab_receptors),len(list_all_sources)))
    for j in range(len(list_position)):
        for k in range(len(list_position[j])):
            for i in range(len(tab_receptors)):
                ind = list(tab_sources[list_position[j][k]]).index(list_all_sources[j])
                tab_moyenne[i][j] = tab_moyenne[i][j] + tab_result[list_position[j][k]][i][ind]
    for i in range(np.shape(tab_moyenne)[0]):
        for j in range(np.shape(tab_moyenne)[1]):
            tab_moyenne[i][j] = tab_moyenne[i][j]/len(list_position[j])
    return [list_all_sources,tab_moyenne,tab_receptors]

def median(tab_sources,tab_result,tab_receptors):
    list_all_sources = []
    list_position = []
    for p in range(len(tab_sources)):
        for i in range(len(tab_sources[p])):
            if tab_sources[p][i] in list_all_sources:
                pass
            else:
                list_all_sources.append(tab_sources[p][i])
    #list_index_sources = np.zeros((len(tab_sources),len(list_all_sources)))
    for k in range(len(list_all_sources)):
        temp = []
        for p in range(len(tab_sources)):
            if list_all_sources[k] in tab_sources[p]:
                temp.append(p)
            else:
                pass
        list_position.append(temp)
    tab_median = np.empty((len(tab_receptors),len(list_all_sources)),dtype=list)
    for i in range(np.shape(tab_median)[0]):
        for j in range(np.shape(tab_median)[1]):
            tab_median[i][j] = []
    for j in range(len(list_position)):
        for k in range(len(list_position[j])):
            for i in range(len(tab_receptors)):
                ind = list(tab_sources[list_position[j][k]]).index(list_all_sources[j])
                tab_median[i][j].append(tab_result[list_position[j][k]][i][ind])
    for i in range(np.shape(tab_median)[0]):
        for j in range(np.shape(tab_median)[1]):
            tab_median[i][j] = sc.median(tab_median[i][j])
    return [list_all_sources,tab_median,tab_receptors]

def making_output(namelist_receptors,namelist_sources,result,filename):
    file = open(filename,"w")
    file.write("\n")
    file = open(filename,"a")
    #Ecriture de la premiere ligne c'est a dire les sources:
    file.write("\t")
    #file.write("\t")
    for i in range(len(namelist_sources)):
        file.write(namelist_sources[i])
        file.write("\t")
    #Ecriture du tableau et en prmiere colonne les recepteurs
    file.write("\n")
    for i in range(np.shape(result)[0]):
        for j in range(np.shape(result)[1]+1):
            if j == 0:
                file.write(namelist_receptors[i])
                file.write("\t")
            else:
                file.write(str(result[i][j-1]))
                file.write("\t")
        file.write("\n")


#A=normalization("wet_reduced_nitrogen","average","2016","2020","2019")
#B=median(A[2],A[3],A[4])
#making_output(B[2],B[0],B[1])
#print(B)

### Selectors:

print("This program make a normalization for the SR tables between 1995 and 2020 (you can select the first year and the last year for the normalization, the method for the normalization) and the year that you want to normalize.")
print("Author: Henon Aurelien, aurelien.henon@meteo.fr, 2022")
print("------------------------------------")
print("You can use a normalization between 1995 and 2020 with Heiko's tables and Jurek's tables or a normalization between 2016 and 2020 with Michael's tables.")
print("1: 1995-2020")
print("2: 2016-2020")
print("Please make a choice: ")
token_1 = 0
while token_1 ==0:
    choice_1 = input()
    if choice_1 != "1" and choice_1 !="2":
        print("Incorrect input, please retry:")
        token_1 = 0
    else:
        token_1 = 1
print("------------------------------------")
if choice_1 == "1":
    print("What method do you want for the normalization. (average/median)")
    print("Please, select 1 or 2:")
    print("1: average")
    print("2: median")
    token_2 = 0
    while token_2 == 0:
        choice_2 = input()
        if choice_2 !="1" and choice_2 !="2":
            print("Incorrect input, please retry:")
            token_2 = 0
        else:
            token_2=1
    if choice_2 == "1":
        choice_2 = "average"
    elif choice_2 == "2":
        choice_2 = "median"
    print("------------------------------------")
    print("Please, select the first year that you want for normalization. (between 1995 and 2020) ")
    token_3 = 0
    while token_3 == 0:
        first_year = input()
        if int(first_year) <1995 or int(first_year) > 2020:
            print("Incorrect input, please retry:")
            token_3 = 0
        else:
            token_3 = 1
    print("Please, select the first year that you want for normalization. (between 1995 and 2020 and > first year)")
    token_4 = 0
    while token_4 ==0:
        last_year = input()
        if int(last_year) <1995 or int(last_year) > 2020 or int(last_year)<int(first_year):
            print("Incorrect input, please retry:")
            token_4 = 0
        else:
            token_4 = 1
    print("------------------------------------")
    print("Please select the parameter that you want: (select 1,2,3,4,5 or 6)")
    print("1: dry reduced nitrogen")
    print("2: wet reduced nitrogen")
    print("3: dry oxidised nitrogen")
    print("4: wet oxidised nitrogen")
    print("5: reduced nitrogen")
    print("6: oxidised nitrogen")
    token_5 = 0
    while token_5 ==0:
        choice_5 = input()
        if choice_5 != "1" and choice_5 != "2" and choice_5 != "3" and choice_5 != "4" and choice_5 != "5" and choice_5 != "6":
            print("Incorrect input, please retry:")
            token_5 = 0
        else:
            token_5 = 1
    if choice_5 == "1":
        choice_5 = "dry_reduced_nitrogen"
    elif choice_5 == "2":
        choice_5 = "wet_reduced_nitrogen"
    elif choice_5 == "3":
        choice_5 = "dry_oxidised_nitrogen"
    elif choice_5 == "4":
        choice_5 = "wet_oxidised_nitrogen"
    elif choice_5 == "5":
        choice_5 = "reduced_nitrogen"
    elif choice_5 == "6":
        choice_5 = "oxidised_nitrogen"
    print("------------------------------------")
    print("Please select the year to normalize between 1995 and 2020:")
    print("Example: 2005")
    print("Warning: The year 2015 is not available due to a restriction of the budget.")
    token_6 = 0
    while token_6 == 0:
        choice_6 = input()
        if int(choice_6) < 1995 or int(choice_6)> 2020 or int(choice_6)==2015:
            print("Incorrect input, please retry:")
            token_6 = 0
        else:
            token_6 = 1
    print("------------------------------------")
    print("What kind of output do you want ? (Please select your(s) output(s)")
    print("1: the normalized SR table (output_SR.txt)")
    print("2: all transfer coefficients (output_TC_year.txt)")
    print("3: the normalized SR table and all transfer coefficients (output_SR.txt and output_TC.txt)")
    token_7 = 0
    while token_7 == 0:
        choice_7 = input()
        if choice_7 != "1" and choice_7 != "2" and choice_7 != "3":
            print("Incorrect input, please retry:")
            token_7 = 0
        else:
            token_7 = 1
    A = normalization(choice_5,choice_2,first_year,last_year,choice_6)
    if choice_2 == "average":
        B = mean(A[2],A[3],A[4])
    elif choice_2 == "median":
        B = median(A[2],A[3],A[4])

    if choice_7 == "1":
        making_output(B[2],B[0],B[1],"output_SR.txt")
    elif choice_7 == "2":
        for i in range(len(A[0])):
            making_output(A[4],A[0][i],A[1][i],"output_TC_"+str(int(first_year)+i)+".txt")
    elif choice_7 == "3":
        making_output(B[2],B[0],B[1],"output_SR.txt")
        for i in range(len(A[0])):
            making_output(A[4],A[0][i],A[1][i],"output_TC_"+str(int(first_year)+i)+".txt")
#elif choice_1 == "2":
