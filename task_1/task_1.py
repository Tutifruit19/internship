### import
import os
import numpy as np

def tri(name_list):
    """
    Organization of the output text file
    """
    number_list = []
    index_list = []
    for i in range(len(name_list)):
        if name_list[i][:4]=="EEZ0":
            number_list.append(int(name_list[i][4:]))
        elif name_list[i][:2]=="EE":
            number_list.append(int(name_list[i][3:]))
        else:
            pass
    old_number_list = [number_list[i] for i in range(len(number_list))]
    number_list.sort()
    for i in range(len(number_list)):
        index_list.append(old_number_list.index(number_list[i]))
    return [index_list,number_list]


os.system("mkdir temp")#create temporary files
path_grid = "/home/estellec/task_1/emep_ll_gridfraction_01degCEIP_2018_helcom_ospar_oaa_eez_2022.nc" #the path of the emep grid
os.system("cp /home/aurelienh/task_1/nc2CountryAll_module/nc2CountryAllocation_4digits nc2CountryAllocation_4digits") #temporary file

print("---------------------------------")
print("\n")
print("Please before executing the program, charge the following module: module load emep")
#print("\n")
#print("You must have the following file in the same place as this program: emep_ll_gridfraction_01degCEIP_2018_ospar2020_eez.nc")
print("\n")
print("---------------------------------")
print("\n")

### definition of the parameters (input)
token = 0 #to be sure that the number entered is an integer
while token ==0: #selection of the start and the end
    print("Please enter the first year of the simulation: ")
    first_year = input()
    print("Please enter the last year of the simulation: ")
    last_year =input()
    if type(int(first_year)) == int and type(int(last_year)) == int:
        token = 1


#the 4 model output parameters
list_parameters = ["DDEP_OXN_m2Grid","WDEP_OXN","DDEP_RDN_m2Grid","WDEP_RDN"]

#selection of the receptors zones
print("Selection of the receptors")
print("------------------------------")
print("Do you need all the OSPAR receptors ? (yes/no)")
answer_1 = input()


### execution of the nc2CountryAllocation routine for all the year and catch the result in different txt file in the directory temp, when all the zones are selected
if answer_1 == "yes":
    l=0
    for k in range(len(list_parameters)):#indicates the charging of the program to the user
        for i in range(int(first_year),int(last_year)+1):
            l=l+1
            os.system("./nc2CountryAllocation_4digits -A "+path_grid+" -i /lustre/storeB/project/fou/kl/emep/ModelRuns/HELCOM/latest_TREND_results/"+str(i)+"/Base_fullrun.nc -p "+list_parameters[k]+" -C EEZ48,EEZ65,EEZ71,EEZ91,EEZ99,EEZ100,EEZ108,EEZ109,EEZ110,EEZ119,EEZ123,EEZ185,EEZ187,EEZ188,EEZ189,EEZ190,EEZ191,EEZ209,EEZ212,EEZ213,EEZ215,EEZ216,EEZ224,EEZ273,OR1,OR2,OR3,OR4,OR5,OAA_CFR,OAA_CCTI,OAA_ATL,OAA_SHPM,OAA_CNOR1,OAA_CNOR2,OAA_CNOR3,OAA_DB,OAA_KD,OAA_NT,OAA_SNS,OAA_GBC,OAA_ADPM,OAA_GBSW,OAA_SPM,OAA_GDPM,OAA_CUKC,OAA_CWMTI,OAA_SCHPM1,OAA_ELPM,OAA_SCHPM2,OAA_MPM,OAA_RHPM,OAA_EMPM,OAA_THPM,OAA_HPM,OAA_ECPM1,OAA_ECPM2,OAA_IS2,OAA_CO,OAA_ENS,OAA_CWCC,OAA_OWCO,OAA_OWAO,OAA_IWCI,OAA_OWBO,OAA_ASS,OAA_CIRL,OAA_CUK1,OAA_IS1,OAA_IRS,OAA_KC,OAA_NNS,OAA_CWM,OAA_LBPM,OAA_SK,OAA_SS,OAA_CWBC,OAA_IWBI,OAA_CWAC,OAA_IWAI,OAA_LPM,OAA_GBCW,OAA_NAAP2,OAA_NAAO1,OAA_NAAPF,OAA_NAAC3,OAA_NAAC2,OAA_NAAC1A,OAA_NAAC1B,OAA_NAAC1C,OAA_NAAC1D,OAA_SAAP2,OAA_SAAOC,OAA_SAAP1,OAA_SAAC1,OAA_SAAC2>temp/result"+str(i)+"_"+list_parameters[k]+".txt") #nc2CountryAllocation command
            print("Charging..............................."+str(round((l/(4*(int(last_year)-int(first_year)+1)))*100,2))+"%") #indicates the charging of the program to the user

### execution of the nc2CountryAllocation routine for all the year and catch the result in different txt file in the directory temp, when the user selects the zones
elif answer_1 == "no":
    print("----------------------")
    print("Select zones: EEZ48,EEZ65,EEZ71,EEZ91,EEZ99,EEZ100,EEZ108,EEZ109,EEZ110,EEZ119,EEZ123,EEZ185,EEZ187,EEZ188,EEZ189,EEZ190,EEZ191,EEZ209,EEZ212,EEZ213,EEZ215,EEZ216,EEZ224,EEZ273,OR1,OR2,OR3,OR4,OR5,OAA_CFR,OAA_CCTI,OAA_ATL,OAA_SHPM,OAA_CNOR1,OAA_CNOR2,OAA_CNOR3,OAA_DB,OAA_KD,OAA_NT,OAA_SNS,OAA_GBC,OAA_ADPM,OAA_GBSW,OAA_SPM,OAA_GDPM,OAA_CUKC,OAA_CWMTI,OAA_SCHPM1,OAA_ELPM,OAA_SCHPM2,OAA_MPM,OAA_RHPM,OAA_EMPM,OAA_THPM,OAA_HPM,OAA_ECPM1,OAA_ECPM2,OAA_IS2,OAA_CO,OAA_ENS,OAA_CWCC,OAA_OWCO,OAA_OWAO,OAA_IWCI,OAA_OWBO,OAA_ASS,OAA_CIRL,OAA_CUK1,OAA_IS1,OAA_IRS,OAA_KC,OAA_NNS,OAA_CWM,OAA_LBPM,OAA_SK,OAA_SS,OAA_CWBC,OAA_IWBI,OAA_CWAC,OAA_IWAI,OAA_LPM,OAA_GBCW,OAA_NAAP2,OAA_NAAO1,OAA_NAAPF,OAA_NAAC3,OAA_NAAC2,OAA_NAAC1A,OAA_NAAC1B,OAA_NAAC1C,OAA_NAAC1D,OAA_SAAP2,OAA_SAAOC,OAA_SAAP1,OAA_SAAC1,OAA_SAAC2")
    print("----------------------")
    print("The format must be: EEZ48,EEZ65,EEZ71")
    print("Please enter the zones separated by comma with no blanks:")
    str_filename =input() #name of the receptors selected
    l=0
    for k in range(len(list_parameters)):
        for i in range(int(first_year),int(last_year)+1):
            l=l+1 #indicates the charging of the program to the user
            os.system("./nc2CountryAllocation_4digits -A "+path_grid+" -i /lustre/storeB/project/fou/kl/emep/ModelRuns/HELCOM/latest_TREND_results/"+str(i)+"/Base_fullrun.nc -p "+list_parameters[k]+" -C "+str_filename+">temp/result"+str(i)+"_"+list_parameters[k]+".txt") #nc2CountryAllocation command
            print("Charging..............................."+str(round((l/(4*(int(last_year)-int(first_year)+1)))*100,2))+"%") #indicates the charging of the program to the user



### creation of tables with the diffrent results
tab_DDEP_OXN_m2Grid=[]
for i in range(int(first_year),int(last_year)+1):
    var = np.genfromtxt("temp/result"+str(i)+"_DDEP_OXN_m2Grid"+".txt",dtype=str)
    tab_DDEP_OXN_m2Grid.append(var) #the results for DDEP_OXN_m2Grid are put in an array

tab_WDEP_OXN=[]
for i in range(int(first_year),int(last_year)+1):
    var = np.genfromtxt("temp/result"+str(i)+"_WDEP_OXN"+".txt",dtype=str)
    tab_WDEP_OXN.append(var) #the results for WDEP_OXN are put in an array


tab_DDEP_RDN_m2Grid=[]
for i in range(int(first_year),int(last_year)+1):
    var = np.genfromtxt("temp/result"+str(i)+"_DDEP_RDN_m2Grid.txt",dtype=str)
    tab_DDEP_RDN_m2Grid.append(var) #the results for DDEP_RDN_m2Grid are put in an array


tab_WDEP_RDN=[]
for i in range(int(first_year),int(last_year)+1):
    var = np.genfromtxt("temp/result"+str(i)+"_WDEP_RDN.txt",dtype=str)
    tab_WDEP_RDN.append(var) #the results for WDEP_RDN are put in an array


tab=[tab_DDEP_OXN_m2Grid,tab_WDEP_OXN,tab_DDEP_RDN_m2Grid,tab_WDEP_RDN] #all the results are now in the same list



### creation of the output txt file
#creation of an empty text file
file = open("result.txt","w")

file.write("----------Receptor tables----------") #title
file.write("\n")
file.write("\n")

name_region = [] #list of the receptors
list_years = list(range(int(first_year),int(last_year)+1)) #list of the years

#creation of the output text file
if len(np.shape(tab))==4:
    for j in range(np.shape(tab)[2]):
        if len(tab[0][0][j][0])==5 and tab[0][0][j][0][0] =="E":
            name_region.append(tab[0][0][j][0][:3]+"0"+tab[0][0][j][0][3:])
        elif tab[0][0][j][0][:3]=="OAA":
            name_region.append(tab[0][0][j][0][4:])
        else:
            name_region.append(tab[0][0][j][0])
elif len(np.shape(tab))==3:
    name_region.append(tab[0][0][0])
for k in range(len(list_parameters)):
    file.write("\n")
    file.write(list_parameters[k]) #subtitle
    file.write("\n")
    file.write("\n")
    file = open("result.txt","a")
    file.write("      ")
    print(np.shape(tab)[2])
    for i in range(np.shape(tab)[2]):
        print(i)
        if i<len(tri(name_region)[0]):#Organization of the output text file
            file.write(name_region[tri(name_region)[0][i]]+ "  ")#Organization of the output text file
        else:
            file.write(name_region[i]+ "  ")#Organization of the output text file

    file.write("\n")

    if len(np.shape(tab))==4:
        for i in range(np.shape(tab)[1]):
            file.write(str(list_years[i])+"  ")
            for j in range(np.shape(tab)[2]):
                if j<len(tri(name_region)[0]):#Organization of the output text file
                    file.write(tab[k][i][tri(name_region)[0][j]][1]+"  ")#Organization of the output text file
                else:
                    file.write(tab[k][i][j][1]+"  ")#Organization of the output text file
            file.write("\n")
    elif len(np.shape(tab))==3:
        for i in range(np.shape(tab)[1]):
            file.write(str(list_years[i])+"  ")
            file.write(tab[k][i][1]+"  ")
            file.write("\n")
    file.write("-------------------------------------------------------------------------------------------------------------------------------")
    file.write("\n")

#os.system("rm -r temp")#remove temporary files
os.system("rm nc2CountryAllocation_4digits")#remove temporary files






