#This routine takes the source receptors tables and create a text file that can be used for deposition.py
#Here you can change the names of your source receptor tables ( RDN and OXN )
#You can also change the name of the file that the routine creates
# You can chose if you work with HELCOM or OSPAR receptors 
#Do not forget to change the names of the recptors at the end of the routine

import numpy as np
import csv

#local fraction tables 
#local fraction tables 
RDN_files = ["RDN_1995.txt", "RDN_1996.txt", "RDN_1997.txt", "RDN_1998.txt", "RDN_1999.txt", "RDN_2000.txt","RDN_2001.txt", "RDN_2002.txt","RDN_2003.txt","RDN_2004.txt","RDN_2005.txt","RDN_2006.txt","RDN_2007.txt","RDN_2008.txt", "RDN_2009.txt","RDN_2010.txt","RDN_2011.txt","RDN_2012.txt","RDN_2013.txt","RDN_2014.txt","RDN_2016.txt","RDN_2017.txt","RDN_2018.txt","RDN_2019.txt","RDN_2020.txt",]
OXN_files = ["OXN_1995.txt", "OXN_1996.txt", "OXN_1997.txt", "OXN_1998.txt", "OXN_1999.txt", "OXN_2000.txt","OXN_2001.txt", "OXN_2002.txt","OXN_2003.txt","OXN_2004.txt","OXN_2005.txt","OXN_2006.txt","OXN_2007.txt","OXN_2008.txt", "OXN_2009.txt","OXN_2010.txt","OXN_2011.txt","OXN_2012.txt","OXN_2013.txt","OXN_2014.txt","OXN_2016.txt","OXN_2017.txt","OXN_2018.txt","OXN_2019.txt","OXN_2020.txt",]

#HELCOM receptors
#HELCOM = ['HE8','HE5','HE1','HE2','HE3','HE4','HE7','HE6','HE9']

#OSPAR receptors
OSPAR = ["OR1", "OR2", "OR3", "OR4", "OR5", "EEZ100", "EEZ1065", "EEZ1071", "EEZ108", "EEZ109", "EEZ110", "EEZ1100", "EEZ119", "EEZ1213", "EEZ185", "EEZ188", "EEZ189", "EEZ190", "EEZ191", "EEZ2065", "EEZ209", "EEZ2100", "EEZ212", "EEZ213", "EEZ215", "EEZ216", "EEZ2209", "EEZ2213", "EEZ2216", "EEZ224", "EEZ273", "EEZ3108", "EEZ3209", "EEZ3213", "EEZ4091", "EEZ4209", "EEZ4213", "EEZ4273", "EEZ48", "EEZ5065", "EEZ5071", "EEZ5091", "EEZ5100", "EEZ5108", "EEZ5209", "EEZ5213", "EEZ5273", "EEZ65", "EEZ71", "EEZ91", "EEZ99"]

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

    pollutant = file[5:8]
    year = file[0:4]

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

    

#writing the LF data in a csv file
#we don't have oxidized nitrogen for local fraction method : 
#oxidised nitrogen
LF_deposition = open("OSPAR_LF_dep_1995_2020.txt", "w")
LF_deposition.write("\n Oxidised N;\n\nyear;OR1;OR2;OR3;OR4;OR5;EEZ100;EEZ1065;EEZ1071;EEZ108;EEZ109;EEZ110;EEZ1100;EEZ119;EEZ1213;EEZ185;EEZ188;EEZ189;EEZ190;EEZ191;EEZ2065;EEZ209;EEZ2100;EEZ212;EEZ213;EEZ215;EEZ216;EEZ2209;EEZ2213;EEZ2216;EEZ224;EEZ273;EEZ3108;EEZ3209;EEZ3213;EEZ4091;EEZ4209;EEZ4213;EEZ4273;EEZ48;EEZ5065;EEZ5071;EEZ5091;EEZ5100;EEZ5108;EEZ5209;EEZ5213;EEZ5273;EEZ65;EEZ71;EEZ91;EEZ99\n")
LF_deposition.close()
for file in RDN_files :  
    LF_deposition = open("OSPAR_LF_dep_1995_2020.txt", "a")
    pollutant, year, deposition = deposition_values(file,OSPAR)
    deposition = ["       0.0", "       0.0","       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0","       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0","       0.0""       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0","       0.0","       0.0","       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0","       0.0", "       0.0","       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0","       0.0", "       0.0","       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0", "       0.0","       0.0"]
    LF_deposition.write(year + ";" + deposition[0] + ";" + deposition[1] + ";" + deposition[2] + ";" + deposition[3] + ";"  + deposition[4] + ";" + deposition[5] + ";" + deposition[6] + ";" + deposition[7] + ";" + deposition[8] + ";" + deposition[9] + ";" + deposition[10] + ";" + deposition[11] + ";" + deposition[12] + ";"  + deposition[13] + ";" + deposition[14] + ";" + deposition[15] + ";" + deposition[16] + ";" + deposition[17] +";" + deposition[18] + ";" + deposition[19] + ";" + deposition[20] + ";" + deposition[21] + ";"  + deposition[22] + ";" + deposition[23] + ";" + deposition[24] + ";" + deposition[25] + ";" + deposition[26] + ";" + deposition[27] + ";" + deposition[28] + ";" + deposition[29] + ";" + deposition[30] + ";"  + deposition[31] + ";" + deposition[32] + ";" + deposition[33] + ";" + deposition[34] + ";" + deposition[35]+ ";" + deposition[36] + ";" + deposition[37] + ";" + deposition[38] + ";" + deposition[39] + ";"  + deposition[40] + ";" + deposition[41] + ";" + deposition[42] + ";" + deposition[43] + ";" + deposition[44]+ ";" + deposition[45] + ";" + deposition[46] + ";" + deposition[47] + ";"  + deposition[48] + ";" + deposition[49] + ";" + deposition[50] + "\n")


#reduceded nitrogen
LF_deposition = open("OSPAR_LF_dep_1995_2020.txt", "a")
LF_deposition.write("\n Reduced N;\n\nyear;OR1;OR2;OR3;OR4;OR5;EEZ100;EEZ1065;EEZ1071;EEZ108;EEZ109;EEZ110;EEZ1100;EEZ119;EEZ1213;EEZ185;EEZ188;EEZ189;EEZ190;EEZ191;EEZ2065;EEZ209;EEZ2100;EEZ212;EEZ213;EEZ215;EEZ216;EEZ2209;EEZ2213;EEZ2216;EEZ224;EEZ273;EEZ3108;EEZ3209;EEZ3213;EEZ4091;EEZ4209;EEZ4213;EEZ4273;EEZ48;EEZ5065;EEZ5071;EEZ5091;EEZ5100;EEZ5108;EEZ5209;EEZ5213;EEZ5273;EEZ65;EEZ71;EEZ91;EEZ99\n")
LF_deposition.close()
for file in RDN_files :  
    LF_deposition = open("OSPAR_LF_dep_1995_2020.txt", "a")
    pollutant, year, deposition = deposition_values(file,OSPAR)
    LF_deposition.write(year + ";" + deposition[0] + ";" + deposition[1] + ";" + deposition[2] + ";" + deposition[3] + ";"  + deposition[4] + ";" + deposition[5] + ";" + deposition[6] + ";" + deposition[7] + ";" + deposition[8] + ";" + deposition[9] + ";" + deposition[10] + ";" + deposition[11] + ";" + deposition[12] + ";"  + deposition[13] + ";" + deposition[14] + ";" + deposition[15] + ";" + deposition[16] + ";" + deposition[17] +";" + deposition[18] + ";" + deposition[19] + ";" + deposition[20] + ";" + deposition[21] + ";"  + deposition[22] + ";" + deposition[23] + ";" + deposition[24] + ";" + deposition[25] + ";" + deposition[26] + ";" + deposition[27] + ";" + deposition[28] + ";" + deposition[29] + ";" + deposition[30] + ";"  + deposition[31] + ";" + deposition[32] + ";" + deposition[33] + ";" + deposition[34] + ";" + deposition[35]+ ";" + deposition[36] + ";" + deposition[37] + ";" + deposition[38] + ";" + deposition[39] + ";"  + deposition[40] + ";" + deposition[41] + ";" + deposition[42] + ";" + deposition[43] + ";" + deposition[44]+ ";" + deposition[45] + ";" + deposition[46] + ";" + deposition[47] + ";"  + deposition[48] + ";" + deposition[49] + ";" + deposition[50] +"\n")

# we don't have total nitrogen for local fraction method, because we do not have the OXN : 
#total nitrogen = reduced nitrogen
LF_deposition = open("OSPAR_LF_dep_1995_2020.txt", "a")
LF_deposition.write("\n Total N;\n\nyear;OR1;OR2;OR3;OR4;OR5;EEZ100;EEZ1065;EEZ1071;EEZ108;EEZ109;EEZ110;EEZ1100;EEZ119;EEZ1213;EEZ185;EEZ188;EEZ189;EEZ190;EEZ191;EEZ2065;EEZ209;EEZ2100;EEZ212;EEZ213;EEZ215;EEZ216;EEZ2209;EEZ2213;EEZ2216;EEZ224;EEZ273;EEZ3108;EEZ3209;EEZ3213;EEZ4091;EEZ4209;EEZ4213;EEZ4273;EEZ48;EEZ5065;EEZ5071;EEZ5091;EEZ5100;EEZ5108;EEZ5209;EEZ5213;EEZ5273;EEZ65;EEZ71;EEZ91;EEZ99\n")
LF_deposition.close()
for file in RDN_files :  
    LF_deposition = open("OSPAR_LF_dep_1995_2020.txt", "a")
    pollutant, year, deposition = deposition_values(file,OSPAR)
    LF_deposition.write(year + ";" + deposition[0] + ";" + deposition[1] + ";" + deposition[2] + ";" + deposition[3] + ";"  + deposition[4] + ";" + deposition[5] + ";" + deposition[6] + ";" + deposition[7] + ";" + deposition[8] + ";" + deposition[9] + ";" + deposition[10] + ";" + deposition[11] + ";" + deposition[12] + ";"  + deposition[13] + ";" + deposition[14] + ";" + deposition[15] + ";" + deposition[16] + ";" + deposition[17] +";" + deposition[18] + ";" + deposition[19] + ";" + deposition[20] + ";" + deposition[21] + ";"  + deposition[22] + ";" + deposition[23] + ";" + deposition[24] + ";" + deposition[25] + ";" + deposition[26] + ";" + deposition[27] + ";" + deposition[28] + ";" + deposition[29] + ";" + deposition[30] + ";"  + deposition[31] + ";" + deposition[32] + ";" + deposition[33] + ";" + deposition[34] + ";" + deposition[35]+ ";" + deposition[36] + ";" + deposition[37] + ";" + deposition[38] + ";" + deposition[39] + ";"  + deposition[40] + ";" + deposition[41] + ";" + deposition[42] + ";" + deposition[43] + ";" + deposition[44]+ ";" + deposition[45] + ";" + deposition[46] + ";" + deposition[47] + ";"  + deposition[48] + ";" + deposition[49] + ";" + deposition[50] +"\n")
