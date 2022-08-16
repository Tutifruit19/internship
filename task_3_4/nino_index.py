import csv
import numpy as np
import matplotlib.pyplot as plt
import statistics as sc
from tqdm import tqdm

SOI_index = np.genfromtxt("/home/aurelienh/Desktop/Int/ENSO_link/SOI_index.txt")

years_SOI = []
for i in range(np.shape(SOI_index)[0]):
    years_SOI.append(int(SOI_index[i][0]))

SOI_tab = np.zeros((np.shape(SOI_index)[0],np.shape(SOI_index)[1]-1))
for i in range(np.shape(SOI_index)[0]):
    for j in range(1,np.shape(SOI_index)[1]):
        SOI_tab[i][j-1] = int(SOI_index[i][j])

year_mean_SOI = []
for i in range(np.shape(SOI_tab)[0]):
    year_mean_SOI.append(sum(SOI_tab[i])/len(SOI_tab[i]))

number_year = 6

min_list = []
min_index = []
max_list = []
max_index = []
for i in range(int(number_year/2)):
    min_list.append(min(year_mean_SOI))
    max_list.append(max(year_mean_SOI))
    min_index.append(year_mean_SOI.index(min(year_mean_SOI)))
    max_index.append(year_mean_SOI.index(max(year_mean_SOI)))
    year_mean_SOI[min_index[-1]] = 0
    year_mean_SOI[max_index[-1]] = 0

years_max = []
years_min = []
for i in range(len(max_index)):
    years_max.append(years_SOI[max_index[i]])
    years_min.append(years_SOI[min_index[i]])

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

tab_1 = open_SR_tab("/home/aurelienh/Desktop/Int/task_3_4/result/output_SR_reduced_1995-2020_2019.csv")
tab_2 = open_SR_tab("/home/aurelienh/Desktop/Int/task_3_4/result/output_SR_reduced_enso6_2019.csv")

value_1 = convert(tab_1[2])
value_2 = convert(tab_2[2])

sources_1 = tab_1[0][1:]
sources_2 = tab_2[0][1:]

temp = sorting(sources_1,value_1,sources_2,value_2)
sources_1bis = temp[0]
value_1bis = temp[1]

def plot_1(index_value):
    for i in range(len(sources_1bis)):
        if i==0:
            plt.bar(sources_1bis[i],value_1bis[index_value][i],color="red",label="Normalization 1995-2020")
            plt.bar(sources_2[i],value_2[index_value][i],color="blue",alpha=0.5,label="Normalization 3 years nina and 3 years nino")
        else:
            plt.bar(sources_1bis[i],value_1bis[index_value][i],color="red")
            plt.bar(sources_2[i],value_2[index_value][i],color="blue",alpha=0.5)
    plt.title("All sources contribution for "+str(tab_1[1][index_value]))
    plt.legend()
    plt.xticks(rotation=45,fontsize=8)
    plt.savefig("/home/aurelienh/Desktop/Int/task_3_4/result/enso_comp_6_reduced/all_sources_contribution/all_sources_contribution_for_"+str(tab_1[1][index_value])+".jpg",dpi=1000)
    plt.close()

def plot_2(index_value):
    for i in range(len(sources_1bis)):
        ratio = (min([value_1bis[index_value][i],value_2[index_value][i]]))/(max([value_1bis[index_value][i],value_2[index_value][i]]))
        plt.bar(sources_1bis[i],ratio,color="blue")
    plt.axhline(y=0.5,color="black",label="ratio = 0.5")
    plt.axhline(y=0.9,color="red",label="ratio = 0.9")
    plt.title("2019 for "+str(tab_1[1][index_value])+": Ratio min(normalization 1995-2020, normalization enso 6 years) / max(normalization 1995-2020, normalization enso 6 years)",fontsize=6)
    plt.legend()
    plt.xticks(rotation=45,fontsize=8)
    plt.savefig("/home/aurelienh/Desktop/Int/task_3_4/result/enso_comp_6_reduced/ratio/ratio_sources_"+str(tab_1[1][index_value])+".jpg",dpi=1000)
    plt.close()

def run():
    for i in tqdm(range(len(tab_1[1]))):
        plot_1(i)
        plot_2(i)
