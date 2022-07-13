import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import statistics as st
table = pd.read_csv("/home/aurelienh/Desktop/Int/2010_reduced_nitrogenLF.csv")

"""def new_tab(tab):
    nbr_ligne = np.shape(tab)[0]
    head_col = []
    for i in range(len(str(tab.columns))):
        if str(tab.columns)[i] == "t":
            if str(tab.columns)[i+1:i+4] !="ype":
                if str(tab.columns)[i+1]!="'":
                    head_col.append(str(tab.columns)[i+1]+str(tab.columns)[i+2])
                else:
                    pass
            else:
                pass
        else:
            pass
    head_li = []
    for i in range(np.shape(tab.values)[0]):
        head_li.append(tab.values[i][0][:2])
    table = np.zeros((len(head_li),len(head_col)))
    for i in range(len(head_li)):
        print(tab.values[2][0])
        for j in range(len(str(tab.values[i][0]))):
            if str(tab.values[i][0])[j] == "\t":
                k = 1
                val = ""
                if j+k<len(str(tab.values[i][0])):
                    print(j+k)
                    while str(tab.values[i][0])[j+k-1] != "\t":
                        val = val + str(tab.values[i][0])[j+k-1]
                        print(val)
                        k = k +1
                    else:
                        pass
                table[i][j] = float(val)

            else:
                pass
    return table"""

result=[]
with open("/home/aurelienh/Desktop/Int/2010_reduced_nitrogenLF.csv") as data:
    for line in csv.reader(data):
        result.append(line[0].split("\t"))
SR_name = result[0]

def convert(liste):
    float_list = []
    for i in range(1,len(liste)):
        float_list.append(float(liste[i]))
    return float_list

def plotage(recepteur):
    index = SR_name.index(recepteur)
    X = np.linspace(0,len(convert(result[index])),len(convert(result[index])))
    for i in range(len(X)):
        plt.bar(SR_name[i+1],convert(result[index])[i])
    plt.xticks(rotation=45)
    moyenne = st.mean(convert(result[index]))
    median = st.median(convert(result[index]))
    q75 = np.percentile(convert(result[index]),90)
    plt.axhline(y=moyenne,color="r",label="mean")
    plt.axhline(y=median,color="b",label="median")
    plt.axhline(y=q75,color="y",label="Q90")
    plt.title("Emitters for "+recepteur)
    plt.ylabel("100 Mg of N")
    plt.legend()
    plt.show()