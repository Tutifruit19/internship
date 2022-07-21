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

#print(open_SR_tab("/home/aurelienh/task_3and4/data/dry_reduced_nitrogen_2016.csv"))

def convert(tab):
    float_tab = np.zeros((np.shape(tab)[0]-1,np.shape(tab)[1]-1))
    for i in range(1,np.shape(tab)[0]):
        for j in range(1,np.shape(tab)[1]):
            if tab[i][j]=="":
                float_tab[i-1][j-1]=0
            else:
                float_tab[i-1][j-1] = float(tab[i][j])
    return float_tab

def making_output(tab):
    name_list_emitters = tab[0]
    name_list_receptors = tab[1]
    result = convert(tab[2])
    file = open("output_SR.txt","w")
    file.write(choice_3bis)
    file = open("output_SR.txt","a")
    file.write("\n")
    file.write("\n")
    file.write("-----------------------------------------------")
    file.write("\n")
    file.write("\t")
    file.write("\t")
    for i in range(len(name_list_emitters)):#First line contruction: emitters
        file.write(name_list_emitters[i])
        file.write("\t")
    file.write("\n")
    for i in range(np.shape(result)[0]):
        file.write(name_list_receptors[i])#construction of the first column: recpetors name
        file.write("\t")
        for j in range(np.shape(result)[1]):
            file.write(str(result[i][j]))#Value of the table
            file.write("\t")
        file.write("\n")
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
    return [SR_name_emitters,SR_name_receptors,result,filename_1,filename_2]


def making_output_3(tab,choice_3bis,choice_4,type_pol,method,first_year,last_year):
    name_list_emitters = tab[0]
    name_list_receptors = tab[1]
    if choice_0 == "yes":
        result = normalization(open_SR_tab("data/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,method,first_year,last_year)
    elif choice_0 == "no":
        result = normalization(fusion_open_SR_table("data/data_jurek_helcom/"+choice_3bis+"_"+choice_4+".csv","data/data_jurek_ospar/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,method,first_year,last_year)
    file = open("output_SR.txt","w")
    file.write(choice_3bis+" normalized with the "+choice_1bis+" of the 2016-2020 meteorology.")
    file = open("output_SR.txt","a")
    file.write("\n")
    file.write("\n")
    file.write("-----------------------------------------------")
    file.write("\n")
    file.write("\t")
    file.write("\t")
    for i in range(len(name_list_emitters)):#First line contruction: emitters
        file.write(name_list_emitters[i])
        file.write("\t")
    file.write("\n")
    for i in range(np.shape(result)[0]):
        file.write(name_list_receptors[i])#construction of the first column: recpetors name
        file.write("\t")
        for j in range(np.shape(result)[1]):
            file.write(str(result[i][j]))#Value of the table
            file.write("\t")
        file.write("\n")
#making_output(open_SR_tab("/home/aurelienh/task_3and4/data/dry_reduced_nitrogen_2018.csv"))
def making_output_4(tab,receptors_name,choice_3bis,choice_4,type_pol,method,first_year,last_year):
    name_list_emitters = tab[0]
    name_list_receptors_all = tab[1]
    if choice_0 == "yes":
        result = normalization(open_SR_tab("data/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,method,first_year,last_year)
    elif choice_0 == "no":
        result = normalization(fusion_open_SR_table("data/data_jurek_helcom/"+choice_3bis+"_"+choice_4+".csv","data/data_jurek_ospar/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,method,first_year,last_year)
    index_receptors = []
    receptors_name_list = receptors_name.split(",")
    for i in range(len(receptors_name_list)):
        index_receptors.append(name_list_receptors_all.index(receptors_name_list[i]))
    file = open("output_SR.txt","w")
    file.write(choice_3bis+" normalized with the "+choice_1bis+" of the 2016-2020 meteorology.")
    file = open("output_SR.txt","a")
    file.write("\n")
    file.write("\n")
    file.write("-----------------------------------------------")
    file.write("\n")
    file.write("\t")
    file.write("\t")
    for i in range(len(name_list_emitters)):#First line contruction: emitters
        file.write(name_list_emitters[i])
        file.write("\t")
    file.write("\n")
    for i in range(np.shape(result)[0]):
        if i in index_receptors:
            file.write(name_list_receptors_all[i])#construction of the first column: recpetors name
            file.write("\t")
            for j in range(np.shape(result)[1]):
                file.write(str(result[i][j]))#Value of the table
                file.write("\t")
            file.write("\n")
        else:
            pass

def making_output_2(tab,receptors_name):
    name_list_emitters = tab[0]
    name_list_receptors_all = tab[1]
    result = convert(tab[2])
    index_receptors = []
    receptors_name_list = receptors_name.split(",")
    for i in range(len(receptors_name_list)):
        index_receptors.append(name_list_receptors_all.index(receptors_name_list[i]))
    file = open("output_SR.txt","w")
    file.write(tab[3][39:-4])
    file = open("output_SR.txt","a")
    file.write("\n")
    file.write("\n")
    file.write("-----------------------------------------------")
    file.write("\n")
    file.write("\t")
    file.write("\t")
    for i in range(len(name_list_emitters)):#First line contruction: emitters
        file.write(name_list_emitters[i])
        file.write("\t")
    file.write("\n")
    for i in range(np.shape(result)[0]):
        if i in index_receptors:
            file.write(name_list_receptors_all[i])#construction of the first column: recpetors name
            file.write("\t")
            for j in range(np.shape(result)[1]):
                file.write(str(result[i][j]))#Value of the table
                file.write("\t")
            file.write("\n")
        else:
            pass

def normalization(tab,type_pol,method,first_year_str,last_year_str):
    """emi_reduced_nitrogen_2016 = []
    emi_reduced_nitrogen_2017 = []
    emi_reduced_nitrogen_2018 = []
    emi_reduced_nitrogen_2019 = []
    emi_reduced_nitrogen_2020 = []
    emi_oxidised_nitrogen_2016 = []
    emi_oxidised_nitrogen_2017 = []
    emi_oxidised_nitrogen_2018 = []
    emi_oxidised_nitrogen_2019 = []
    emi_oxidised_nitrogen_2020 = []"""
    first_year = int(first_year_str)
    last_year = int(last_year_str)

    emi_reduced_nitrogen = []
    emi_oxidised_nitrogen = []
    number_year = (last_year - first_year) + 1
    for p in range(number_year):
        emi_reduced_nitrogen.append([])
        emi_oxidised_nitrogen.append([])

    compteur = 0
    for p in range(first_year,last_year+1):
        tab_reduced_nitrogen = open_SR_tab("data/data_emi_normalization/"+str(p)+"_reduced_nitrogen.csv")
        for i in range(1,np.shape(tab_reduced_nitrogen[2])[1]):
            if tab_reduced_nitrogen[2][-1][i] == "":
                emi_reduced_nitrogen[compteur].append(0.0)
            else:
                emi_reduced_nitrogen[compteur].append(float(tab_reduced_nitrogen[2][-1][i]))
        compteur = compteur + 1
    compteur = 0
    for p in range(first_year,last_year+1):
        tab_oxidised_nitrogen = open_SR_tab("data/data_emi_normalization/"+str(p)+"_oxidised_nitrogen.csv")
        for i in range(1,np.shape(tab_oxidised_nitrogen[2])[1]):
            if tab_oxidised_nitrogen[2][-1][i] == "":
                emi_oxidised_nitrogen[compteur].append(0.0)
            else:
                emi_oxidised_nitrogen[compteur].append(float(tab_oxidised_nitrogen[2][-1][i]))
        compteur = compteur + 1


    """tab_reduced_nitrogen_2017 = open_SR_tab("data/reduced_nitrogen_2017.csv")
    for i in range(1,np.shape(tab_reduced_nitrogen_2017[2])[1]):
        if tab_reduced_nitrogen_2017[2][-1][i] == "":
            emi_reduced_nitrogen_2017.append(0.0)
        else:
            emi_reduced_nitrogen_2017.append(float(tab_reduced_nitrogen_2017[2][-1][i]))
    tab_reduced_nitrogen_2018 = open_SR_tab("data/reduced_nitrogen_2018.csv")
    for i in range(1,np.shape(tab_reduced_nitrogen_2018[2])[1]):
        if tab_reduced_nitrogen_2018[2][-1][i] == "":
            emi_reduced_nitrogen_2018.append(0.0)
        else:
            emi_reduced_nitrogen_2018.append(float(tab_reduced_nitrogen_2018[2][-1][i]))
    tab_reduced_nitrogen_2019 = open_SR_tab("data/reduced_nitrogen_2019.csv")
    for i in range(1,np.shape(tab_reduced_nitrogen_2019[2])[1]):
        if tab_reduced_nitrogen_2019[2][-1][i] == "":
            emi_reduced_nitrogen_2019.append(0.0)
        else:
            emi_reduced_nitrogen_2019.append(float(tab_reduced_nitrogen_2019[2][-1][i]))
    tab_reduced_nitrogen_2020 = open_SR_tab("data/reduced_nitrogen_2020.csv")
    for i in range(1,np.shape(tab_reduced_nitrogen_2020[2])[1]):
        if tab_reduced_nitrogen_2020[2][-1][i] == "":
            emi_reduced_nitrogen_2020.append(0.0)
        else:
            emi_reduced_nitrogen_2020.append(float(tab_reduced_nitrogen_2020[2][-1][i]))
    tab_oxidised_nitrogen_2016 = open_SR_tab("data/oxidised_nitrogen_2016.csv")
    for i in range(1,np.shape(tab_oxidised_nitrogen_2016[2])[1]):
        if tab_oxidised_nitrogen_2016[2][-1][i] == "":
            emi_oxidised_nitrogen_2016.append(0.0)
        else:
            emi_oxidised_nitrogen_2016.append(float(tab_oxidised_nitrogen_2016[2][-1][i]))
    tab_oxidised_nitrogen_2017 = open_SR_tab("data/oxidised_nitrogen_2017.csv")
    for i in range(1,np.shape(tab_oxidised_nitrogen_2017[2])[1]):
        if tab_oxidised_nitrogen_2017[2][-1][i] == "":
            emi_oxidised_nitrogen_2017.append(0.0)
        else:
            emi_oxidised_nitrogen_2017.append(float(tab_oxidised_nitrogen_2017[2][-1][i]))
    tab_oxidised_nitrogen_2018 = open_SR_tab("data/oxidised_nitrogen_2018.csv")
    for i in range(1,np.shape(tab_oxidised_nitrogen_2018[2])[1]):
        if tab_oxidised_nitrogen_2018[2][-1][i] == "":
            emi_oxidised_nitrogen_2018.append(0.0)
        else:
            emi_oxidised_nitrogen_2018.append(float(tab_oxidised_nitrogen_2018[2][-1][i]))
    tab_oxidised_nitrogen_2019 = open_SR_tab("data/oxidised_nitrogen_2019.csv")
    for i in range(1,np.shape(tab_oxidised_nitrogen_2019[2])[1]):
        if tab_oxidised_nitrogen_2019[2][-1][i] == "":
            emi_oxidised_nitrogen_2019.append(0.0)
        else:
            emi_oxidised_nitrogen_2019.append(float(tab_oxidised_nitrogen_2019[2][-1][i]))
    tab_oxidised_nitrogen_2020 = open_SR_tab("data/oxidised_nitrogen_2020.csv")
    for i in range(1,np.shape(tab_oxidised_nitrogen_2020[2])[1]):
        if tab_oxidised_nitrogen_2020[2][-1][i] == "":
            emi_oxidised_nitrogen_2020.append(0.0)
        else:
            emi_oxidised_nitrogen_2020.append(float(tab_oxidised_nitrogen_2020[2][-1][i]))"""
    SR_tab = []
    result_jurek = []
    if choice_0 == "no":
        for p in range(first_year,last_year+1):
            SR_tab_tempo = fusion_open_SR_table("data/data_jurek_helcom/"+type_pol+"_"+str(p)+".csv","data/data_jurek_ospar/"+type_pol+"_"+str(p)+".csv")
            result_jurek_tempo = convert(SR_tab_tempo[2])
            SR_tab.append(SR_tab_tempo)
            result_jurek.append(result_jurek_tempo)
    elif choice_0 == "yes":
        for p in range(first_year,last_year+1):
            SR_tab_tempo = open_SR_tab("data/"+type_pol+"_"+str(p)+".csv")
            result_jurek_tempo = convert(SR_tab_tempo[2])
            SR_tab.append(SR_tab_tempo)
            result_jurek.append(result_jurek_tempo)

    """SR_tab_2016 = fusion_open_SR_tab("data/data_jurek_helcom/"+type_pol+"_2016.csv","data/data_jurek_ospar/"+type_pol+"_2016.csv")
    result_2016 = convert(SR_tab_2016[2])
    SR_tab_2017 = open_SR_tab("data/"+type_pol+"_2017.csv")
    result_2017 = convert(SR_tab_2017[2])
    SR_tab_2018 = open_SR_tab("data/"+type_pol+"_2018.csv")
    result_2018 = convert(SR_tab_2018[2])
    SR_tab_2019 = open_SR_tab("data/"+type_pol+"_2019.csv")
    result_2019 = convert(SR_tab_2019[2])
    SR_tab_2020 = open_SR_tab("data/"+type_pol+"_2020.csv")
    result_2020 = convert(SR_tab_2020[2])"""

    tc = []
    compteur = 0
    for p in range(first_year,last_year+1):
        tc_tempo = np.zeros((np.shape(result_jurek[compteur])))
        tc.append(tc_tempo)
        compteur = compteur + 1

    """tc_2016 = np.zeros((np.shape(result_2016)))
    tc_2017 = np.zeros((np.shape(result_2017)))
    tc_2018 = np.zeros((np.shape(result_2018)))
    tc_2019 = np.zeros((np.shape(result_2019)))
    tc_2020 = np.zeros((np.shape(result_2020)))"""
    if type_pol == "oxidised_nitrogen" or type_pol == "dry_oxidised_nitrogen" or type_pol == "wet_oxidised_nitrogen":
        for p in range(np.shape(tc)[0]):
            for i in range(np.shape(tc)[1]):
                for j in range(np.shape(tc)[2]):
                    if emi_oxidised_nitrogen[p][j] != 0:
                        tc[p][i][j] = result_jurek[p][i][j]/emi_oxidised_nitrogen[p][j]
                    else:
                        tc[p][i][j] = float("nan")
    elif type_pol == "reduced_nitrogen" or type_pol == "dry_reduced_nitrogen" or type_pol == "wet_reduced_nitrogen":
        for p in range(np.shape(tc)[0]):
            for i in range(np.shape(tc)[1]):
                for j in range(np.shape(tc)[2]):
                    if emi_reduced_nitrogen[p][j] != 0:
                        tc[p][i][j] = result_jurek[p][i][j]/emi_reduced_nitrogen[p][j]
                    else:
                        tc[p][i][j] = float("nan")

    """if type_pol == "oxidised_nitrogen" or type_pol == "dry_oxidised_nitrogen" or type_pol == "wet_oxidised_nitrogen":
        for i in range(np.shape(tc_2016)[0]):
            for j in range(np.shape(tc_2016)[1]):
                if emi_oxidised_nitrogen_2016[j] !=0:
                    tc_2016[i][j] = result_2016[i][j]/emi_oxidised_nitrogen_2016[j]
                else:
                    tc_2016[i][j] = float("nan")
        for i in range(np.shape(tc_2017)[0]):
            for j in range(np.shape(tc_2017)[1]):
                if emi_oxidised_nitrogen_2017[j] !=0:
                    tc_2017[i][j] = result_2017[i][j]/emi_oxidised_nitrogen_2017[j]
                else:
                    tc_2017[i][j] = float("nan")
        for i in range(np.shape(tc_2018)[0]):
            for j in range(np.shape(tc_2018)[1]):
                if emi_oxidised_nitrogen_2018[j] !=0:
                    tc_2018[i][j] = result_2018[i][j]/emi_oxidised_nitrogen_2018[j]
                else:
                    tc_2018[i][j] = float("nan")
        for i in range(np.shape(tc_2019)[0]):
            for j in range(np.shape(tc_2019)[1]):
                if emi_oxidised_nitrogen_2019[j] !=0:
                    tc_2019[i][j] = result_2019[i][j]/emi_oxidised_nitrogen_2019[j]
                else:
                    tc_2019[i][j] = float("nan")
        for i in range(np.shape(tc_2020)[0]):
            for j in range(np.shape(tc_2020)[1]):
                if emi_oxidised_nitrogen_2020[j] !=0:
                    tc_2020[i][j] = result_2020[i][j]/emi_oxidised_nitrogen_2020[j]
                else:
                    tc_2020[i][j] = float("nan")
    elif type_pol == "reduced_nitrogen" or type_pol == "dry_reduced_nitrogen" or type_pol == "wet_reduced_nitrogen":
        for i in range(np.shape(tc_2016)[0]):
            for j in range(np.shape(tc_2016)[1]):
                if emi_reduced_nitrogen_2016[j] !=0:
                    tc_2016[i][j] = result_2016[i][j]/emi_reduced_nitrogen_2016[j]
                else:
                    tc_2016[i][j] = float("nan")
        for i in range(np.shape(tc_2017)[0]):
            for j in range(np.shape(tc_2017)[1]):
                if emi_reduced_nitrogen_2017[j] !=0:
                    tc_2017[i][j] = result_2017[i][j]/emi_reduced_nitrogen_2017[j]
                else:
                    tc_2017[i][j] = float("nan")
        for i in range(np.shape(tc_2018)[0]):
            for j in range(np.shape(tc_2018)[1]):
                if emi_reduced_nitrogen_2018[j] !=0:
                    tc_2018[i][j] = result_2018[i][j]/emi_reduced_nitrogen_2018[j]
                else:
                    tc_2018[i][j] = float("nan")
        for i in range(np.shape(tc_2019)[0]):
            for j in range(np.shape(tc_2019)[1]):
                if emi_reduced_nitrogen_2019[j] != 0:
                    tc_2019[i][j] = result_2019[i][j]/emi_reduced_nitrogen_2019[j]
                else:
                    tc_2019[i][j] = float("nan")
        for i in range(np.shape(tc_2020)[0]):
            for j in range(np.shape(tc_2020)[1]):
                if emi_reduced_nitrogen_2020[j] != 0:
                    tc_2020[i][j] = result_2020[i][j]/emi_reduced_nitrogen_2020[j]
                else:
                    tc_2020[i][j] = float("nan")"""

    name_list_emitters = tab[0]
    name_list_receptors_all = tab[1]
    result = convert(tab[2])

    normalized = []
    for p in range(first_year,last_year+1):
        normalized.append(np.zeros((np.shape(result))))

    """normalized_2016 = np.zeros((np.shape(result)))
    normalized_2017 = np.zeros((np.shape(result)))
    normalized_2018 = np.zeros((np.shape(result)))
    normalized_2019 = np.zeros((np.shape(result)))
    normalized_2020 = np.zeros((np.shape(result)))"""

    for p in range(np.shape(normalized)[0]):
        for i in range(np.shape(normalized)[1]):
            for j in range(np.shape(normalized)[2]):
                normalized[p][i][j] = tc[p][i][j]*result[i][j]

    """for i in range(np.shape(normalized_2016)[0]):
        for j in range(np.shape(normalized_2016)[1]):
            normalized_2016[i][j] = tc_2016[i][j]*result[i][j]
    for i in range(np.shape(normalized_2017)[0]):
        for j in range(np.shape(normalized_2017)[1]):
            normalized_2017[i][j] = tc_2017[i][j]*result[i][j]
    for i in range(np.shape(normalized_2018)[0]):
        for j in range(np.shape(normalized_2018)[1]):
            normalized_2018[i][j] = tc_2018[i][j]*result[i][j]
    for i in range(np.shape(normalized_2019)[0]):
        for j in range(np.shape(normalized_2019)[1]):
            normalized_2019[i][j] = tc_2019[i][j]*result[i][j]
    for i in range(np.shape(normalized_2020)[0]):
        for j in range(np.shape(normalized_2020)[1]):
            normalized_2020[i][j] = tc_2020[i][j]*result[i][j]"""


    """substract = [normalized_2016,normalized_2017,normalized_2018,normalized_2019,normalized_2020]
    somme = np.zeros((np.shape(normalized_2020)))
    median_tab = np.empty(np.shape(somme),dtype=list)#start the stuff
    for i in range(np.shape(median_tab)[0]):
        for j in range(np.shape(median_tab)[1]):
            median_tab[i][j] = []
    for i in range(np.shape(median_tab)[0]):
        for j in range(np.shape(median_tab)[1]):
            compteur = 0
            for k in range(2016,2020+1):
                if k<int(first_year):
                    pass
                elif k>int(last_year):
                    pass
                else:
                    median_tab[i][j].append(substract[compteur][i][j])
                compteur = compteur + 1
    compteur_bis = 5
    for i in range(np.shape(normalized_2020)[0]):
        for j in range(np.shape(normalized_2020)[1]):
            somme[i][j] = normalized_2016[i][j]+normalized_2017[i][j]+normalized_2018[i][j]+normalized_2019[i][j]+normalized_2020[i][j]
    for k in range(2016,2020+1):
        if k<int(first_year):
            for i in range(np.shape(somme)[0]):
                for j in range(np.shape(somme)[1]):
                    somme[i][j] = somme[i][j] - substract[5-compteur_bis][i][j]
            del substract[5-compteur_bis]
            compteur_bis = compteur_bis - 1
        elif k>int(last_year):
            for i in range(np.shape(somme)[0]):
                for j in range(np.shape(somme)[1]):
                    somme[i][j] = somme[i][j] - substract[5-compteur_bis][i][j]
            del substract[5-compteur_bis]
            compteur_bis = compteur_bis - 1
    normalized_table = np.zeros((np.shape(normalized_2020)))
    if method =="average":
        for i in range(np.shape(normalized_table)[0]):
            for j in range(np.shape(normalized_table)[1]):
                normalized_table[i][j]= (somme[i][j])/compteur_bis
    elif method =="median":
        for i in range(np.shape(normalized_table)[0]):
            for j in range(np.shape(normalized_table)[1]):
                normalized_table[i][j] = sc.median(median_tab[i][j])"""

    if method == "average":
        normalized_table = np.zeros((np.shape(normalized)[1:]))
        for i in range(np.shape(normalized)[1]):
            for j in range(np.shape(normalized)[2]):
                for p in range(np.shape(normalized)[0]):
                    normalized_table[i][j]=normalized_table[i][j]+normalized[p][i][j]
                normalized_table[i][j] = normalized_table[i][j]/(np.shape(normalized)[0])
    elif method == "median":
        median_tab = np.empty(np.shape(normalized)[1:],dtype=list)
        for i in range(np.shape(median_tab)[0]):
            for j in range(np.shape(median_tab)[1]):
                median_tab[i][j] = []
        for i in range(np.shape(median_tab)[0]):
            for j in range(np.shape(median_tab)[1]):
                for p in range(np.shape(normalized)[0]):
                    median_tab[i][j].append(normalized[p][i][j])
        normalized_table = np.zeros((np.shape(normalized)[1:]))
        for i in range(np.shape(normalized)[1]):
            for j in range(np.shape(normalized)[2]):
                normalized_table[i][j] = sc.median(median_tab[i][j])
    return normalized_table

#print(normalization(open_SR_tab("/home/aurelienh/task_3and4/data/dry_oxidised_nitrogen_2018.csv"),"oxidised_nitrogen","average"))
#print(open_SR_tab("/home/aurelienh/task_3and4/data/data_jurek_ospar/wet_oxidised_nitrogen_2007.csv"))


### All Selection before to run the the routine
print("-----------------------------------------------")
print("\n")
print("\n")
print("This routine creates SR tables between ??? and 2020. You can choose receptors that you want and if you want normalized SR tables (the normalization is made with 2016-2020 meteorology)")
print("\n")
print("\n")
print("-----------------------------------------------")
print("\n")
print("Do you want a normalization with 2016-2020 years and for a year between these years ? because all the receptors are not available before. If you wwant before you can use 1995-2020 normalization or less but just for Helcom and Ospar receptors. (yes/no)")
token_0 = 0
while token_0 == 0:
    choice_0 = input()
    if choice_0 != "yes" and choice_0 != "no":
        token_0 = 0
        print("Incorrect input, please try again:")
    else:
        token_0 = 1
print("\n")
print("\n")
print("-----------------------------------------------")
if choice_0 == "yes":
    print("Do you want brute SR tables or normalized SR tables ? (brute/normalized)")
    token_1 = 0
    while token_1 ==0:
        choice_1 = input()
        if choice_1 !="brute" and choice_1 !="normalized":
            token_1=0
            print("Incorrect input, please try again:")
        else:
            token_1=1
    print("-----------------------------------------------")
    if choice_1 =="normalized":
        print("\n")
        print("\t")
        print("Which method do you want for the normalization ? (average/median)")
        token_1bis = 0
        while token_1bis == 0:
            choice_1bis = input()
            if choice_1bis != "average" and choice_1bis != "median":
                token_1bis = 0
                print("Incorrect input, please try again:")
            else:
                token_1bis = 1
    else:
        pass
    if choice_1 == "normalized":
        print("-----------------------------------------------")
        print("\n")
        print("\t")
        print("Do you want a normalisation with all avalaible years ? (yes/no)")
        token_1n = 0
        while token_1n == 0:
            choice_1n = input()
            if choice_1n != "yes" and choice_1n != "no":
                token_1n = 0
                print("Incorrect input, please try again:")
            else:
                token_1n = 1
        if choice_1n == "no":
            print("-----------------------------------------------")
            print("\n")
            print("\t")
            print("Select the first year between 2016 and 2020:")
            token_1f = 0
            while token_1f == 0:
                first_year = input()
                if first_year != "2016" and first_year != "2017" and first_year != "2018" and first_year != "2019" and first_year != "2020":
                    token_1f = 0
                    print("Incorrect input, please try again")
                else:
                    token_1f = 1

            print("Select the last year between 2016 and 2020: (> first year)")
            token_1f = 0
            while token_1f == 0:
                last_year = input()
                if last_year != "2016" and last_year != "2017" and last_year != "2018" and last_year != "2019" and last_year != "2020":
                    token_1f = 0
                    print("Incorrect input, please try again")
                else:
                    token_1f = 1
        else:
            first_year = 2016
            last_year = 2020
    else:
        pass
    print("Do you want all the receptors ? (yes/no)")
    token_2 = 0
    while token_2==0:
        choice_2 = input()
        if choice_2 !="yes" and choice_2 !="no":
            token_2=0
            print("Incorrect input, please try again:")
        else:
            token_2 =1
    if choice_2 == "no":
        print("Select the receptors.")
        print("The format must be: EEZ48,EEZ65,EEZ71")
        print("Please enter the zones separated by comma with no blanks:")
        str_receptors = input()
    else:
        pass
    print("-----------------------------------------------")
    print("\n")
    print("Please, select your parameters: oxidised nitrogen, dry oxidised nitrogen, wet oxidised nitrogen, reduced nitrogen, dry reduced nitrogen, wet reduced nitrogen ?")
    print("Example: wet oxidised nitrogen")
    print("Please enter without capital letter:")
    token_3 = 0
    while token_3 == 0:
        choice_3 = input()
        if choice_3 != "oxidised nitrogen" and choice_3 != "dry oxidised nitrogen" and choice_3 != "wet oxidised nitrogen" and choice_3 != "reduced nitrogen" and choice_3 != "dry reduced nitrogen" and choice_3 != "wet reduced nitrogen":
            token_3 = 0
            print("Incorrect input, please try again:")
        else:
            if choice_3 == "oxidised nitrogen":
                choice_3bis = "oxidised_nitrogen"
            elif choice_3 == "dry oxidised nitrogen":
                choice_3bis = "dry_oxidised_nitrogen"
            elif choice_3 == "wet oxidised nitrogen":
                choice_3bis = "wet_oxidised_nitrogen"
            elif choice_3 == "reduced nitrogen":
                choice_3bis = "reduced_nitrogen"
            elif choice_3 == "dry reduced nitrogen":
                choice_3bis = "dry_reduced_nitrogen"
            elif choice_3 == "wet reduced nitrogen":
                choice_3bis = "wet_reduced_nitrogen"
            token_3 = 1
    print("-----------------------------------------------")
    print("\n")
    print("Please select a year: 2016,2017,2018,2019,2020")
    token_4 = 0
    while token_4 == 0:
        choice_4 = input()
        if choice_4 != "2016" and choice_4 != "2017" and choice_4 != "2018" and choice_4 != "2019" and choice_4 != "2020":
            token_4 = 0
            print("Incorrect input, please try again")
        else:
            token_4 = 1
    print("-----------------------------------------------")
    print("The text file output_SR.txt has been created. It include the SR table based on yours choices.")
    print("-----------------------------------------------")
    print("The text file transfer_coef.txt has been created. It include the transfer coef based on yours choices.")

### The principal routine

    if choice_1 == "brute":
        if choice_2 == "yes":
            making_output(open_SR_tab("data/"+choice_3bis+"_"+choice_4+".csv"))
        elif choice_2 =="no":
            making_output_2(open_SR_tab("data/"+choice_3bis+"_"+choice_4+".csv"),str_receptors)

    elif choice_1 =="normalized":
        if choice_2 =="yes":
            making_output_3(open_SR_tab("data/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,choice_4,choice_3bis,choice_1bis,first_year,last_year)
        elif choice_2 =="no":
            making_output_4(open_SR_tab("data/"+choice_3bis+"_"+choice_4+".csv"),str_receptors,choice_3bis,choice_4,choice_3bis,choice_1bis,first_year,last_year)
###
elif choice_0 == "no":
    print("Do you want brute SR tables or normalized SR tables ? (brute/normalized)")
    token_1a = 0
    while token_1a ==0:
        choice_1 = input()
        if choice_1 !="brute" and choice_1 !="normalized":
            token_1a=0
            print("Incorrect input, please try again:")
        else:
            token_1a=1
    print("-----------------------------------------------")
    if choice_1 =="normalized":
        print("\n")
        print("\t")
        print("Which method do you want for the normalization ? (average/median)")
        token_1bisa = 0
        while token_1bisa == 0:
            choice_1bis = input()
            if choice_1bis != "average" and choice_1bis != "median":
                token_1bisa = 0
                print("Incorrect input, please try again:")
            else:
                token_1bisa = 1
    else:
        pass
    print("-----------------------------------------------")
    print("\n")
    print("\t")
    if choice_1 =="normalized":
        print("Select the first year between 1995 and 2020:")
        token_4a = 0
        while token_4a == 0:
            first_year = input()
            if int(first_year) <1995 or int(first_year) > 2020 :
                token_4a = 0
                print("Incorrect input, please try again")
            else:
                token_4a = 1
        print("Select the last year between 1995 and 2020: (> first year)")
        token_4a = 0
        while token_4a == 0:
            last_year = input()
            if int(last_year) <1995 or int(last_year) > 2020 or int(last_year) < int(first_year):
                token_4a = 0
                print("Incorrect input, please try again")
            else:
                token_4a = 1
        print("-----------------------------------------------")
        print("\n")
        print("\t")
    print("Do you want all the receptors ? (yes/no)")
    token_2 = 0
    while token_2==0:
        choice_2 = input()
        if choice_2 !="yes" and choice_2 !="no":
            token_2=0
            print("Incorrect input, please try again:")
        else:
            token_2 =1
    if choice_2 == "no":
        print("Select the receptors. Only the Helcom or Ospar receptors")
        print("The format must be: EEZ48,EEZ65,EEZ71,OR1,HE8")
        print("Please enter the zones separated by comma with no blanks:")
        str_receptors = input()
    else:
        pass
    print("-----------------------------------------------")
    print("\n")
    print("Please, select your parameters: dry oxidised nitrogen, wet oxidised nitrogen, dry reduced nitrogen, wet reduced nitrogen ?")
    print("Example: wet oxidised nitrogen")
    print("Please enter without capital letter:")
    token_3 = 0
    while token_3 == 0:
        choice_3 = input()
        if choice_3 != "oxidised nitrogen" and choice_3 != "dry oxidised nitrogen" and choice_3 != "wet oxidised nitrogen" and choice_3 != "reduced nitrogen" and choice_3 != "dry reduced nitrogen" and choice_3 != "wet reduced nitrogen":
            token_3 = 0
            print("Incorrect input, please try again:")
        else:
            #if choice_3 == "oxidised nitrogen":
               # choice_3bis = "oxidised_nitrogen"
            if choice_3 == "dry oxidised nitrogen":
                choice_3bis = "dry_oxidised_nitrogen"
            elif choice_3 == "wet oxidised nitrogen":
                choice_3bis = "wet_oxidised_nitrogen"
            #elif choice_3 == "reduced nitrogen":
                #choice_3bis = "reduced_nitrogen"
            elif choice_3 == "dry reduced nitrogen":
                choice_3bis = "dry_reduced_nitrogen"
            elif choice_3 == "wet reduced nitrogen":
                choice_3bis = "wet_reduced_nitrogen"
            token_3 = 1
    print("-----------------------------------------------")
    print("\n")
    print("Please select a year between 1995 and 2020")
    token_4 = 0
    while token_4 == 0:
        choice_4 = input()
        if int(choice_4) < 1995 or int(choice_4) > 2020 :
            token_4 = 0
            print("Incorrect input, please try again")
        else:
            token_4 = 1
    print("-----------------------------------------------")
    print("The text file output_SR.txt has been created. It include the SR table based on yours choices.")
    print("-----------------------------------------------")
    print("The text file transfer_coef.txt has been created. It include the transfer coef based on yours choices.")

### Principal routine 2
    if choice_1 == "brute":
        if choice_2 == "yes":
            making_output(fusion_open_SR_table("data/data_jurek_helcom/"+choice_3bis+"_"+choice_4+".csv","data/data_jurek_ospar/"+choice_3bis+"_"+choice_4+".csv"))
        elif choice_2 == "no":
            making_output_2(fusion_open_SR_table("data/data_jurek_helcom/"+choice_3bis+"_"+choice_4+".csv","data/data_jurek_ospar/"+choice_3bis+"_"+choice_4+".csv"),str_receptors)
    elif choice_1 == "normalized":
        if choice_2 == "yes":
            making_output_3(fusion_open_SR_table("data/data_jurek_helcom/"+choice_3bis+"_"+choice_4+".csv","data/data_jurek_ospar/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,choice_4,choice_3bis,choice_1bis,first_year,last_year)
        elif choice_2 == "no":
            making_output_4(fusion_open_SR_table("data/data_jurek_helcom/"+choice_3bis+"_"+choice_4+".csv","data/data_jurek_ospar/"+choice_3bis+"_"+choice_4+".csv"),str_receptors,choice_3bis,choice_4,choice_3bis,choice_1bis,first_year,last_year)

#for annee choisie et with les meteorologies choisies