# -*- coding: utf-8 -*-
# ECUACIONES DE SEGUNDO GRADO: grafica y = ax² + bx + c.
# Se comprueba que a no sea cero, porque si a=0 la expresión deja de ser cuadrática.
# Los comentarios explican el propósito de cada sección y los pasos principales.

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt


# Construye el formulario de los coeficientes a, b y c.
def ventana_segundo_grado():
    ventana = tk.Toplevel()
    ventana.title("Gráfica de ecuación de segundo grado")
    ventana.geometry("450x360")
    ventana.resizable(False, False)

    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except Exception:
        pass

    tk.Label(
        ventana,
        text="Ecuación de segundo grado",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        ventana,
        text="Ingresa los valores de y = ax² + bx + c"
    ).pack()

    marco = tk.Frame(ventana)
    marco.pack(pady=20)

    tk.Label(marco, text="a:").grid(row=0, column=0, padx=10, pady=5)
    entrada_a = tk.Entry(marco, width=15)
    entrada_a.grid(row=0, column=1)

    tk.Label(marco, text="b:").grid(row=1, column=0, padx=10, pady=5)
    entrada_b = tk.Entry(marco, width=15)
    entrada_b.grid(row=1, column=1)

    tk.Label(marco, text="c:").grid(row=2, column=0, padx=10, pady=5)
    entrada_c = tk.Entry(marco, width=15)
    entrada_c.grid(row=2, column=1)

    # Valida los coeficientes y calcula la función cuadrática.
    def graficar():
        try:
            a = float(entrada_a.get())
            b = float(entrada_b.get())
            c = float(entrada_c.get())

            # Si a es cero, no existe término x² y no es una ecuación de segundo grado.
            if a == 0:
                messagebox.showerror(
                    "Error",
                    "El valor de 'a' no puede ser 0 en una ecuación de segundo grado."
                )
                return

            # Crea valores de x para dibujar una curva continua.
            x = np.linspace(-10, 10, 400)
            # Calcula y para cada x usando la fórmula cuadrática.
            y = a * x**2 + b * x + c

            plt.figure(figsize=(7, 5))
            plt.plot(x, y, label=f"y = {a}x² + {b}x + {c}")
            plt.axhline(0)
            plt.axvline(0)
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.title("Ecuación de segundo grado")
            plt.grid(True)
            plt.legend()
            plt.show()

        # Muestra un mensaje si alguno de los campos no contiene un número válido.
        except ValueError:
            messagebox.showerror(
                "Error",
                "Ingresa valores numéricos válidos."
            )

    boton = tk.Button(
        ventana,
        text="Graficar",
        command=graficar,
        width=20
    )
    boton.pack(pady=10)

    # Presionar Enter ejecuta el boton Graficar
    # Enter ejecuta la acción Graficar.
    ventana.bind("<Return>", lambda evento: boton.invoke())
