"This routine gives us some plots, where we can find the top ten contributors for each HELCOM receptor"

#imports 
from audioop import reverse
from tkinter import Menu
import numpy as np
from cgitb import reset
import csv 
import statistics as stat
import matplotlib.pyplot as plt
import os

#contribution file 
file = "contributions_actual_9_1995_2020.txt"

#directory for each pollutant
os.system("mkdir OXN_top_ten")
os.system("mkdir RDN_top_ten")
os.system("mkdir TOT_top_ten")

#directory for the plots with the mean btw 1995 and 2020
os.system("mkdir OXN_top_ten/mean_1995_2020")
os.system("mkdir RDN_top_ten/mean_1995_2020")
os.system("mkdir TOT_top_ten/mean_1995_2020")
path = os.getcwd()

#list of all the years 
list_years = list(range(1995,2021))

#creating a directory for each year in each pollutant
for year in list_years:
    os.system("mkdir OXN_top_ten/" + str(year))
    os.system("mkdir RDN_top_ten/" + str(year))
    os.system("mkdir TOT_top_ten/" + str(year))
    

#reading the file and putting it into a list
result = []
with open(file,'r') as data:
    for line in csv.reader(data):        
        result.append(line)
new_result = [result[i] for i in range(len(result))]

# 4 types of nitrogen 
pollutants = [" OXN dry deposition",  "OXN wet deposition", " RDN dry deposition",  "RDN wet deposition"]
dry_deposition = []
wet_deposition = []

#for pollutant in pollutants:
#delate the first line: it is the name of the pollutant
result.pop(0)
new_result.pop(0)

#list of the receptors
receptors = ["ARC            ", " BAP            ", " BOB            ", " BOS            ", " GUF            ", " GUR            ", " KAT            ", " SOU            ", " WEB            "]


list_values_receptor = []

#for receptor in (receptors):

result.pop(0)

i = 0 
blanks_year = "      year"
list_contributors = []
list_values_contributors = []
list_values_contributor = []

#function that gives the long names of the emitters 
def long_name(emitter):

    """
    Input : name of the emitter 
    Output: long name of the emitter
    """
    longname = ""
    if (emitter =='AL') :
        longname='Albania'
    
    elif (emitter =='AM') :
        longname='Armenia'
        
    elif (emitter =='AST') :
        longname='Asian_areas'
        

    elif (emitter =='AT') :
        longname='Austria'
        
    elif (emitter =='ATL') :
        longname='North-East_Atlantic_Ocean'
        

    elif (emitter =='AZ') :
        longname='Azerbaijan'
        
    elif (emitter =='BA') :
        longname='Bosnia_and_Herzegovina'
        
    elif (emitter =='BAS') :
        longname='Baltic_Sea'
        

    elif (emitter =='BE') :
        longname='Belgium'
        
    elif (emitter =='BG') :
        longname='Bulgaria'
        
    elif (emitter =='BLS') :
        longname='Black_Sea'
        

    elif (emitter =='BY') :
        longname='Belarus'
        
    elif (emitter =='CH') :
        longname='Switzerland'
        

    elif (emitter =='CY') :
        longname='Cyprus'
        

    elif (emitter =='CZ') :
        longname='Czechia'
        

    elif (emitter =='DE') :
        longname='Germany'
        

    elif (emitter =='DK') :
        longname='Denmark'
        

    elif (emitter =='EE') :
        longname='Estonia'
        

    elif (emitter =='ES') :
        longname='Spain'
        

    elif (emitter =='FI') :
        longname='Finland'
        

    elif (emitter =='FR') :
        longname='France'
        

    elif (emitter =='GB') :
        longname='United_Kingdom'
        

    elif (emitter =='GE') :
        longname='Georgia'
        

    elif (emitter =='GR') :
        longname='Greece'
        

    elif (emitter =='HR') :
        longname='Croatia'
        
    elif (emitter =='HU') :
        longname='Hungary'
        

    elif (emitter =='IE') :
        longname='Ireland'
        

    elif (emitter =='IS') :
        longname='Iceland'
        

    elif (emitter =='IT') :
        longname='Italy'
        

    elif (emitter =='KG') :
        longname='Kyrgyzstan'
        

    elif (emitter =='KZ') :
        longname='Kazakhstan'
        

    elif (emitter =='LI') :
        longname='Liechtenstein'
        

    elif (emitter =='LT') :
        longname='Lithuania'
        

    elif (emitter =='LU') :
        longname='Luxembourg'
        

    elif (emitter =='LV') :
        longname='Latvia'
        

    elif (emitter =='MC') :
        longname='Monaco'
        

    elif (emitter =='MD') :
        longname='Moldova'
        

    elif (emitter =='ME') :
        longname='Montenegro'
        

    elif (emitter =='MED') :
        longname='Mediterranean_Sea'
        

    elif (emitter =='MK') :
        longname='North_Macedonia'
        

    elif (emitter =='MT') :
        longname='Malta'
        

    elif (emitter =='NL') :
        longname='Netherlands'
        

    elif (emitter =='NO') :
        longname='Norway'
        

    elif (emitter =='NOA') :
        longname='North_Africa'
        

    elif (emitter =='NOS') :
        longname='North_Sea'
        

    elif (emitter =='PL') :
        longname='Poland'
        

    elif (emitter =='PT') :
        longname='Portugal'
        

    elif (emitter =='RO') :
        longname='Romania'
        

    elif (emitter =='RS') :
        longname='Serbia'
        

    elif (emitter =='RU') :
        longname='Russian_Federation'
        

    elif (emitter =='SE') :
        longname='Sweden'
        

    elif (emitter =='SI') :
        longname='Slovenia'
        

    elif (emitter =='SK') :
        longname='Slovakia'
        

    elif (emitter =='TJ') :
        longname='Tajikistan'
        

    elif (emitter =='TM') :
        longname='Turkmenistan'
        

    elif (emitter =='TR') :
        longname='Turkey'
        

    elif (emitter =='UA') :
        longname='Ukraine'
        

    elif (emitter =='UZ') :
        longname='Uzbekistan'

    else: 
        pass
    return(longname)

#making the list of all the contributors
list_contributors = ["AT","BA","BE","BG","BY","CH","CZ","DE","DK","EE","ES","FI","FR","GB","GR","HR","HU","IE","IT","LT","LU","LV","MD","NL","NO","PL","RO","RS","RU","SE","SI","SK","TR","UA","ATL","BAS","BLS","MED","NOS","BIC"]

#creating a list with all the values per receptor 
for i in range(len(result)):
    if (result[i][0]).strip() != "ARC" and result[i][0].strip() != "BAP"and result[i][0].strip() != "BOB"and result[i][0].strip() != "BOS"and result[i][0].strip() != "GUF"and result[i][0].strip() != "GUR"and result[i][0].strip() != "KAT"and result[i][0].strip() != "SOU"and result[i][0].strip() != "WEB" and result[i][0]!= '      year       AT       BA       BE       BY       CH       CZ       DE       DK       EE       ES       FI       FR       GB       HR       HU       IE       IT       LT       LV       MD       NL       NO       PL       RO       RS       RU       SE       SI       SK       TR       UA' and result[i][0] != '      year       AT       BA       BE       BG       BY       CH       CZ       DE       DK       EE       ES       FI       FR       GB       GR       HR       HU       IE       IT       LT       LU       LV       MD       NL       NO       PL       RO       RS       RU       SE       SI       SK       TR       UA      ATL      BAS      BLS      MED      NOS      BIC' and result[i][0].strip() != "RDN wet deposition" and result[i][0].strip() != "RDN dry deposition" and result[i][0].strip() != "OXN wet deposition":
        list_values_receptor.append(result[i][0])

#creating a list with all the values per receptor per contributor
i = 0 
while i < len(list_values_receptor):
    for j in range(len(list_years)):
        list_values_contributor.append(list_values_receptor[i+j])        
    list_values_contributors.append(list_values_contributor)
    list_values_contributor = []
    i += len(list_years)

#putting the values in the list of the type of pollutant that corresponds
old_dry_OXN = [value for value in list_values_contributors[0:9]]
old_wet_OXN = [value for value in list_values_contributors[9:18]]
old_dry_RDN = [value for value in list_values_contributors[18:27]]
old_wet_RDN = [value for value in list_values_contributors[27:36]]

count =  0 #to be sure everything is made for every contributor

#empty lists to be completeted for each pollutant  
dry_OXN = []
dry_OXN_values = []
dry_OXN_values_receptors = []

wet_OXN = []
wet_OXN_values = []
wet_OXN_values_receptors = []

dry_RDN = []
dry_RDN_values = []
dry_RDN_values_receptors = []

wet_RDN = []
wet_RDN_values = []
wet_RDN_values_receptors = []

#creating lists of receptor values for each pollutant
for i in range(len(old_dry_OXN)):
    for j in range(len(old_dry_OXN[0])):
        for year in list_years:
            old_dry_OXN[i][j] = old_dry_OXN[i][j].replace("        " + str(year) + "  ","" )
            old_wet_OXN[i][j] = old_wet_OXN[i][j].replace("        " + str(year) + "  ","" )
            old_dry_RDN[i][j] = old_dry_RDN[i][j].replace("        " + str(year) + "  ","" )
            old_wet_RDN[i][j] = old_wet_RDN[i][j].replace("        " + str(year) + "  ","" )

        for x in range(0,len(old_dry_OXN[0][0]),17):
            dry_OXN_values.append(old_dry_OXN[i][j][0+x:17+x].strip())  
            wet_OXN_values.append(old_wet_OXN[i][j][0+x:17+x].strip())  
            dry_RDN_values.append(old_dry_RDN[i][j][0+x:17+x].strip())  
            wet_RDN_values.append(old_wet_RDN[i][j][0+x:17+x].strip())  

        dry_OXN_values_receptors.append(dry_OXN_values)
        dry_OXN_values = []
        wet_OXN_values_receptors.append(wet_OXN_values)
        wet_OXN_values = []
        dry_RDN_values_receptors.append(dry_RDN_values)
        dry_RDN_values = []
        wet_RDN_values_receptors.append(wet_RDN_values)
        wet_RDN_values = []

#creating lists for every value of contributant to a receptor, for each pollutant
for i in range(len(receptors)):
    dry_OXN.append(dry_OXN_values_receptors[count:len(list_years)+count])
    wet_OXN.append(wet_OXN_values_receptors[count:len(list_years)+count])
    dry_RDN.append(dry_RDN_values_receptors[count:len(list_years)+count])
    wet_RDN.append(wet_RDN_values_receptors[count:len(list_years)+count])
    count+= len(list_years)

for i in range(len(dry_RDN)):
    for j in range(len(dry_RDN[0])):
        for delate in range(0,9):
            dry_RDN[i][j].pop(len(dry_RDN[i][j])-1)
            wet_RDN[i][j].pop(len(wet_RDN[i][j])-1)

#creating empty tables to put the total OXN and RDN 
OXN = [[[0 for k in range(len(list_contributors))] for j in range(len(list_years))] for i in range(len(receptors))]
RDN = [[[0 for k in range(len(list_contributors)-9)] for j in range(len(list_years))] for i in range(len(receptors))]
TOT = [[[0 for k in range(len(list_contributors))] for j in range(len(list_years))] for i in range(len(receptors))]

#OXN = wet_OXN + dry_OXN
for i in range(len(dry_OXN)):
    for j in range(len(dry_OXN[0])):
        for k in range(len(dry_OXN[0][0])):         
            OXN[i][j][k] = float(dry_OXN[i][j][k]) + float(wet_OXN[i][j][k])

#RDN = wet_RDN + dry_RDN
for i in range(len(dry_RDN)):
    for j in range(len(dry_RDN[0])):
        for k in range(len(dry_RDN[0][0])):
            RDN[i][j][k] = float(dry_RDN[i][j][k]) + float(wet_RDN[i][j][k])
        RDN[i][j].insert(3,0)
        RDN[i][j].insert(14,0)
        RDN[i][j].insert(20,0)
        for add in range(6):
            RDN[i][j].append(0)

#TOT = OXN + RDN
for i in range(len(TOT)):
    for j in range(len(TOT[0])):
        for k in range(len(TOT[0][0])):
            TOT[i][j][k] = float(OXN[i][j][k]) + float(RDN[i][j][k])

##for each pollutant :
pollutants = [OXN, RDN, TOT] 


for pollutant in pollutants: 
    #need to make the mean for every contributant
    mean = []
    dict_mean_receptors = {}
    values_for_mean = []

    #classic list and dict
    dict_contributors = {}
    pollutant_contribution = []
    all_contributions = []

    for i in range(len(pollutant)): #receptor
        k = 0 
        #mean values list and dict
        dict_mean_receptors = {}
        values_for_mean = []

        contribution_for_receptor = []

        #we need to go trought every value per year of each contributor to make the mean of the contribution of every contributor 
        while k < len(pollutant[0][0]): 
            for j in range(len(pollutant[0])):
                values_for_mean.append(pollutant[i][j][k]) 
                dict_mean_receptors[""+list_contributors[k]+""] = stat.mean(values_for_mean)
            k += 1 
        mean.append(dict_mean_receptors)

        #to make the plots per year we need to go trought every value of each year
        for j in range(len(pollutant[0])): #year
            
            for k in range(len(pollutant[0][0])): #value per contributor
                dict_contributors[""+list_contributors[k]+""] = pollutant[i][j][k]
            contribution_for_receptor.append(dict_contributors)
            dict_contributors = {}

        pollutant_contribution.append(contribution_for_receptor)      

    #list of the top ten mean contributions for each receptor 
    top_ten_mean = []
    for i in range(len(receptors)):
        top_ten_mean_receptor = []
        for top_10 in range(10):
            max_value_mean, max_contributor_mean = max(zip(mean[i].values(),mean[i].keys()))
            top_ten_mean_receptor.append(max(zip(mean[i].values(),mean[i].keys())))
            del mean[i]["" + max_contributor_mean + ""]  
        top_ten_mean.append(top_ten_mean_receptor)

    #list of the top ten year contributions for each receptor
    top_ten = []
    for i in range(len(pollutant_contribution)):
        top_ten_year_receptor = []
        for j in range(len(pollutant_contribution[0])):
            top_ten_year = []
            for top_10 in range(10):
                max_value, max_contributor = max(zip(pollutant_contribution[i][j].values(),pollutant_contribution[i][j].keys()))
                top_ten_year.append(max(zip(pollutant_contribution[i][j].values(),pollutant_contribution[i][j].keys())))
                del pollutant_contribution[i][j]["" + max_contributor + ""]   
            top_ten_year_receptor.append(top_ten_year)
        top_ten.append(top_ten_year_receptor)


    #mean plots 
    """for receptor in range(len(top_ten_mean)):
        top_ten_mean_contributors = []
        top_ten_mean_values = []
        for top in range(len(top_ten_mean[0])):
            top_ten_mean_contributors.append(long_name(top_ten_mean[receptor][top][1])) 
            top_ten_mean_values.append(top_ten_mean[receptor][top][0])
            
        if pollutant == OXN :
            plt.bar(top_ten_mean_contributors,top_ten_mean_values, color = "blue")
            plt.gcf().subplots_adjust(bottom=0.20)
            plt.xticks(top_ten_mean_contributors, rotation  = 37, fontsize = 9)
            plt.ylabel("kt(N)/yr")
            plt.grid(True, axis = "y")
            plt.title("Top ten oxidized nitogen contributors for " + receptors[receptor]) 
            plt.savefig(path + "/OXN_top_ten/mean_1995_2020/"+receptors[receptor].strip())

        elif pollutant == TOT : 
            plt.bar(top_ten_mean_contributors,top_ten_mean_values, color = "green")
            plt.gcf().subplots_adjust(bottom=0.20)
            plt.xticks(top_ten_mean_contributors, rotation  = 37, fontsize = 9)
            plt.ylabel("kt(N)/yr")
            plt.grid(True, axis = "y")
            plt.title("Top ten total nitrogen contributors for " + receptors[receptor])
            plt.savefig(path + "/TOT_top_ten/mean_1995_2020/"+receptors[receptor].strip())

        else : 
            plt.bar(top_ten_mean_contributors,top_ten_mean_values, color = "red")
            plt.gcf().subplots_adjust(bottom=0.20)
            plt.xticks(top_ten_mean_contributors, rotation  = 37, fontsize = 9)
            plt.ylabel("kt(N)/yr")
            plt.grid(True, axis = "y")
            plt.title("Top ten reduced nitrogen contributors for " + receptors[receptor])
            plt.savefig(path + "/RDN_top_ten/mean_1995_2020/"+receptors[receptor].strip())
        
        plt.close()"""

    #year plots
    for receptor in range(len(top_ten)):
        for year in range(len(top_ten[0])):
            top_ten_contributors = []
            top_ten_values = []
            for top in range(len(top_ten[0][0])):
                top_ten_contributors.append(long_name(top_ten[receptor][year][top][1])) 
                top_ten_values.append(top_ten[receptor][year][top][0])
            
            if pollutant == OXN :
                plt.bar(top_ten_contributors,top_ten_values, color = "blue")
                plt.gcf().subplots_adjust(bottom=0.20)
                plt.xticks( rotation  = 37, fontsize = 9)
                plt.ylabel("kt(N)/yr")
                plt.grid(True, axis = "y")
                plt.title("Top ten oxidized nitogen contributors in " + str(list_years[year])+ " for " + receptors[receptor]) 
                plt.savefig(path + "/OXN_top_ten/" + str(list_years[year]) + "/"+receptors[receptor].strip())
            
            elif pollutant == TOT : 
                plt.bar(top_ten_contributors,top_ten_values, color = "green")
                plt.gcf().subplots_adjust(bottom=0.20)
                plt.xticks(rotation  = 37, fontsize = 9)
                plt.ylabel("kt(N)/yr")
                plt.grid(True, axis = "y")
                plt.title("Top ten total nitrogen contributors in " + str(list_years[year])+ "for " + receptors[receptor])
                plt.savefig(path + "/TOT_top_ten/" + str(list_years[year]) + "/"+receptors[receptor].strip())

            else : 
                plt.bar(top_ten_contributors,top_ten_values, color = "red")
                plt.gcf().subplots_adjust(bottom=0.20)
                plt.xticks(rotation  = 37, fontsize = 9)
                plt.ylabel("kt(N)/yr")
                plt.grid(True, axis = "y")
                plt.title("Top ten reduced nitrogen contributors in " + str(list_years[year])+ " for " + receptors[receptor])
                plt.savefig(path + "/RDN_top_ten/" + str(list_years[year]) + "/"+receptors[receptor].strip())
                      
            plt.close()
            

