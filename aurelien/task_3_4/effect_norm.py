import os
import csv
import numpy as np
import matplotlib.pyplot as plt
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
            #print(line[0])
            result.append(line)
    SR_name_sources = result[0]
    SR_name_receptors =[]
    for i in range(1,np.shape(result)[0]):
        SR_name_receptors.append(result[i][0])
    return [SR_name_sources,SR_name_receptors,result,filename]

reduced_95 = open_SR_tab("/home/aurelienh/Desktop/Int/task_3_4/result/output_SR_oxidised_1995-2020_2019.csv")
reduced_10 = open_SR_tab("/home/aurelienh/Desktop/Int/task_3_4/result/output_SR_oxidised_2010-2020_2019.csv")

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

def sorting(heiko_sources,heiko_result,jurek_sources,jurek_result):
    """
    Now, we applied the function filter_heiko_tables on heiko's tab and the function filter_jurek_tables on the jurek's tab.
    We need to be sure if the sources are in the same order in the jurek's tab than in the heiko's tab.
    This function re order the tab.
    input:
    - heiko_sources: the first element of the return of the function filter_heiko_tables.
    - heiko_result: the second element of the return of the function flter_heiko_tables.
    - jurek_sources: the first element of the return of the function filter_jurek_tables.
    - jurek_result: the second element of the return of the function flter_jurek_tables.
    return:
    - A list with heiko's tab and sources. The heiko tab is now sorted to fit with the jure's tab. First element is the filtered sources and second element is the filtered value tab.
    """
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

value_95 = convert(reduced_95[2])
value_10 = convert(reduced_10[2])

sources_95 = reduced_95[0][1:]
sources_10 = reduced_10[0][1:]

temp = sorting(sources_95,value_95,sources_10,value_10)
sources_95bis = temp[0]
value_95bis = temp[1]

#index_value = 9

def plot_1(index_value):
    for i in range(len(sources_95bis)):
        if i==0:
            plt.bar(sources_95bis[i],value_95bis[index_value][i],color="red",label="Normalization 1995-2020")
            plt.bar(sources_10[i],value_10[index_value][i],color="blue",alpha=0.5,label="Normalization 2010-2020")
        else:
            plt.bar(sources_95bis[i],value_95bis[index_value][i],color="red")
            plt.bar(sources_10[i],value_10[index_value][i],color="blue",alpha=0.5)
    plt.title("All sources contribution for "+str(reduced_95[1][index_value]))
    plt.legend()
    plt.xticks(rotation=45,fontsize=8)
    plt.savefig("/home/aurelienh/Desktop/Int/task_3_4/result/oxidised_25years_comparaison/all_sources_contribution/all_sources_contribution_for_"+str(reduced_95[1][index_value])+".jpg",dpi=1000)
    plt.close()

def plot_2(index_value):
    for i in range(len(sources_95)):
        ratio = (min([value_95bis[index_value][i],value_10[index_value][i]]))/(max([value_95bis[index_value][i],value_10[index_value][i]]))
        plt.bar(sources_95bis[i],ratio,color="blue")
    plt.axhline(y=0.5,color="black",label="ratio 0.5")
    plt.title("2019 for "+str(reduced_95[1][index_value])+": Ratio min(normalization 1995-2020, normalization 2010-2020) / max(normalization 1995-2020, normalization 2010-2020)",fontsize=6)
    plt.legend()
    plt.xticks(rotation=45,fontsize=8)
    plt.savefig("/home/aurelienh/Desktop/Int/task_3_4/result/oxidised_25years_comparaison/ratio/ratio_sources_"+str(reduced_95[1][index_value])+".jpg",dpi=1000)
    plt.close()

for i in tqdm(range(len(reduced_95[1]))):
    plot_1(i)
    plot_2(i)

#regarder pour une source tout les recepteurs.Inverse de plus haut.
