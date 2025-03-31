import serial
import time
import os

PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

#initialise billy
billy = []
for i in range (270):
    billy.append([])

fini = True
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Attendre que la connexion soit stable
while fini:
    if ser.in_waiting > 0:
        if ser.readline().decode('utf-8').strip() == '9999':
            for i in range(270):
                billy[i].append(int(ser.readline().decode('utf-8').strip()) )
                os.system('clear')
                print(billy)
                
            fini = False

ser.close()
# Afficher les données
import matplotlib.pyplot as plt
import numpy as np

# Convertir la liste de listes en tableau numpy
billy = np.array(billy)

# Vérifier si billy contient des données valides
if billy.size > 0:
    # Créer un graphique
    plt.figure(figsize=(10, 6))
    plt.plot(billy)  # Pas besoin de transposer, car chaque liste interne contient une seule valeur
    plt.title('Lecture des données')
    plt.xlabel('Index')
    plt.ylabel('Valeurs')
    plt.grid()
    plt.show()
else:
    print("Aucune donnée à afficher.")


