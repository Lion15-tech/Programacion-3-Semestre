import numpy as np

def calcular_3x3(valores):
    A = np.array([[valores[0], valores[1], valores[2]],
                  [valores[4], valores[5], valores[6]],
                  [valores[8], valores[9], valores[10]]], dtype=float)
    B = np.array([valores[3], valores[7], valores[11]], dtype=float)
    det = np.linalg.det(A)
    if abs(det) > 1e-10:
        solucion = np.linalg.solve(A, B)
        tipo = "Solución única"
    else:
        rango_a = np.linalg.matrix_rank(A)
        rango_ampliada = np.linalg.matrix_rank(np.column_stack((A, B)))
        solucion = None
        tipo = "Sin solución" if rango_ampliada > rango_a else "No tiene solución única"
    return A, B, det, solucion, tipo
