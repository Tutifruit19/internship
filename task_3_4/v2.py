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
            path_heiko = "data/data_emi_normalization/"+str(i)+"_oxidised_nitrogen.csv"
            path_jurek_helcom = "data/data_jurek_helcom/"+type_pol+"_"+str(i)+".csv"
            path_jurek_ospar = "data/data_jurek_ospar/"+type_pol+"_"+str(i)+".csv"
            tc.append(unit_normalization(path_heiko,path_jurek_helcom,path_jurek_ospar)[1])
            tc_sources.append(unit_normalization(path_heiko,path_jurek_helcom,path_jurek_ospar)[0])
    elif type_pol == "reduced_nitrogen" or type_pol == "dry_reduced_nitrogen" or type_pol == "wet_reduced_nitrogen":
        for i in range(first_year,last_year+1):
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
    return [new_list_tc_sources,new_list_tc,new_list_table_a_normaliser_sources,normalized_table,table_a_normaliser[1]]

def making_output(namelist_emitters,namelist_soures,result):
    file = open("output_SR.txt","w")
    file.write("\n")
    file = open("output_SR.txt","a")
    #Ecriture de la premiere ligne c'est a dire les sources:
    file.write("\t")
    file.write("\t")
    for i in range(len(name_list_sources)):



normalization("dry_reduced_nitrogen","average","1999","2010","2002")