import numpy as np

def calcular_2x2(a1, b1, c1, a2, b2, c2):
    A = np.array([[a1, b1], [a2, b2]], dtype=float)
    B = np.array([c1, c2], dtype=float)
    det = np.linalg.det(A)
    if abs(det) > 1e-10:
        solucion = np.linalg.solve(A, B)
        tipo = "Solución única"
    else:
        rango_a = np.linalg.matrix_rank(A)
        rango_ampliada = np.linalg.matrix_rank(np.column_stack((A, B)))
        solucion = None
        tipo = "Sin solución" if rango_ampliada > rango_a else "Infinitas soluciones"
    return A, B, det, solucion, tipo
