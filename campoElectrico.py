import numpy as np
import matplotlib.pyplot as plt

# Constantes
k = 8.99e9  # Constante de Coulomb en N·m²/C²
micro = 1e-6  # Factor de conversión de picocoulombs a coulombs

# Función para calcular el campo eléctrico de una carga puntual
def campo_electrico(q, xq, yq, X, Y):
    # Distancia r
    r = np.sqrt((X - xq)**2 + (Y - yq)**2)
    # Evitar divisiones por cero
    r[r == 0] = np.inf
    # Componentes del campo
    Ex = k * q * (X - xq) / r**3
    Ey = k * q * (Y - yq) / r**3
    return Ex, Ey

# Solicitar el número de cargas
num_cargas = int(input("Ingrese la cantidad de cargas: "))

# Crear una lista vacía para almacenar las cargas
cargas = []

# Pedir al usuario que ingrese la posición (x, y) y el valor de la carga para cada una en picocoulombs
for i in range(num_cargas):
    q_pC = float(input(f"Ingrese el valor de la carga {i+1} en microcoulombs (µC): "))
    xq = float(input(f"Ingrese la posición x de la carga {i+1}: "))
    yq = float(input(f"Ingrese la posición y de la carga {i+1}: "))
    # Convertir de picocoulombs a coulombs
    q = q_pC * micro
    cargas.append((q, xq, yq))

# Malla de puntos en el espacio (grilla)
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)

# Inicializar componentes del campo eléctrico total
Ex_total = np.zeros_like(X)
Ey_total = np.zeros_like(Y)

# Sumar el campo de cada carga
for q, xq, yq in cargas:
    Ex, Ey = campo_electrico(q, xq, yq, X, Y)
    Ex_total += Ex
    Ey_total += Ey

# Magnitud del campo eléctrico para las líneas de campo
E_magnitud = np.sqrt(Ex_total**2 + Ey_total**2)

# Gráfico de líneas de campo
plt.figure(figsize=(8, 8))
plt.streamplot(X, Y, Ex_total, Ey_total, color=E_magnitud, linewidth=1, cmap='coolwarm')

# Dibujar las posiciones de las cargas
for q, xq, yq in cargas:
    plt.plot(xq, yq, 'ro' if q > 0 else 'bo', ms=10, label=f'{q/micro:.2f} µC')

# Configurar el gráfico
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.title('Líneas de Campo Eléctrico')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar(label='Magnitud del Campo Eléctrico')
plt.grid(True)
plt.legend()
plt.show()
