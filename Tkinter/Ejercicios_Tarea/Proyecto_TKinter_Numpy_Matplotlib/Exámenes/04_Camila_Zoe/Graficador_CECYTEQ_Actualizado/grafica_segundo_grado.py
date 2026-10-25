import numpy as np

def calcular_segundo_grado(a, b, c):
    if a == 0:
        raise ValueError("En una ecuación de segundo grado, a no puede ser 0.")
    x = np.linspace(-10, 10, 500)
    y = a * x**2 + b * x + c
    xv = -b / (2 * a)
    yv = a * xv**2 + b * xv + c
    discriminante = b*b - 4*a*c
    raices = []
    if discriminante > 0:
        raices = [(-b + np.sqrt(discriminante))/(2*a), (-b - np.sqrt(discriminante))/(2*a)]
    elif abs(discriminante) < 1e-12:
        raices = [xv]
    return x, y, {"vertice": (xv, yv), "eje": xv, "corte_y": c, "discriminante": discriminante, "raices": raices}
