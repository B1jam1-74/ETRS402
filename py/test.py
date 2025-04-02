import numpy as np
import matplotlib.pyplot as plt

# Données
x = np.array([20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
y = np.array([510, 385, 310, 250, 210, 175, 150, 130, 115, 100, 90])

# Ajustement d'un polynôme de degré 2
coeffs_deg2 = np.polyfit(x, y, 2)  # Degré 2
poly_deg2 = np.poly1d(coeffs_deg2)
print("Polynôme de degré 2 :")
print(poly_deg2)

# Ajustement d'un polynôme de degré 3
coeffs_deg3 = np.polyfit(x, y, 3)  # Degré 3
poly_deg3 = np.poly1d(coeffs_deg3)
print("\nPolynôme de degré 3 :")
print(poly_deg3)

# Visualisation pour comparer
x_smooth = np.linspace(min(x), max(x), 200)  # Pour une courbe lisse
y_deg2 = poly_deg2(x_smooth)
y_deg3 = poly_deg3(x_smooth)

plt.scatter(x, y, color='blue', label='Données')
plt.plot(x_smooth, y_deg2, color='red', label='Polynôme degré 2')
plt.plot(x_smooth, y_deg3, color='green', label='Polynôme degré 3')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

# Calcul de l'erreur (somme des carrés des écarts)
error_deg2 = np.sum((poly_deg2(x) - y) ** 2)
error_deg3 = np.sum((poly_deg3(x) - y) ** 2)
print(f"\nErreur (somme des carrés) pour degré 2 : {error_deg2:.2f}")
print(f"Erreur (somme des carrés) pour degré 3 : {error_deg3:.2f}")