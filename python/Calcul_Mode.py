"""
Script python pour ouvrir les fichiers de traces de clavier
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from os import listdir
from os.path import isfile, join
import csv
from collections import Counter


def read_int(f):
    ba = bytearray(4)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.int32)
    return prm[0]
    
def read_double(f):
    ba = bytearray(8)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.double)
    return prm[0]

def read_double_tab(f, n):
    ba = bytearray(8*n)
    nr = f.readinto(ba)
    if nr != len(ba):
        return []
    else:
        prm = np.frombuffer(ba, dtype=np.double)
        return prm
    
def get_pics_from_file(filename):
    # Lecture du fichier d'infos + pics detectes (post-processing KeyFinder)
    print("Ouverture du fichier de pics "+filename)
    f_pic = open(filename, "rb")
    info = dict()
    info["nb_pics"] = read_int(f_pic)
    print("Nb pics par trame: " + str(info["nb_pics"]))
    info["freq_sampling_khz"] = read_double(f_pic)
    print("Frequence d'echantillonnage: " + str(info["freq_sampling_khz"]) + " kHz")
    info["freq_trame_hz"] = read_double(f_pic)
    print("Frequence trame: " + str(info["freq_trame_hz"]) + " Hz")
    info["freq_pic_khz"] = read_double(f_pic)
    print("Frequence pic: " + str(info["freq_pic_khz"]) + " kHz")
    info["norm_fact"] = read_double(f_pic)
    print("Facteur de normalisation: " + str(info["norm_fact"]))
    tab_pics = []
    pics = read_double_tab(f_pic, info["nb_pics"])
    nb_trames = 1
    while len(pics) > 0:
        nb_trames = nb_trames+1
        tab_pics.append(pics)
        pics = read_double_tab(f_pic, info["nb_pics"])

    print("Nb trames: " + str(nb_trames))
    f_pic.close()
    return tab_pics, info

def average_column (csv_filepath):
    column_totals = Counter()
    with open('../Val_pics_CSV/'+csv_filepath,"rb") as f:
        reader = csv.reader(f)
        row_count = 0.0
        for row in reader:
            for column_idx, column_value in enumerate(row):
                try:
                    n = float(column_value)
                    column_totals[column_idx] += n
                except ValueError:
                    print ("Error -- ({}) Column({}) could not be converted to float!".format(column_value, column_idx))                   
            row_count += 1.0            

    # row_count is now 1 too many so decrement it back down
    row_count -= 1.0

    # make sure column index keys are in order
    column_indexes = column_totals.keys()
    column_indexes.sort()

    # calculate per column averages using a list comprehension
    averages = [column_totals[idx]/row_count for idx in column_indexes]
    return averages

def Modecsv(file):

	data = pd.read_csv('../Val_pics_CSV/'+ file) 
	data = data.mode(dropna=False)
	data = data.head(1)
	name = [file]
	data['Lettre'] = name
	#data.to_csv ('../Mode_CSV/'+ file, index = False, header=True)
	return data



if __name__ == "__main__":


	#Traitement densité sur chaque .bin
	fichiers_liste = [f for f in listdir("../Val_pics_CSV/") if isfile(join("../Val_pics_CSV/", f))] #liste des fichier .bin
	CSV = pd.DataFrame()
	for i in range(len(fichiers_liste)):
		print("Traitement fichier : " + fichiers_liste[i]+ "\n")
		#print(Modecsv(fichiers_liste[i]))
		CSV = pd.concat([CSV, Modecsv(fichiers_liste[i])])

	print(CSV)
	CSV.to_csv ('../Mode_CSV/valeur_dominante_concat.csv', index = False, header=True)

	


	    

'''
	    nom = str(fichiers_liste[i])
	    nom = nom.replace('.bin','')
	
	    plt.figure(1)
	    plt.subplot(211)
	    #boucle sur le nombre total de trames
	    for j in range(len(graph)) :
	    	x = range(1,info["nb_pics"]+1)
	    	y = graph[j] 	
	    	plt.hist2d(x,y,(50, 50), cmap=plt.cm.jet) #histo2D avec colorisation densité
	  
	    plt.xlabel('numéro de pic')
	    plt.ylabel('valeur du pic')
	    plt.title(fichiers_liste[i] + ' densité') #Titre graph
	    plt.ylim(0, 1.5)
	    plt.grid(b=True, which='both')

	    plt.show() #Affichage graph
	    plt.savefig(nom) #SAVE graph à la racine du programme 


	    
	    #Deuxieme affichage
	    plt.subplot(212)
	    plt.plot(range(1,info["nb_pics"]+1), graph[234], 'ko')
	    plt.xlabel('numéro de pic')
	    plt.ylabel('valeur du pic')
	    plt.title(fichier+' permier')
	    plt.ylim(0, 1.5)
	    plt.grid(b=True, which='both')
	    '''

	    
	    


	   
	    




	    	

	
	    
    