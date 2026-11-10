import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# Ventana con la gráfica
def graficar():
    try:
        v1 = float(ent.get() or 0)
        v2 = float(ent1.get() or 0)
        v3 = float(ent2.get() or 0)
        v4 = float(ent3.get() or 0)
        v5 = float(ent4.get() or 0)
        v6 = float(ent5.get() or 0)
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Ingresa solamente números en los seis campos.")
        return

    # Separamos los valores de cada ecuación
    a1, b1, c1 = v1, v2, v3
    a2, b2, c2 = v4, v5, v6

    if a1 == 0 and b1 == 0:
        messagebox.showerror("Ecuación incorrecta", "La ecuación 1 debe tener un coeficiente distinto de cero.")
        return
    if a2 == 0 and b2 == 0:
        messagebox.showerror("Ecuación incorrecta", "La ecuación 2 debe tener un coeficiente distinto de cero.")
        return

    vent2 = tk.Toplevel(ventana)
    vent2.title("Graficador")
    vent2.geometry("700x500")
   
    # Figura
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_ylim(-200, 200)
    ax.set_xlim(-200, 200)

    # Colocar los ejes en el centro
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    # Especificaciones
    ax.grid(True, linestyle="--", alpha=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    x = np.linspace(-200, 200, 400)

    # Graficar ecuación 1: a1x + b1y = c1
    if b1 != 0:
        y1 = (c1 - a1 * x) / b1
        ax.plot(x, y1, color="b", label="Ecuación 1")
    else:
        ax.axvline(c1 / a1, color="b", label="Ecuación 1")

    # Graficar ecuación 2: a2x + b2y = c2
    if b2 != 0:
        y2 = (c2 - a2 * x) / b2
        ax.plot(x, y2, color="r", label="Ecuación 2")
    else:
        ax.axvline(c2 / a2, color="r", label="Ecuación 2")

    # Punto de intersección (solución del sistema)
    det = a1 * b2 - a2 * b1

    if det != 0:
        x_sol = (c1 * b2 - c2 * b1) / det
        y_sol = (a1 * c2 - a2 * c1) / det
        ax.plot(x_sol, y_sol, marker="s", color="r", linestyle="", label="Intersección")
        ax.set_title(f"Solución: x = {x_sol:.2f}, y = {y_sol:.2f}")
    else:
        ax.set_title("No hay una solución única (rectas paralelas o iguales)")

    ax.legend(loc="upper right")

    # Convertir la figura para usarla en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=vent2)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # Liberar la figura al cerrar la ventana
    vent2.protocol("WM_DELETE_WINDOW", lambda: (plt.close(fig), vent2.destroy()))


# Ventana principal
ventana = tk.Tk()
ventana.title("Ecuaciones py")

# Centrar ventana
ancho_pant = ventana.winfo_screenwidth()
alto_pant = ventana.winfo_screenheight()
ancho_vent = 500
alto_vent = 600
posicionx = round(ancho_pant / 2 - ancho_vent / 2)
posiciony = round(alto_pant / 2 - alto_vent / 2) - 30
ventana.geometry(f"{ancho_vent}x{alto_vent}+{posicionx}+{posiciony}")

# Elementos de interfaz
fuente_p = ("Roboto", 30, "bold")
etiqueta = tk.Label(ventana, text="Dimelo comando", font=fuente_p)
etiqueta.pack(pady=10)

boton = tk.Button(
    ventana,
    text="Graficar ecuaciones",
    cursor="hand2",
    command=graficar
)
boton.pack(pady=10)

# Indicación del orden de los valores
etiqueta2 = tk.Label(
    ventana,
    text="Orden: a1, b1, c1, a2, b2, c2\n(a1x + b1y = c1  y  a2x + b2y = c2)"
)
etiqueta2.pack()

ent = tk.Entry(ventana,background="blue")
ent1 = tk.Entry(ventana,background="blue")
ent2 = tk.Entry(ventana,background="blue")
ent3 = tk.Entry(ventana,background="blue")
ent4 = tk.Entry(ventana,background="blue")
ent5 = tk.Entry(ventana,background="blue")

for e in (ent, ent1, ent2, ent3, ent4, ent5):
    e.pack(pady=(10, 20))
    e.bind("<Return>", lambda ev: ev.widget.tk_focusNext().focus_set())

ventana.mainloop()
