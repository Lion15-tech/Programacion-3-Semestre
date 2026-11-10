# -*- coding: utf-8 -*-
# PROGRAMA PRINCIPAL: crea la ventana inicial y conecta cada botón con su módulo.
# Tkinter construye la interfaz; cada archivo importado contiene una sección del proyecto.
# Los comentarios explican el propósito de cada sección y los pasos principales.

import tkinter as tk
from tkinter import messagebox
import primer_grado
import segundo_grado
import sistema
import trigonometria


# Función puente: llama a la ventana definida en el módulo de primer grado.
def abrir_primer_grado():
    primer_grado.ventana_primer_grado()


# Abre el formulario para una ecuación cuadrática.
def abrir_segundo_grado():
    segundo_grado.ventana_segundo_grado()


# Abre el menú que deja elegir un sistema 2x2 o 3x3.
def abrir_sistemas():
    sistema.menu_sistemas()


# Abre el menú con las dos clases de triángulos.
def abrir_trigonometria():
    trigonometria.menu_trigonometria()


# Cierra la aplicación principal.
def salir():
    ventana.destroy()


# Tk() crea la ventana raíz; las demás ventanas se crean como Toplevel.
ventana = tk.Tk()
ventana.title("Gráficas - CECyTEQ")
ventana.geometry("520x520")
ventana.resizable(False, False)

try:
    ventana.iconbitmap("logo_cecyteq.ico")
except Exception:
    pass

# Encabezado
tk.Label(
    ventana,
    text="GRÁFICAS",
    font=("Arial", 24, "bold")
).pack(pady=(18, 5))

tk.Label(
    ventana,
    text="CECyTEQ\nGráficas, sistemas y trigonometría",
    font=("Arial", 12)
).pack(pady=(0, 12))

# Cada botón ejecuta la función indicada en command.
# Opciones visibles en la ventana principal
marco = tk.Frame(ventana)
marco.pack(pady=5)

tk.Button(
    marco, text="Gráfica de primer grado", width=32,
    command=abrir_primer_grado
).pack(pady=5)

tk.Button(
    marco, text="Gráfica de segundo grado", width=32,
    command=abrir_segundo_grado
).pack(pady=5)

tk.Button(
    marco, text="Sistema de ecuaciones", width=32,
    command=abrir_sistemas
).pack(pady=5)

tk.Button(
    marco, text="Trigonometría", width=32,
    command=abrir_trigonometria
).pack(pady=5)

tk.Button(
    marco, text="Salir", width=32,
    command=salir
).pack(pady=5)

# El menú superior ofrece las mismas acciones como alternativa.
# También conservamos las opciones en la barra de menú
barra_menu = tk.Menu(ventana)
menu_graficas = tk.Menu(barra_menu, tearoff=0)
menu_graficas.add_command(label="Gráfica de una ecuación de primer grado", command=abrir_primer_grado)
menu_graficas.add_command(label="Gráfica de una ecuación de segundo grado", command=abrir_segundo_grado)
menu_graficas.add_command(label="Sistema de ecuaciones", command=abrir_sistemas)
menu_graficas.add_command(label="Trigonometría", command=abrir_trigonometria)
menu_graficas.add_separator()
menu_graficas.add_command(label="Salir", command=salir)
barra_menu.add_cascade(label="Opciones", menu=menu_graficas)
ventana.config(menu=barra_menu)

# Enter activa el botón que tenga el foco, cuando corresponda.
# Permite activar con Enter el botón que tenga el foco del teclado.
def activar_con_enter(evento):
    widget = ventana.focus_get()
    if isinstance(widget, tk.Button):
        widget.invoke()

ventana.bind("<Return>", activar_con_enter)

# Inicia el ciclo de eventos: mantiene la interfaz abierta y responde a clics/teclas.
ventana.mainloop()
