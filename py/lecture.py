import serial
import time
import os

PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

#initialise billy
billy = []
for i in range (270*2):
    billy.append([])

fini = True
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Attendre que la connexion soit stable
while fini:
    if ser.in_waiting > 0:
        if ser.readline().decode('utf-8').strip() == '9999':
            for i in range(270*2):
                billy[i].append(int(ser.readline().decode('utf-8').strip()))
                os.system('clear')
                print(billy)
        #quand on a fait 3 fois le tour car on a 3 valeurs dans billy[2][-1]
        if len(billy[2]) == 3:
            fini = False


ser.close()
#creer un clone de billy
billy2 = []
for i in range (270*2):
    billy2.append([])
# mettre les moyennes dans billy2
for i in range(270*2):
    if len(billy[i]) > 0:
        moyenne = sum(billy[i]) / len(billy[i])
        billy2[i].append(moyenne)

os.system('clear')

#convertir les données en cm
for i in range(270*2):
    for j in range(len(billy2[i])):
        # Formula from MATLAB polyfit with exact coefficients
        billy2[i][j] = 0.0000000106*billy2[i][j]**4 + (-0.0000146535)*(billy2[i][j]**3) + 0.0076086045*(billy2[i][j]**2) + (-1.9072664930)*(billy2[i][j]) + 239.0912491215
print(billy2)


#affichzer la vision 2d des valeurs

import matplotlib.pyplot as plt
import numpy as np

# Convertir la liste de listes en tableau numpy
billy2 = np.array(billy2)

# Vérifier si billy contient des données valides
if billy2.size > 0:
    # Extraire les valeurs de distance
    distances = [val[0] for val in billy2]
    
    # Créer les angles (de 0 à 270 degrés)
    angles = np.linspace(0, 270, len(distances))
    
    # Convertir en radians pour les calculs
    angles_rad = np.radians(angles)
    
    # Convertir en coordonnées cartésiennes
    x = distances * np.cos(angles_rad)
    y = distances * np.sin(angles_rad)
    
    # Créer un graphique cartésien
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y, c='blue', s=10, alpha=0.7)
    plt.scatter(0, 0, c='red', s=100, marker='*')  # Position du capteur
    
    # Limites du graphique
    max_dist = max(distances)
    plt.xlim(-max_dist*1.1, max_dist*1.1)
    plt.ylim(-max_dist*1.1, max_dist*1.1)
    
    plt.grid(True)
    plt.title('Scan 2D de la pièce (270 degrés)')
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    
    # Ajouter une légende
    plt.plot([], [], 'r*', markersize=10, label='Capteur')
    plt.plot([], [], 'bo', markersize=5, label='Points de mesure')
    plt.legend()

    plt.show()


    # Créer un second graphique en coordonnées polaires
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, projection='polar')
    ax.scatter(angles_rad, distances, c='blue', s=10, alpha=0.7)
    ax.set_title('Scan en coordonnées polaires')
    ax.set_theta_zero_location('N')  # 0 degrés au Nord
    ax.set_theta_direction(-1)  # Sens horaire
    ax.set_rlabel_position(0)
    
    plt.tight_layout()
    plt.show()

    # Créer un graphique avec les courbes superposées pour chaque angle
    plt.figure(figsize=(15, 8))
    angles = np.linspace(0, 270, len(billy))
    
    # Pour chaque scan (0, 1, 2)
    for scan_idx in range(min([len(row) for row in billy if len(row) > 0])):
        # Extraire les données du scan
        scan_data = [row[scan_idx] if scan_idx < len(row) else float('nan') for row in billy]
        plt.plot(angles, scan_data, label=f'Scan {scan_idx+1}')
    
    plt.title('Scans superposés')
    plt.xlabel('Angle (degrés)')
    plt.ylabel('Distance (mm)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    # Afficher les données