# -*- coding: utf-8 -*-
# ECUACIONES DE PRIMER GRADO: captura m y b para graficar y = mx + b.
# NumPy genera valores de x y Matplotlib dibuja la recta en una ventana de gráfica.
# Los comentarios explican el propósito de cada sección y los pasos principales.

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt


# Crea el formulario para introducir la pendiente m y la intersección b.
def ventana_primer_grado():

    # Abre una ventana secundaria sin cerrar el menú principal.
    ventana = tk.Toplevel()
    ventana.title("Gráfica de ecuación de primer grado")
    ventana.geometry("450x300")
    ventana.resizable(False, False)

    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except:
        pass

    titulo = tk.Label(
        ventana,
        text="Ecuación de primer grado",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=20)

    tk.Label(
        ventana,
        text="Ingresa los valores de y = mx + b"
    ).pack()

    marco = tk.Frame(ventana)
    marco.pack(pady=20)

    tk.Label(marco, text="m:").grid(row=0, column=0, padx=10)
    entrada_m = tk.Entry(marco, width=15)
    entrada_m.grid(row=0, column=1)

    tk.Label(marco, text="b:").grid(row=1, column=0, padx=10)
    entrada_b = tk.Entry(marco, width=15)
    entrada_b.grid(row=1, column=1)

    # Lee los números, calcula y=m*x+b y muestra la recta.
    def graficar():

        try:
            m = float(entrada_m.get())
            b = float(entrada_b.get())

            # Genera 400 puntos de x entre -10 y 10 para que la recta se vea suave.
            x = np.linspace(-10, 10, 400)
            # Evalúa la ecuación en cada valor de x.
            y = m * x + b

            # Prepara una figura de Matplotlib y luego dibuja la curva y los ejes.
            plt.figure(figsize=(7, 5))
            plt.plot(x, y, label=f"y = {m}x + {b}")
            plt.axhline(0)
            plt.axvline(0)
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.title("Ecuación de primer grado")
            plt.grid(True)
            plt.legend()
            plt.show()

        # Evita que el programa se cierre si el usuario escribe letras en vez de números.
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
    # La tecla Enter invoca el mismo botón que se usa con el mouse.
    ventana.bind("<Return>", lambda evento: boton.invoke())
