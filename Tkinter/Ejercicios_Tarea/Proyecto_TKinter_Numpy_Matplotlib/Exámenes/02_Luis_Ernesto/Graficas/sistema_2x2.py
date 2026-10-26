# -*- coding: utf-8 -*-
# SOLUCIONADOR DE SISTEMAS 2x2: resuelve dos ecuaciones con x e y.
# NumPy usa álgebra lineal para calcular la solución del sistema.
# Los comentarios explican el propósito de cada sección y los pasos principales.

import tkinter as tk
from tkinter import messagebox
import numpy as np


# Construye la ventana de captura de dos ecuaciones: ax+by=c y dx+ey=f.
def ventana_2x2():

    ventana = tk.Toplevel()
    ventana.title("Sistema de ecuaciones 2x2")
    ventana.geometry("500x500")
    ventana.resizable(False, False)

    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except:
        pass

    titulo = tk.Label(
        ventana,
        text="SISTEMA DE ECUACIONES 2x2",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=20)

    tk.Label(
        ventana,
        text="Ingresa los coeficientes:",
        font=("Arial", 12)
    ).pack(pady=10)

    # Frame agrupa los campos para mantener ordenada la interfaz.
    marco = tk.Frame(ventana)
    marco.pack(pady=10)

    # Primera ecuación
    tk.Label(
        marco,
        text="Ecuación 1:"
    ).grid(row=0, column=0, padx=5, pady=10)

    x1 = tk.Entry(marco, width=8)
    x1.grid(row=0, column=1)

    tk.Label(
        marco,
        text="x +"
    ).grid(row=0, column=2)

    y1 = tk.Entry(marco, width=8)
    y1.grid(row=0, column=3)

    tk.Label(
        marco,
        text="y ="
    ).grid(row=0, column=4)

    r1 = tk.Entry(marco, width=8)
    r1.grid(row=0, column=5)

    # Segunda ecuación
    tk.Label(
        marco,
        text="Ecuación 2:"
    ).grid(row=1, column=0, padx=5, pady=10)

    x2 = tk.Entry(marco, width=8)
    x2.grid(row=1, column=1)

    tk.Label(
        marco,
        text="x +"
    ).grid(row=1, column=2)

    y2 = tk.Entry(marco, width=8)
    y2.grid(row=1, column=3)

    tk.Label(
        marco,
        text="y ="
    ).grid(row=1, column=4)

    r2 = tk.Entry(marco, width=8)
    r2.grid(row=1, column=5)

    resultado = tk.Label(
        ventana,
        text="",
        font=("Arial", 12),
        justify="left"
    )
    resultado.pack(pady=20)

    # Toma los valores introducidos y resuelve el sistema lineal.
    def resolver():

        try:
            a = float(x1.get())
            b = float(y1.get())
            c = float(r1.get())

            d = float(x2.get())
            e = float(y2.get())
            f = float(r2.get())

            # Matriz de coeficientes: cada fila representa una ecuación.
            matriz = np.array([
                [a, b],
                [d, e]
            ])

            # Vector de términos independientes, es decir, los valores a la derecha del igual.
            resultados = np.array([c, f])

            # Comprobar si el sistema tiene solución única
            # Determinante cero indica que no hay una solución única.
            if np.linalg.det(matriz) == 0:
                resultado.config(
                    text="El sistema no tiene una solución única."
                )
                return

            # Resuelve la matriz por métodos de álgebra lineal.
            solucion = np.linalg.solve(
                matriz,
                resultados
            )

            x = solucion[0]
            y = solucion[1]

            resultado.config(
                text=(
                    "RESULTADO\n\n"
                    f"x = {x:.2f}\n"
                    f"y = {y:.2f}"
                )
            )

        # Captura entradas vacías o que no se puedan convertir a número.
        except ValueError:

            messagebox.showerror(
                "Error",
                "Ingresa únicamente valores numéricos."
            )

        # Captura un error matemático al intentar resolver la matriz.
        except np.linalg.LinAlgError:

            messagebox.showerror(
                "Error",
                "No se pudo resolver el sistema."
            )

    boton = tk.Button(
        ventana,
        text="Resolver",
        command=resolver,
        width=20
    )
    boton.pack(pady=10)

    # Presionar Enter ejecuta el boton Resolver
    # Enter ejecuta el botón Resolver.
    ventana.bind("<Return>", lambda evento: boton.invoke())
