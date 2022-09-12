import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc 
from scipy import stats
from scipy.stats import linregress
import os

#we are doing deposition, but could work for emission 
em_or_dep = "deposition"

#path of the file 
print("Please enter the name of the deposition file:")
print("---------------------------------------------------")
file = input()
print("---------------------------------------------------")
print("What kind of data is that ?")
print("1 : classic")
print("2 : normalized")
print("---------------------------------------------------")
type = input()

#associate each type of data with an str
if type == "1" : 
    str_type = "classic"
elif type == "2" : 
    str_type = "normalized"

#create new directory
path = os.getcwd()
os.system("mkdir " + str_type + "_" + em_or_dep)

#reading the file and putting it into a list
result = [] 
with open(file,'r') as data:
    for line in csv.reader(data):     
        result.append(line)
new_result = [result[i] for i in range(len(result))]

#statistical significance 
def kendall_tau( years, values ):

    """
    Inputs : name of the emitter
             list of the years we work with
             list of the values for each year

    Outputs : name of the emitter
              statisctical significance 
              agreement or not between years and values (depending of the tau value)
              tau
              p-value
    """

    tau, p_value = stats.kendalltau(years, values)
    tau = round(tau,2)
    str_p_value = str(p_value)
    if "e" in str_p_value:
        index = str_p_value.find("e")
        nombre = str_p_value[0:4]
        puissance = str_p_value[index:index+4]
        result = nombre + puissance
    else : 
        result = str(round(p_value, 3))
    trend = round(((1 - p_value ) * 100),2)
    agreement = ""
    if tau == 1: 
        agreement = "agreement"
    elif tau == -1: 
        agreement = "disagreement"

    elif -0.1 < tau  and tau < 0.1 : 
        agreement = "independence"
    else : 
        agreement = "ø"


    return( result )

#we have 3 types of nitrogen
nox_values = []
nh3_values = []
nox_values_rec_emi = []
nh3_values_rec_emi = []
for k in range(0,3):

    #delete the first line because it is a blanck
    result.pop(0)
    new_result.pop(0)
    
    #first kind of deposition
    title = result[0][0]
    characters1 = ";"
    characters2= " "
    for x in range(len(characters1)):
        title=title.replace(characters1,"")
    for x in range(len(characters2)):
        title=title.replace(characters2,"")

    #delating the title and the other blank
    result.pop(0)
    new_result.pop(0)
    result.pop(0)
    new_result.pop(0)

    #creation of the list of rec_emi/emitters
    str_rec_emi = result[0][0] + ";"
    list_rec_emi = []
    result.pop(0)
    new_result.pop(0)
    characters3 = "year"
    for x in range(len(characters3)):
        str_rec_emi=str_rec_emi.replace(characters3,"")

    start_rec_emi = 0
    for x in range(len(str_rec_emi)):
        if str_rec_emi[x] == ";":
            end_rec_emi = x
            list_rec_emi.append(str_rec_emi[start_rec_emi+1:end_rec_emi])
        start_rec_emi = end_rec_emi
    list_rec_emi.pop(0)


    #creation of the list of years and values
    list_str_values = []
    list_years = []

    if k != 2 : #we have 3 types of deposition, only the last one does not end with ";"
        i = 0
        while result[i]!=[]:
            str_year = result[i][0]
            list_years.append(str_year[0:4])
            str_values = result[i]
            new_result.pop(0)
            list_str_values.append(str_values)
            i+=1
    else : 
        for i in range(len(result)):
            str_year = result[i][0]
            list_years.append(str_year[0:4])
            str_values = result[i]
            new_result.pop(0)
            list_str_values.append(str_values)

    #delating the years of the list - now we only have the values 
    for i in range(len(list_str_values)):
        characters = str(list_years[i])
        characters = characters + ";"
        for j in range(len(list_str_values[0])):
            list_str_values[i][j]=list_str_values[i][j].replace(characters,"")

    #creating a matrix with all the values per receptor and year
    value = []
    tab_value = [] #Table with all the values per year and receptor
    list_values =[] #List of the values of every receptor per year 
    x=0

    for i in range(len(list_str_values)):
        list_str_values[i][0] = list_str_values[i][0] + ";"
        while (len(list_values)<len(list_rec_emi)) :
            if list_str_values[i][0][x] == ";" :
                value.append(list_str_values[i][0][x-10:x-1])
                list_values.append(float(value[0]))
                value = []
                x+=1
            else:
                x+=1
        tab_value.append(list_values)
        list_values = []     
        x=0
    

    result = [new_result[i] for i in range(len(new_result))]

    
    #linear regression
    for i in range(len(list_years)):
        list_years[i]=float(list_years[i])

    def lin_reg(receptor_values):
        """

        Function that returns the y values of the linear regression between the years and the values of the receptor/emitter, the slope, the intercept and the r

        """
        mymodel = []
        slope, intercept, r, p_value, se = stats.linregress(list_years, receptor_values)
        for i in range(len(list_years)):
            mymodel.append(slope*list_years[i]+intercept)

        str_p_value = str(p_value)
        if "e" in str_p_value:
            index = str_p_value.find("e")
            nombre = str_p_value[0:4]
            puissance = str_p_value[index:index+4]
            result = nombre + puissance
        else : 
            result = str(round(p_value, 3))

        return [mymodel, slope, intercept, r, result]

    #classic plots    
    j=0
    os.system("mkdir " +path + "/"+  str_type + "_" + em_or_dep+ "/" + title)
    while j<len(list_rec_emi):
        list_values_rec_emi =[]
        for i in range(len(list_years)):
            list_values_rec_emi.append(tab_value[i][j])
        if title=="OxidisedN":
            plt.plot(list_years,list_values_rec_emi, label=list_rec_emi[j], color = "blue")
            TITLE = "Oxidized N"
        elif title=="ReducedN":
            plt.plot(list_years,list_values_rec_emi, label=list_rec_emi[j], color = "red")
            TITLE = "Reduced N"
        else:
            plt.plot(list_years,list_values_rec_emi, label=list_rec_emi[j], color = "green")
            TITLE = "Total N"
        
        plt.plot(list_years, (lin_reg(list_values_rec_emi))[0],"--" , color = "black",label = "y = "+ str(round(lin_reg(list_values_rec_emi)[1],2)) +"* x + " + str(round(lin_reg(list_values_rec_emi)[2],2))+ "\n" + "R-squared: " + str(round(lin_reg(list_values_rec_emi)[3]**2,2)) + "\n" + "p-value: " + str(lin_reg(list_values_rec_emi)[4]))
        dim=np.arange(list_years[0], list_years[len(list_years)-1],1)
        plt.xticks(dim, rotation  = 60)
        #plt.yticks(np.arange(0,150,50))
        plt.ylabel("Deposition in kt(N)/yr")
        plt.legend(fontsize = 10)
        plt.grid(True, axis = "y")
        plt.title(TITLE,fontsize = 10)
        plt.savefig(path+ "/" + str_type + "_" + em_or_dep+ "/"  +title+"/"+str(int(list_years[0]))+"_"+str(int(list_years[len(list_years)-1]))+"_" +list_rec_emi[j]+".png")
        plt.close()
        j+=1


    #bar plots
    j=0 
    while j<len(list_rec_emi):
        list_values_rec_emi =[]
        for i in range(len(list_years)):
            list_values_rec_emi.append(tab_value[i][j])
        if title=="OxidisedN":
            for i in range(len(list_values_rec_emi)):
                nox_values.append(list_values_rec_emi[i])
            nox_values_rec_emi.append(nox_values)
            nox_values = [] 
        elif title=="ReducedN":
            for i in range(len(list_values_rec_emi)):
                nh3_values.append(list_values_rec_emi[i])
            nh3_values_rec_emi.append(nh3_values)            
            nh3_values = []
        else:
            pass
        
        j+=1 


#bar plots
os.system("mkdir " +path + "/"+  str_type + "_" +em_or_dep + "/bar_plots" )
for i in range(len(list_rec_emi)):       
    #print(nox_values_rec_emi)
    plt.bar(list_years, nox_values_rec_emi[i], label = "Oxidized N", color = "blue") 
    plt.bar(list_years,nh3_values_rec_emi[i], label = "Reduced N", color = "red", bottom = nox_values_rec_emi[i])  
    dim=np.arange(list_years[0], list_years[len(list_years)-1],1)
    plt.xticks(dim, rotation  = 60)
    #plt.yticks(np.arange(0,60,10))
    plt.ylabel("Deposition in kt(N)/yr")
    plt.legend(fontsize = 10)
    plt.grid(True, axis = "y")
    plt.title(list_rec_emi[i], fontsize = 10)
    plt.savefig(path +  "/"+ str_type + "_"+ em_or_dep + "/bar_plots/"+list_rec_emi[i]+"_"+str(int(list_years[0]))+"_"+str(int(list_years[len(list_years)-1]))+".png")
    plt.close()
            
