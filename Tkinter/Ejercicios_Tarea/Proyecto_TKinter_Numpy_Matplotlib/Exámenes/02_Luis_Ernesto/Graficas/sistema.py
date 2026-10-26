# -*- coding: utf-8 -*-
# MENÚ DE SISTEMAS: permite abrir el solucionador de 2 incógnitas o el de 3 incógnitas.
# Este archivo organiza las ventanas; los cálculos están en sistema_2x2.py y sistema_3x3.py.
# Los comentarios explican el propósito de cada sección y los pasos principales.

import tkinter as tk
import sistema_2x2
import sistema_3x3


# Ventana de selección para elegir el tamaño del sistema.
def menu_sistemas():
    ventana = tk.Toplevel()
    ventana.title("Sistema de ecuaciones")
    ventana.geometry("400x300")
    ventana.resizable(False, False)

    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except Exception:
        pass

    tk.Label(
        ventana,
        text="SISTEMA DE ECUACIONES",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        ventana,
        text="Selecciona el tipo de sistema:",
        font=("Arial", 12)
    ).pack(pady=10)

    tk.Button(
        ventana,
        text="Sistema 2x2",
        width=25,
        command=sistema_2x2.ventana_2x2
    ).pack(pady=10)

    tk.Button(
        ventana,
        text="Sistema 3x3",
        width=25,
        command=sistema_3x3.ventana_3x3
    ).pack(pady=10)


# Función auxiliar para abrir directamente el solucionador 2x2.
def ventana_2x2():
    sistema_2x2.ventana_2x2()


# Función auxiliar para abrir directamente el solucionador 3x3.
def ventana_3x3():
    sistema_3x3.ventana_3x3()


def abrir_2x2():
    ventana_2x2()


def abrir_3x3():
    ventana_3x3()
