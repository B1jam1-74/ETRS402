import serial
import time
import os

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

#initialise billy
billy = []
for i in range (90):
    billy.append([])

fini = True
ser = serial.Serial(PORT, BAUD_RATE, timeout=1, rtscts=True, dsrdtr=True, write_timeout=0)
time.sleep(2)  # Attendre que la connexion soit stable
while fini:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line == '9999':
            i = 0
            while i < 90:
                line = ser.readline().decode('utf-8').strip()
                if line == '-9999':  # End marker
                    break
                elif line.isdigit() or (line.startswith('-') and line[1:].isdigit()):  # Ensure the line contains only digits with optional negative sign
                    billy[i].append(int(line))
                    time.sleep(0.01)  # Small delay to prevent reading too fast
                else:
                    i -= 1
                os.system('clear')
                print(billy)
                i += 1
        # quand on a fait 3 fois le tour car on a 3 valeurs dans billy[2][-1]
        if len(billy[2]) == 3:
            fini = False


ser.close()
#creer un clone de billy
billy2 = []
for i in range (90):
    billy2.append([])
# mettre les moyennes dans billy2
for i in range(90):
    if len(billy[i]) > 0:
        moyenne = sum(billy[i]) / len(billy[i])
        billy2[i].append(moyenne)

os.system('clear')

#convertir les données en cm
for i in range(90):
    for j in range(len(billy2[i])):
        # Formula from MATLAB polyfit with exact coefficients
        billy2[i][j] = 0.000000014078219*(billy2[i][j]**4) - 0.000021664228*(billy2[i][j]**3) + 0.0121434129*(billy2[i][j]**2) - 3.050156069*billy2[i][j] + 336.02811204 #0.0000000106*billy2[i][j]**4 + (-0.0000146535)*(billy2[i][j]**3) + 0.0076086045*(billy2[i][j]**2) + (-1.9072664930)*(billy2[i][j]) + 239.0912491215
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
    # Afficher un quatrieme graphique polaire avec la moyenne mobile
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, projection='polar')
    
    # Extraire les données de distance
    data = np.array([val[0] for val in billy2])
    
    # Calculer la moyenne mobile
    window_size = 10
    weights = np.ones(window_size) / window_size
    data_smooth = np.convolve(data, weights, mode='valid')
    
    # Ajuster les angles pour correspondre à la taille réduite après convolution
    angles_smooth = np.linspace(0, 270, len(data_smooth))
    angles_smooth_rad = np.radians(angles_smooth)
    
    # Tracer la moyenne mobile
    ax.plot(angles_smooth_rad, data_smooth, c='blue', linewidth=2)
    ax.scatter(angles_rad, [val[0] for val in billy2], c='red', s=5, alpha=0.3)
    
    ax.set_title('Moyenne mobile du scan')
    ax.set_theta_zero_location('N')  # 0 degrés au Nord
    ax.set_theta_direction(-1)  # Sens horaire
    ax.set_rlabel_position(0)
    
    # Ajouter une légende
    plt.legend(['Moyenne mobile', 'Données brutes'])
    
    plt.tight_layout()
    plt.show()