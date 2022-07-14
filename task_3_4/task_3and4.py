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

def making_output_3(tab,choice_3bis,choice_4,type_pol,method):
    name_list_emitters = tab[0]
    name_list_receptors = tab[1]
    result = normalization(open_SR_tab("/home/aurelienh/task_3and4/data/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,method)
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

def normalization(tab,type_pol,method="average"):
    emi_reduced_nitrogen_2016 = []
    emi_reduced_nitrogen_2017 = []
    emi_reduced_nitrogen_2018 = []
    emi_reduced_nitrogen_2019 = []
    emi_reduced_nitrogen_2020 = []
    emi_oxidised_nitrogen_2016 = []
    emi_oxidised_nitrogen_2017 = []
    emi_oxidised_nitrogen_2018 = []
    emi_oxidised_nitrogen_2019 = []
    emi_oxidised_nitrogen_2020 = []
    tab_reduced_nitrogen_2016 = open_SR_tab("data/reduced_nitrogen_2016.csv")
    for i in range(1,np.shape(tab_reduced_nitrogen_2016[2])[1]):
        if tab_reduced_nitrogen_2016[2][-1][i] == "":
            emi_reduced_nitrogen_2016.append(0.0)
        else:
            emi_reduced_nitrogen_2016.append(float(tab_reduced_nitrogen_2016[2][-1][i]))
    tab_reduced_nitrogen_2017 = open_SR_tab("data/reduced_nitrogen_2017.csv")
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
            emi_oxidised_nitrogen_2020.append(float(tab_oxidised_nitrogen_2020[2][-1][i]))

    SR_tab_2016 = open_SR_tab("data/"+type_pol+"_2016.csv")
    result_2016 = convert(SR_tab_2016[2])
    SR_tab_2017 = open_SR_tab("data/"+type_pol+"_2017.csv")
    result_2017 = convert(SR_tab_2017[2])
    SR_tab_2018 = open_SR_tab("data/"+type_pol+"_2018.csv")
    result_2018 = convert(SR_tab_2018[2])
    SR_tab_2019 = open_SR_tab("data/"+type_pol+"_2019.csv")
    result_2019 = convert(SR_tab_2019[2])
    SR_tab_2020 = open_SR_tab("data/"+type_pol+"_2020.csv")
    result_2020 = convert(SR_tab_2020[2])

    tc_2016 = np.zeros((np.shape(result_2016)))
    tc_2017 = np.zeros((np.shape(result_2017)))
    tc_2018 = np.zeros((np.shape(result_2018)))
    tc_2019 = np.zeros((np.shape(result_2019)))
    tc_2020 = np.zeros((np.shape(result_2020)))
    if type_pol == "oxidised_nitrogen" or type_pol == "dry_oxidised_nitrogen" or type_pol == "wet_oxidised_nitrogen":
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
                    tc_2020[i][j] = float("nan")

    name_list_emitters = tab[0]
    name_list_receptors_all = tab[1]
    result = convert(tab[2])
    normalized_2016 = np.zeros((np.shape(result)))
    normalized_2017 = np.zeros((np.shape(result)))
    normalized_2018 = np.zeros((np.shape(result)))
    normalized_2019 = np.zeros((np.shape(result)))
    normalized_2020 = np.zeros((np.shape(result)))
    for i in range(np.shape(normalized_2016)[0]):
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
            normalized_2020[i][j] = tc_2020[i][j]*result[i][j]

    normalized_table = np.zeros((np.shape(normalized_2020)))
    if method =="average":
        for i in range(np.shape(normalized_table)[0]):
            for j in range(np.shape(normalized_table)[1]):
                normalized_table[i][j]= (normalized_2016[i][j]+normalized_2017[i][j]+normalized_2018[i][j]+normalized_2019[i][j]+normalized_2020[i][j])/5
    elif method =="median":
        for i in range(np.shape(normalized_table)[0]):
            for j in range(np.shape(normalized_table)[1]):
                normalized_table[i][j] = sc.median([normalized_2016[i][j],normalized_2017[i][j],normalized_2018[i][j],normalized_2019[i][j],normalized_2020[i][j]])

    return normalized_table

#print(normalization(open_SR_tab("/home/aurelienh/task_3and4/data/dry_oxidised_nitrogen_2018.csv"),"oxidised_nitrogen","average"))



### All Selection before to run the the routine
print("-----------------------------------------------")
print("\n")
print("\n")
print("This routine creates SR tables between 2016 and 2020. You can choose receptors that you want and if you want normalized SR tables (the normalization is made with 2016-2020 meteorology)")
print("\n")
print("\n")
print("-----------------------------------------------")
print("\n")
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

### The principal routine

if choice_1 == "brute":
    if choice_2 == "yes":
        making_output(open_SR_tab("/home/aurelienh/task_3and4/data/"+choice_3bis+"_"+choice_4+".csv"))
    elif choice_2 =="no":
        making_output_2(open_SR_tab("/home/aurelienh/task_3and4/data/"+choice_3bis+"_"+choice_4+".csv"),str_receptors)

elif choice_1 =="normalized":
    if choice_2 =="yes":
        making_output_3(open_SR_tab("/home/aurelienh/task_3and4/data/"+choice_3bis+"_"+choice_4+".csv"),choice_3bis,choice_4,choice_3bis,choice_1bis)
    elif choice_2 =="no":
        pass


