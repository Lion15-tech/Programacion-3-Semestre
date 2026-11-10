# -*- coding: utf-8 -*-
# SOLUCIONADOR DE SISTEMAS 3x3: resuelve tres ecuaciones con x, y y z.
# Las entradas se guardan en una matriz de coeficientes y un vector de resultados.
# Los comentarios explican el propósito de cada sección y los pasos principales.

import tkinter as tk
from tkinter import messagebox
import numpy as np


# Construye el formulario de tres ecuaciones con incógnitas x, y y z.
def ventana_3x3():

    ventana = tk.Toplevel()
    ventana.title("Sistema de ecuaciones 3x3")
    ventana.geometry("650x550")
    ventana.resizable(False, False)

    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except:
        pass

    titulo = tk.Label(
        ventana,
        text="SISTEMA DE ECUACIONES 3x3",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=20)

    tk.Label(
        ventana,
        text="Ingresa los coeficientes de cada ecuación:",
        font=("Arial", 12)
    ).pack(pady=10)

    marco = tk.Frame(ventana)
    marco.pack(pady=10)

    # Los encabezados indican en qué columna va cada coeficiente.
    # Encabezados
    tk.Label(
        marco,
        text="",
        width=12
    ).grid(row=0, column=0)

    tk.Label(
        marco,
        text="x",
        font=("Arial", 11, "bold")
    ).grid(row=0, column=1)

    tk.Label(
        marco,
        text="y",
        font=("Arial", 11, "bold")
    ).grid(row=0, column=3)

    tk.Label(
        marco,
        text="z",
        font=("Arial", 11, "bold")
    ).grid(row=0, column=5)

    tk.Label(
        marco,
        text="Resultado",
        font=("Arial", 11, "bold")
    ).grid(row=0, column=7)

    # La lista entradas conserva referencias a los campos creados en el ciclo.
    # Listas para guardar las entradas
    entradas = []

    # Repite la creación de campos para las tres ecuaciones.
    for fila in range(3):

        tk.Label(
            marco,
            text=f"Ecuación {fila + 1}:"
        ).grid(
            row=fila + 1,
            column=0,
            padx=5,
            pady=10
        )

        fila_entradas = []

        # Coeficiente x
        entrada_x = tk.Entry(
            marco,
            width=8
        )
        entrada_x.grid(
            row=fila + 1,
            column=1
        )

        tk.Label(
            marco,
            text="x +"
        ).grid(
            row=fila + 1,
            column=2
        )

        fila_entradas.append(entrada_x)

        # Coeficiente y
        entrada_y = tk.Entry(
            marco,
            width=8
        )
        entrada_y.grid(
            row=fila + 1,
            column=3
        )

        tk.Label(
            marco,
            text="y +"
        ).grid(
            row=fila + 1,
            column=4
        )

        fila_entradas.append(entrada_y)

        # Coeficiente z
        entrada_z = tk.Entry(
            marco,
            width=8
        )
        entrada_z.grid(
            row=fila + 1,
            column=5
        )

        tk.Label(
            marco,
            text="z ="
        ).grid(
            row=fila + 1,
            column=6
        )

        fila_entradas.append(entrada_z)

        # Resultado
        entrada_resultado = tk.Entry(
            marco,
            width=8
        )
        entrada_resultado.grid(
            row=fila + 1,
            column=7
        )

        fila_entradas.append(entrada_resultado)

        entradas.append(fila_entradas)

    resultado = tk.Label(
        ventana,
        text="",
        font=("Arial", 12),
        justify="left"
    )
    resultado.pack(pady=20)

    # Lee los nueve coeficientes y los tres resultados para formar el sistema.
    def resolver():

        try:

            # Matriz 3x3: cada fila contiene los coeficientes de x, y y z.
            matriz = np.array([
                [
                    float(entradas[0][0].get()),
                    float(entradas[0][1].get()),
                    float(entradas[0][2].get())
                ],
                [
                    float(entradas[1][0].get()),
                    float(entradas[1][1].get()),
                    float(entradas[1][2].get())
                ],
                [
                    float(entradas[2][0].get()),
                    float(entradas[2][1].get()),
                    float(entradas[2][2].get())
                ]
            ])

            # Vector con los términos independientes de las tres ecuaciones.
            resultados = np.array([
                float(entradas[0][3].get()),
                float(entradas[1][3].get()),
                float(entradas[2][3].get())
            ])

            # Si la matriz es singular, el sistema no tiene solución única.
            # Verificar determinante
            if np.linalg.det(matriz) == 0:

                resultado.config(
                    text="El sistema no tiene una solución única."
                )

                return

            # Calcula simultáneamente los valores de x, y y z.
            solucion = np.linalg.solve(
                matriz,
                resultados
            )

            x = solucion[0]
            y = solucion[1]
            z = solucion[2]

            resultado.config(
                text=(
                    "RESULTADO\n\n"
                    f"x = {x:.2f}\n"
                    f"y = {y:.2f}\n"
                    f"z = {z:.2f}"
                )
            )

        # Avisa si algún campo está vacío o contiene texto no numérico.
        except ValueError:

            messagebox.showerror(
                "Error",
                "Ingresa únicamente valores numéricos."
            )

        # Maneja problemas de álgebra lineal al resolver la matriz.
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
