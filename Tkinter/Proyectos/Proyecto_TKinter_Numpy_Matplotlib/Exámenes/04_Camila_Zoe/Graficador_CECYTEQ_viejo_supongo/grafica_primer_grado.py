import numpy as np

def calcular_primer_grado(a, b):
    x = np.linspace(-10, 10, 400)
    y = a * x + b
    datos = {
        "pendiente": a,
        "corte_y": b,
        "raiz": None if a == 0 else -b / a
    }
    return x, y, datos
