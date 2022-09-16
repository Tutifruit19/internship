#This routine takes the source receptors tables and create a text file that can be used for deposition.py
#Here you can change the names of your source receptor tables ( RDN and OXN )
#You can also change the name of the file that the routine creates
# You can chose if you work with HELCOM or OSPAR receptors 
#Do not forget to change the names of the recptors at the end of the routine

import numpy as np
import csv
#questions for the user
print("-----------------------------------\n")
#years
print("YEARS")
print("Enter the first and the last year :")
print("ex: 1999,2006")
user_years = input()
print("-----------------------------------\n")
#receptors
print("RECEPTORS")
# creating an empty list
user_receptors = []
# number of elements as input
n = int(input("Enter number of receptors you want : "))
# iterating till the range
for i in range(0, n):
    print("Name of the receptor:")
    ele = str(input())
    user_receptors.append(ele) # adding the element
print("-----------------------------------\n")
#asking is OXN is available (right now it isn't for the local fraction method)
print("OXN")
print("Are the OXN source/receptor tables available?")
print("yes/no")
OXN_available = input()
print("-----------------------------------\n")
#name of the file created by routine
print("NAME OF THE FILE")
print("How do you want to call the final file?")
user_file_name = input()



#local fraction tables 
list_years = np.arange(float(user_years[0:4]),float(user_years[5:9])+1)
RDN_files = []
OXN_files = []
for year in list_years:
    RDN_files.append("RDN_" + str(int(year)) + ".txt")
    OXN_files.append("OXN_" + str(int(year)) + ".txt")

def deposition_values(file, receptors):

    """
    Function that mades the sum of all the recieved Nitrogen by a receptor, so we can have the total deposition.

    Inputs : file -> name of the file 
            receptors -> list with all the receptors we want

    Outputs :   year 
                type of pollutant
                list of the total deposition for each receptor

    """
    
    all_dict_str = []
    
    deposition_float = []
    deposition_str = []

    pollutant = file[0:3]
    year = file[4:8]

    #dictionary of the values of N per receptor
    with open(file, "r") as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter = "\t")
        for row in csv_reader:
            if row[0] in receptors : 
                all_dict_str.append(row)
    all_dict_float = [[0 for j in range(len(all_dict_str[0]))] for i in range(len(all_dict_str))]
    
    #replace the missing data per 0
    for i in range(len(all_dict_str)):
        all_dict_str[i].pop(0)
        for sup in range(3):
            all_dict_str[i].pop()
        for j in range(len(all_dict_str[0])):
            if all_dict_str[i][j] == "nan" or all_dict_str[i][j] == ""  : 
                all_dict_str[i][j] = "0" 
            all_dict_float[i][j] = float(all_dict_str[i][j])
        deposition_float.append((sum(all_dict_float[i]))/10)
    for i in range(len(deposition_float)):
        deposition_float[i] = round(deposition_float[i], 4)
        deposition_str.append(str(deposition_float[i]))

        #we want all the str to have the same shape
        if len(deposition_str[i]) != 10 :
            add = ""
            for blanck in range(10 - len(deposition_str[i])):
                add = " " + add
            deposition_str[i] = add + deposition_str[i]       
    return(pollutant, year, deposition_str)

def total_deposition_values(RDN_file, OXN_file, receptors): 
    """
    !!! RDN and OXN do not have the same shape, because of the seas areas
    """

    OXN_dict = []
    RDN_dict = []
    deposition_float = []
    deposition_str = []

    pollutant = OXN_file[0:3]
    year = OXN_file[4:8]
     
    #list of OXN values per receptor
    with open(OXN_file, "r") as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter = "\t")
        for row in csv_reader:
            if row[0] in receptors : 
                OXN_dict.append(row)

    #list of RDN values per receptor
    with open(RDN_file, "r") as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter = "\t")
        for row in csv_reader:
            if row[0] in receptors : 
                RDN_dict.append(row)

    #replace the missing data per 0
    for i in range(len(OXN_dict)):
        OXN_dict[i].pop(0)
        for j in range(len(OXN_dict[0])):
            if OXN_dict[i][j] == "nan" : 
                OXN_dict[i][j] = "0" 
        OXN_dict[i].pop()

    for i in range(len(RDN_dict)):
        RDN_dict[i].pop(0)
        RDN_dict[i].pop()
        RDN_dict[i].insert(3,0)
        RDN_dict[i].insert(14,0)
        for add in range(4):
            RDN_dict[i].insert(len(RDN_dict[0])-1,0)
        for add in range(2): 
            RDN_dict[i].append(0)
            

    TOT_dict = [[0 for j in range(len(RDN_dict[0]))]for i in range(len(RDN_dict))]

    for i in range(len(TOT_dict)):
        for j in range(len(TOT_dict[0])):
            TOT_dict[i][j] = float(OXN_dict[i][j]) + float(RDN_dict[i][j])
        deposition_float.append((sum(TOT_dict[i]))/10)
    for i in range(len(deposition_float)):
        deposition_float[i] = round(deposition_float[i], 4)
        deposition_str.append(str(deposition_float[i]))

        #we want all the str to have the same shape
        if len(deposition_str[i]) != 10 :
            add = ""
            for blanck in range(10 - len(deposition_str[i])):
                add = " " + add
            deposition_str[i] = add + deposition_str[i]

    return(pollutant, year, deposition_str)


#doing an str with the list of receptors
str_receptors = ""
for receptor in user_receptors:
    str_receptors = str_receptors + ";" +  str(receptor) 

#writing the data in a csv file
#oxidised nitrogen
deposition_data = open(user_file_name, "w")
deposition_data.write("\n Oxidised N;\n\nyear" + str_receptors + "\n")
deposition_data.close()
for file in RDN_files :  
    deposition_data = open(user_file_name, "a")
    pollutant, year, deposition = deposition_values(file,user_receptors)
    deposition_data.write(year)
    for i in range(len(user_receptors)):
        if OXN_available == "no" : 
            deposition[i] = "       0.0"
        deposition_data.write(";" + deposition[i])
    deposition_data.write("\n")


#reduceded nitrogen
deposition_data = open(user_file_name, "a")
deposition_data.write("\n Reduced N;\n\nyear" + str_receptors + "\n")
deposition_data.close()
for file in RDN_files :  
    deposition_data = open(user_file_name, "a")
    pollutant, year, deposition = deposition_values(file,user_receptors)
    deposition_data.write(year)
    for i in range(len(user_receptors)):
        deposition_data.write(";" + deposition[i])
    deposition_data.write("\n")
    

# we don't have total nitrogen for local fraction method, because we do not have the OXN : 
#total nitrogen = reduced nitrogen
deposition_data = open(user_file_name, "a")
deposition_data.write("\n Total N;\n\nyear" + str_receptors + "\n")
deposition_data.close()
for file in RDN_files :  
    deposition_data = open(user_file_name, "a")
    pollutant, year, deposition = deposition_values(file,user_receptors)
    deposition_data.write(year)
    for i in range(len(user_receptors)):
        deposition_data.write(";" + deposition[i])
    deposition_data.write("\n")