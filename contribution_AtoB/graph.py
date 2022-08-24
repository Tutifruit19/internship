import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from tqdm import tqdm

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

def fusion_open_SR_table(filename_1,filename_2):
    """
    Do the same as the function open_SR_tab but for the jurek's SR tab.
    In fact there are two Jurek's tab (one with OSPAR receptors and one with the HELCOM receptors).
    We need to merge the two
    return:
    -the same list than open_SR_tab with the merge
    """
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

def lin_reg(receptor_values,list_years):
        """

        Function that returns the y values of the linear regression between the years and the values of the receptor/emitter, the slope, the intercept and the r

        """
        mymodel = []
        slope, intercept, r, p, se = stats.linregress(list_years, receptor_values)
        for i in range(len(list_years)):
            mymodel.append(slope*list_years[i]+intercept)
        str_p_value = str(p)
        if "e" in str_p_value:
            index = str_p_value.find("e")
            nombre = str_p_value[0:4]
            puissance = str_p_value[index:index+4]
            result_p = nombre + puissance
        else :
            result_p = str(round(p, 3))

        return [mymodel, slope, intercept, r,result_p]

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

test_1 = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/Perturbation_method/data_jurek_helcom/dry_oxidised_nitrogen_2019.csv"
test_2 = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/Perturbation_method/data_jurek_ospar/dry_oxidised_nitrogen_2019.csv"

def plot_graph_brute(receptor,source,method,pol,normalization):
    if method == "Perturbation":
        if normalization == "n":
            norm_txt = "Normalization off"
            list_value = []
            for k in range(1995,2021):
                filename_1 = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/Perturbation_method/data_jurek_helcom/dry_"+pol+"_nitrogen_"+str(k)+".csv"
                filename_2 = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/Perturbation_method/data_jurek_ospar/dry_"+pol+"_nitrogen_"+str(k)+".csv"
                filename_1bis = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/Perturbation_method/data_jurek_helcom/wet_"+pol+"_nitrogen_"+str(k)+".csv"
                filename_2bis = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/Perturbation_method/data_jurek_ospar/wet_"+pol+"_nitrogen_"+str(k)+".csv"
                temp_dry = fusion_open_SR_table(filename_1,filename_2)
                temp_wet = fusion_open_SR_table(filename_1bis,filename_2bis)
                result_dry = convert(temp_dry[2])
                result_wet = convert(temp_wet[2])
                receptors_dry = temp_dry[1]
                receptors_wet = temp_wet[1]
                sources_dry = temp_dry[0]
                sources_wet = temp_wet[0]
                i_dry = receptors_dry.index(receptor)
                i_wet = receptors_wet.index(receptor)
                j_dry = sources_dry.index(source)
                j_wet = sources_wet.index(source)
                list_value.append((result_dry[i_dry][j_dry]+result_wet[i_wet][j_wet])/10)
        elif normalization == "y":
            norm_txt = "Normalization on"
            list_value = []
            for k in range(1995,2021):
                if k == 2015:
                    filename_1 = "/home/aurelienh/Desktop/Int/contribution_AtoB/normalized/Perturbation_method/"+pol+"/output_SR_"+str(k-1)+".txt"
                    filename_2 = "/home/aurelienh/Desktop/Int/contribution_AtoB/normalized/Perturbation_method/"+pol+"/output_SR_"+str(k+1)+".txt"
                    temp_1 = open_SR_tab(filename_1)
                    temp_2 = open_SR_tab(filename_2)
                    sources_1 = temp_1[0][1:]
                    sources_2 = temp_2[0][1:]
                    receptors_1 = temp_1[1]
                    receptors_2 = temp_2[1]
                    result_1 = convert(temp_1[2])
                    result_2 = convert(temp_2[2])
                    i_1 = receptors_1.index(receptor)
                    j_1 = sources_1.index(source)
                    i_2 = receptors_2.index(receptor)
                    j_2 = sources_2.index(source)
                    list_value.append((result_1[i_1][j_1]+result_2[i_2][j_2])/2)
                else:
                    filename = "/home/aurelienh/Desktop/Int/contribution_AtoB/normalized/Perturbation_method/"+pol+"/output_SR_"+str(k)+".txt"
                    temp = open_SR_tab(filename)
                    sources = temp[0][1:]
                    receptors = temp[1]
                    result = convert(temp[2])
                    i = receptors.index(receptor)
                    j = sources.index(source)
                    list_value.append(result[i][j])
    elif method =="Local fraction":
        if normalization =="n":
            norm_txt = "Normalization off"
            list_value = []
            for k in range(1995,2021):
                if k == 2015:
                    filename_1 = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/LocalFraction_method/"+str(k-1)+"_reduced_nitrogenLF.csv"
                    filename_2 = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/LocalFraction_method/"+str(k+1)+"_reduced_nitrogenLF.csv"
                    temp_1 = open_SR_tab(filename_1)
                    temp_2 = open_SR_tab(filename_2)
                    sources_1 = temp_1[0][1:]
                    sources_2 = temp_2[0][1:]
                    receptors_1 = temp_1[1]
                    receptors_2 = temp_2[1]
                    result_1 = convert(temp_1[2])
                    result_2 = convert(temp_2[2])
                    i_1 = receptors_1.index(receptor)
                    j_1 = sources_1.index(source)
                    i_2 = receptors_2.index(receptor)
                    j_2 = sources_2.index(source)
                    list_value.append((result_1[i_1][j_1]+result_2[i_2][j_2])/20)
                else:
                    filename = "/home/aurelienh/Desktop/Int/contribution_AtoB/brute/LocalFraction_method/"+str(k)+"_reduced_nitrogenLF.csv"
                    temp = open_SR_tab(filename)
                    sources = temp[0][1:]
                    receptors = temp[1]
                    result = convert(temp[2])
                    i = receptors.index(receptor)
                    j = sources.index(source)
                    list_value.append(result[i][j]/10)
        elif normalization == "y":
            norm_txt = "Normalization on"
            list_value = []
            for k in range(1995,2021):
                if k == 2015:

                else:
                    filename = "/home/aurelienh/Desktop/Int/contribution_AtoB/normalized/LocalFraction_method/RDN_LF_"+str(k)+".txt"
                    temp = open_SR_tab(filename)
                    sources = temp[0][1:]
                    receptors = temp[1]
                    result = convert(temp[2])
                    i = receptors.index(receptor)
                    j = sources.index(source)
                    list_value.append(result[i][j]/20)
    absc = np.linspace(1995,2020,26)
    plt.plot(absc,list_value,color="red",marker="o")
    lin = lin_reg(list_value,absc)
    p_value = kendall_tau(absc,list_value)
    plt.plot(absc,lin[0],color="black",linestyle="--",label="y = "+str(round(lin[1],2))+".x"+" + "+str(round(lin[2],2))+"\n"+"P-value (kendall test) = "+p_value+"\n"+"p-value (linear regression) = "+str(lin[4]))
    plt.title(source+" to "+receptor+" with "+method+" method. " +norm_txt)
    plt.xlabel("Years")
    plt.ylabel("Dep in kt(N)/yr")
    plt.grid()
    plt.legend()
    plt.show()