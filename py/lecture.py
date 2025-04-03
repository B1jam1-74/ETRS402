import serial
import time
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import matplotlib.pyplot as plt
import numpy as np

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Initialise billy
billy = []
for i in range(90):
    billy.append([])

# Fonction pour la collecte des données
def collect_data():
    global billy, fini
    fini = True
    
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1, rtscts=True, dsrdtr=True, write_timeout=0)
        time.sleep(2)  # Attendre que la connexion soit stable
        
        status_var.set("Collecte des données en cours...")
        progress_bar['value'] = 0
        
        while fini:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line == '9999':
                    i = 0
                    # Calculer le scan actuel (0, 1 ou 2)
                    current_scan = 0
                    if len(billy[0]) > 0:
                        current_scan = len(billy[0])
                    
                    # Mise à jour de la barre de progression globale
                    progress_bar['value'] = (current_scan * 33.33)
                    root.update_idletasks()
                    
                    while i < 90:
                        line = ser.readline().decode('utf-8').strip()
                        if line == '-9999':  # End marker
                            break
                        elif line.isdigit() or (line.startswith('-') and line[1:].isdigit()):  # Ensure the line contains only digits with optional negative sign
                            billy[i].append(int(line))
                            time.sleep(0.01)  # Small delay to prevent reading too fast
                        else:
                            i -= 1
                        
                        # Update progress bar within this scan (scaled to the current scan)
                        scan_progress = (i / 90) * 33.33
                        progress_bar['value'] = (current_scan * 33.33) + scan_progress
                        root.update_idletasks()
                        i += 1
                
                # quand on a fait 3 fois le tour car on a 3 valeurs dans billy[2][-1]
                if len(billy[2]) == 3:
                    # Si après 3 scans il y a des positions sans valeur, utiliser la valeur précédente
                    for i in range(90):
                        for scan in range(1, 3):  # Pour les scans 2 et 3
                            if len(billy[i]) <= scan:  # Si le scan n'a pas de valeur
                                billy[i].append(billy[i-1][scan])  # Utiliser la valeur du scan précédentfor i in range(90):
                    
                    fini = False
                    status_var.set("Collecte terminée!")
                    process_button['state'] = 'normal'
                    show_raw_button['state'] = 'normal'
        
        ser.close()
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication série: {e}")
        status_var.set("Erreur de communication")

# Fonction pour lancer la collecte dans un thread séparé
def start_collection():
    collect_button['state'] = 'disabled'
    process_button['state'] = 'disabled'
    show_button['state'] = 'disabled'
    show_raw_button['state'] = 'disabled'
    
    # Réinitialiser billy
    global billy
    billy = []
    for i in range(90):
        billy.append([])
    
    # Lancer la collecte dans un thread séparé
    threading.Thread(target=collect_data, daemon=True).start()

# Fonction pour traiter les données
def process_data():
    status_var.set("Traitement des données...")
    
    try:
        # Créer un clone de billy
        global billy2
        billy2 = []
        for i in range(90):
            billy2.append([])
        
        # Mettre les moyennes dans billy2
        for i in range(90):
            if len(billy[i]) > 0:
                moyenne = sum(billy[i]) / len(billy[i])
                billy2[i].append(moyenne)
        
        # Convertir les données en cm
        for i in range(90):
            for j in range(len(billy2[i])):
                # Formula from MATLAB polyfit with exact coefficients
                billy2[i][j] = 0.000000014078219*(billy2[i][j]**4) - 0.000021664228*(billy2[i][j]**3) + 0.0121434129*(billy2[i][j]**2) - 3.050156069*billy2[i][j] + 336.02811204
        
        status_var.set("Traitement terminé!")
        show_button['state'] = 'normal'
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du traitement: {e}")
        status_var.set("Erreur de traitement")

# Fonction pour afficher les graphiques
def show_graphs():
    status_var.set("Affichage des graphiques...")
    
    # Convertir la liste de listes en tableau numpy
    np_billy2 = np.array(billy2)
    
    # Vérifier si billy contient des données valides
    if np_billy2.size > 0:
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
        plt.xlabel('X (cm)')
        plt.ylabel('Y (cm)')
        
        # Calcul du périmètre
        # Fermer le polygone en ajoutant le premier point à la fin
        x_closed = np.append(x, x[0])
        y_closed = np.append(y, y[0])
        
        # Calcul du périmètre
        perimeter = 0
        for i in range(len(x) - 1):
            perimeter += np.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2)
        
        # Calcul de l'aire en utilisant la formule de Gauss (ou formule du lacet)
        area = 0
        for i in range(len(x)):
            area += (x[i] * y[(i + 1) % len(x)]) - (x[(i + 1) % len(x)] * y[i])  # Boucle fermée avec modulo
        area = abs(area) / 2
        
        # Ajouter les résultats au graphique
        plt.figtext(0.5, 0.01, f'Périmètre: {perimeter:.2f} cm | Aire: {area:.2f} cm²', 
                   ha='center', bbox={'facecolor':'white', 'alpha':0.8, 'pad':5})
        
        # Ajouter une légende
        plt.plot([], [], 'r*', markersize=10, label='Capteur')
        plt.plot([], [], 'bo', markersize=5, label='Points de mesure')
        plt.legend()
        
        plt.show(block=False)
        
        # Créer un second graphique en coordonnées polaires
        plt.figure(figsize=(10, 10))
        ax = plt.subplot(111, projection='polar')
        ax.scatter(angles_rad, distances, c='blue', s=10, alpha=0.7)
        ax.set_title('Scan en coordonnées polaires')
        ax.set_theta_zero_location('N')  # 0 degrés au Nord
        ax.set_theta_direction(-1)  # Sens horaire
        ax.set_rlabel_position(0)
        
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
        plt.ylabel('Distance (cm)')
        plt.legend()
        plt.grid(True)

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
        plt.show(block=False)
        
        status_var.set("Graphiques affichés")
    else:
        messagebox.showerror("Erreur", "Aucune donnée à afficher")
        status_var.set("Erreur d'affichage")

# Fonction pour afficher les valeurs brutes des 3 scans
def show_raw_values():
    if not billy or len(billy[0]) < 3:
        messagebox.showerror("Erreur", "Pas assez de données à afficher")
        return
    
    # Créer une nouvelle fenêtre
    raw_window = tk.Toplevel(root)
    raw_window.title("Valeurs brutes des 3 scans")
    raw_window.geometry("800x600")
    
    # Créer un notebook (onglets)
    notebook = ttk.Notebook(raw_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Créer un onglet pour chaque scan
    for scan_idx in range(3):
        # Créer un frame pour ce scan
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=f"Scan {scan_idx+1}")
        
        # Créer un widget de défilement
        scroll_frame = ttk.Frame(frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Créer un widget Text pour afficher les données
        text_widget = tk.Text(scroll_frame, yscrollcommand=scrollbar.set, width=60, height=30)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text_widget.yview)
        
        # Insérer les en-têtes
        text_widget.insert(tk.END, "Angle\tDistance (brute)\n")
        text_widget.insert(tk.END, "-" * 40 + "\n")
        
        # Insérer les données
        angles = np.linspace(0, 270, len(billy))
        
        for i, angle in enumerate(angles):
            if i < len(billy) and scan_idx < len(billy[i]):
                text_widget.insert(tk.END, f"{angle:.1f}°\t{billy[i][scan_idx]}\n")
            else:
                text_widget.insert(tk.END, f"{angle:.1f}°\tN/A\n")
        
        # Rendre le widget en lecture seule
        text_widget.config(state=tk.DISABLED)

# Créer l'interface graphique
root = tk.Tk()
root.title("Scanner Laser")
root.geometry("600x300")

# Variables
status_var = tk.StringVar()
status_var.set("Prêt")

# Frame principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Titre
title_label = ttk.Label(main_frame, text="Scanner Laser Contrôle", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Boutons
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=20)

collect_button = ttk.Button(button_frame, text="Collecter les données", command=start_collection)
collect_button.grid(row=0, column=0, padx=10)

process_button = ttk.Button(button_frame, text="Traiter les données", command=process_data, state='disabled')
process_button.grid(row=0, column=1, padx=10)

show_button = ttk.Button(button_frame, text="Afficher les graphiques", command=show_graphs, state='disabled')
show_button.grid(row=0, column=2, padx=10)

show_raw_button = ttk.Button(button_frame, text="Afficher valeurs brutes", command=show_raw_values, state='disabled')
show_raw_button.grid(row=1, column=1, padx=10, pady=10)

# Barre de progression
progress_frame = ttk.Frame(main_frame)
progress_frame.pack(fill=tk.X, pady=10)

progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=500, mode='determinate')
progress_bar.pack(fill=tk.X)

# Statut
status_label = ttk.Label(main_frame, textvariable=status_var)
status_label.pack(pady=10)

# Initialiser la variable globale
billy2 = []

# Lancer l'interface
if __name__ == "__main__":
    root.mainloop()