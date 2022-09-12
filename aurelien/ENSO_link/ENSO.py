import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import random as rd

#ouverture des donnees
SOI_index = np.genfromtxt("/home/aurelienh/Desktop/Int/ENSO_link/SOI_index.txt")
table_2018 = pd.read_csv("/home/aurelienh/Desktop/Int/ENSO_link/oxidised_nitrogen_2018.csv")
table_2019 = pd.read_csv("/home/aurelienh/Desktop/Int/ENSO_link/oxidised_nitrogen_2019.csv")

#Mise en forme des indices SOI pour l'ENSO
list_SOI = []
year = []
month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec",]
absc = []
start = 1990
compt = 0
for i in range(np.shape(SOI_index)[0]):
    for j in range(np.shape(SOI_index)[1]-1):
        list_SOI.append(SOI_index[i][j+1])
        compt = compt + 1
        if compt%12 == 0 and i!=np.shape(SOI_index)[0]:
            year.append(int(start+1))
            start =start+1
            month2 = []
            for i in range(len(month)):
                absc.append(month[i]+str(start))
        else:
            pass

#Mise en forme des tables SR
result_2018=[]
with open("/home/aurelienh/Desktop/Int/ENSO_link/oxidised_nitrogen_2018.csv") as data:
    for line in csv.reader(data):
        result_2018.append(line[0].split("\t"))
SR_name_2018 = result_2018[0]

result_2019=[]
with open("/home/aurelienh/Desktop/Int/ENSO_link/oxidised_nitrogen_2019.csv") as data:
    for line in csv.reader(data):
        result_2019.append(line[0].split("\t"))
SR_name_2019 = result_2019[0]

def convert(liste):
    float_list = []
    for i in range(1,len(liste)):
        if liste[i] == "":
            float_list.append(0.0)
        else:
            float_list.append(float(liste[i]))
    return float_list

#Normalisation
emission_2018 = convert(result_2018[-1])
emission_2019 = convert(result_2019[-1])

index_2018 = SR_name_2018.index("CH")
index_2019 = SR_name_2019.index("CH")

C = emission_2018[index_2018]/emission_2019[index_2019]

def select_nino():
    year = rd.randint(0,2)
    while list_SOI[year]<0:
        year = rd.randint(0,2)
    return year

def select_nina():
    year = rd.randint(0,2)
    while list_SOI[year]>0:
        year = rd.randint(0,2)
    return year

#year_nina = select_nina()
#year_nino = select_nino()
year_nina = 2019
year_nino = 2018

index_recepteur = SR_name_2019.index("AL")
list_recep = result_2019[index_recepteur]
newSR = C*convert(result_2019[index_recepteur])[index_2019]

normalized = (newSR + convert(result_2019[index_recepteur])[index_2019])/2
print(normalized)

#Graphe de la serie temporelle des SOI
plt.plot(absc,list_SOI)
plt.xticks(rotation=90,fontsize=5)
plt.axhline(y=0,color="black")
plt.axhline(y=1,color="red",label="Nino")
plt.axhline(y=-1,color="blue",label="Nina")
plt.legend()
plt.show()
