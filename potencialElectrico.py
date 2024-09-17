import numpy as np
import matplotlib.pyplot as plt

# Constantes
k = 8.99e9  # Constante de Coulomb en N·m²/C²
micro = 1e-6  # Factor de conversión de microcoulombs a coulombs


# Función para calcular el campo eléctrico de una carga puntual
def campo_electrico(q, xq, yq, X, Y):
    # Distancia r
    r = np.sqrt((X - xq) ** 2 + (Y - yq) ** 2)
    # Evitar divisiones por cero
    r[r == 0] = np.inf
    # Componentes del campo
    Ex = k * q * (X - xq) / r ** 3
    Ey = k * q * (Y - yq) / r ** 3
    return Ex, Ey


# Función para calcular el potencial eléctrico de una carga puntual
def potencial(q, xq, yq, X, Y):
    r = np.sqrt((X - xq) ** 2 + (Y - yq) ** 2)
    r[r == 0] = np.inf
    V = k * q / r
    return V


# Solicitar el número de cargas
num_cargas = int(input("Ingrese la cantidad de cargas: "))

# Crear una lista vacía para almacenar las cargas
cargas = []

# Pedir al usuario que ingrese la posición (x, y) y el valor de la carga para cada una en picocoulombs
for i in range(num_cargas):
    q_pC = float(input(f"Ingrese el valor de la carga {i + 1} en microcoulombs (µC): "))
    xq = float(input(f"Ingrese la posición x de la carga {i + 1}: "))
    yq = float(input(f"Ingrese la posición y de la carga {i + 1}: "))
    # Convertir de picocoulombs a coulombs
    q = q_pC * micro
    cargas.append((q, xq, yq))

# Pedir al usuario donde quiere calcular el campo eléctrico y el potencial
xpedido = float(input("Ingrese la posición x donde desea calcular el campo eléctrico y el potencial: "))
ypedido = float(input("Ingrese la posición y donde desea calcular el campo eléctrico y el potencial: "))

# Malla de puntos en el espacio de tamaño 10x10  (grilla)
x = np.linspace(-3, 3, 601)
y = np.linspace(-3, 3, 601)
X, Y = np.meshgrid(x, y)

# Inicializar componentes del campo eléctrico total
Ex_total = np.zeros_like(X)
Ey_total = np.zeros_like(Y)

# Inicializar el potencial total
V_total = np.zeros_like(X)

# Sumar el campo de cada carga
for q, xq, yq in cargas:
    Ex, Ey = campo_electrico(q, xq, yq, X, Y)
    Ex_total += Ex
    Ey_total += Ey

# Sumar el potencial de cada carga para obtener el potencial total
for q, xq, yq in cargas:
    V_total += potencial(q, xq, yq, X, Y)


def scale_value(x):
    # Rango de entrada
    x_min, x_max = -3, 3
    # Rango de salida
    y_min, y_max = 0, 600

    # Aplicar la fórmula de escalado
    y = ((x - x_min) / (x_max - x_min)) * (y_max - y_min) + y_min

    return y


# Gráfico del campo eléctrico (streamplot) y líneas equipotenciales
plt.figure(figsize=(8, 8))

# Dibujar las líneas equipotenciales del potencial total
plt.contour(X, Y, V_total, levels=500, cmap='summer', alpha=0.75)

# Dibujar el campo eléctrico como flechas vectoriales
plt.streamplot(X, Y, Ex_total, Ey_total, color='black', linewidth=1)

# Dibujar las posiciones de las cargas
for q, xq, yq in cargas:
    plt.plot(xq, yq, 'ro' if q > 0 else 'bo', ms=10, label=f'{q / micro:.2f} µC')

# Etiquetas y título
plt.title('Campo Eléctrico y Líneas Equipotenciales de Cargas Puntuales en el Espacio \n '
          'El valor del campo eléctrico '
          'en el punto ({},{}) es: Ex = {} N/C, Ey = {} N/C \n'
          'El valor del potencial eléctrico '
          'en el punto ({},{}) es: V = {} V'.format(xpedido, ypedido,
                                                    Ex_total[int(scale_value(ypedido)), int(scale_value(xpedido))],
                                                    Ey_total[int(scale_value(ypedido)), int(scale_value(xpedido))],
                                                    xpedido, ypedido,
                                                    V_total[int(scale_value(ypedido)), int(scale_value(xpedido))]))
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc='upper right')
plt.legend(title='Cargas')
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)

plt.show()
