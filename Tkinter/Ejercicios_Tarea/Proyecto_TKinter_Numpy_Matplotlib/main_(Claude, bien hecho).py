import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


### Paleta de Colores ###
COLOR_FONDO_PRINCIPAL = "#BCF6BC"  # Verde menta muy claro para el fondo
COLOR_TEXTO_TITULO    = "#1E4620"  # Verde bosque oscuro para los títulos
COLOR_BOTON_NORMAL    = "#2E7D32"  # Verde estándar para los botones
COLOR_BOTON_HOVER     = "#1B5E20"  # Verde más oscuro cuando clckeas con el mouse
COLOR_TEXTO_BOTON     = "#FFFFFF"  # Texto blanco para que contraste con los botones

### Fuentes ###
fuente_titulo = ("Impact", 22)
fuente_botones = ("Helvetica", 11, "bold")

class MenuPrincipal:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gráficas y Ecuaciones - CECYTEQ")
        self.ventana.geometry("480x450")
        self.ventana.config(bg=COLOR_FONDO_PRINCIPAL)

        #### CONFIGURACIÓN DEL ICONO ####
        self.carpeta_proyecto = os.path.dirname(__file__)
        self.ruta_icono = os.path.join(self.carpeta_proyecto, "logo_cecyteq.png")

        try:
            self.icono = tk.PhotoImage(file=self.ruta_icono)
            self.ventana.iconphoto(False, self.icono)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        # Configuración de cuadrícula (Grid)
        self.ventana.rowconfigure(0, weight=1)
        self.ventana.rowconfigure(1, weight=1)
        self.ventana.rowconfigure(2, weight=1)

        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)

        
        tk.Label(self.ventana,
                text="Gráficas \ny \nEcuaciones", 
                font=fuente_titulo,
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL,
                relief="flat",
                padx=20).grid(row=0, column=0, rowspan=3, sticky="nsew") 

        btn_primer = tk.Button(self.ventana,
                text="Gráfica una ecuación \nde primer grado",
                font=fuente_botones,
                bg=COLOR_BOTON_NORMAL,
                fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2",
                bd=0,
                pady=10)
        btn_primer.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        btn_primer.config(command=self.grafica_primer_grado)

        btn_segundo = tk.Button(self.ventana,
                text="Gráfica una ecuación \nde segundo grado",
                font=fuente_botones,
                bg=COLOR_BOTON_NORMAL,
                fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2",
                bd=0,
                pady=10)
        btn_segundo.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        btn_segundo.config(command=self.grafica_segundo_grado)

        btn_sistemas = tk.Button(self.ventana,
                text="Sistemas de ecuaciones",
                font=fuente_botones,
                bg=COLOR_BOTON_NORMAL,
                fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2",
                bd=0,
                pady=10)
        btn_sistemas.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        btn_sistemas.config(command=self.ventana_sistema_ecuaciones)


    #### UTILIDADES PARA PARES ORDENADOS ####
    @staticmethod
    def _num(n):
        """Formatea un número sin ceros sobrantes (2.00 -> 2, -0.00 -> 0)."""
        s = f"{n:.2f}".rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s

    def _texto_poli(self, terminos):
        """Arma 'y = ...' a partir de [(coeficiente, 'x²'), (coeficiente, 'x'), (coeficiente, '')]."""
        texto = ""
        for coef, var in terminos:
            if np.isclose(coef, 0):
                continue
            magnitud = abs(coef)
            if var != "" and np.isclose(magnitud, 1):
                cuerpo = var
            else:
                cuerpo = self._num(magnitud) + var
            if texto == "":
                texto = ("-" if coef < 0 else "") + cuerpo
            else:
                texto += f" {'-' if coef < 0 else '+'} {cuerpo}"
        return "y = " + (texto if texto else "0")

    def _fila_punto(self, padre, etiqueta, x_defecto, y_defecto):
        """Crea una fila '(  x  ,  y  )' y devuelve sus dos Entry."""
        fila = tk.Frame(padre, bg=COLOR_FONDO_PRINCIPAL)
        fila.pack(anchor="w", pady=4)

        tk.Label(fila, text=etiqueta, font=("Helvetica", 10, "bold"),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL,
                width=3, anchor="w").pack(side="left")
        tk.Label(fila, text="(", font=("Helvetica", 12),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(side="left")

        entry_x = tk.Entry(fila, font=("Helvetica", 11), width=5, justify="center")
        entry_x.pack(side="left")
        entry_x.insert(0, x_defecto)

        tk.Label(fila, text=",", font=("Helvetica", 12),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(side="left")

        entry_y = tk.Entry(fila, font=("Helvetica", 11), width=5, justify="center")
        entry_y.pack(side="left")
        entry_y.insert(0, y_defecto)

        tk.Label(fila, text=")", font=("Helvetica", 12),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(side="left")
        return entry_x, entry_y

    def _leer_puntos(self, pares_entries):
        """Lee una lista de (entry_x, entry_y) y devuelve [(x, y), ...] o None si hay error."""
        try:
            return [(float(ex.get().replace(",", ".")), float(ey.get().replace(",", ".")))
                    for ex, ey in pares_entries]
        except ValueError:
            messagebox.showerror("Error de datos",
                                "Por favor, introduce números válidos en todas las coordenadas.")
            return None

    def _marcar_puntos(self, ax, puntos, nombres):
        """Dibuja los pares ordenados ingresados con su etiqueta de coordenadas."""
        for i, ((px, py), nombre) in enumerate(zip(puntos, nombres)):
            ax.plot(px, py, 'o', color="#1565C0", markersize=8, zorder=5,
                    label="Puntos ingresados" if i == 0 else None)
            ax.annotate(f"{nombre}({self._num(px)}, {self._num(py)})", (px, py),
                        textcoords="offset points", xytext=(7, 7), fontsize=8, color="#1565C0")


    #### VENTANAS HIJAS ####
    def grafica_primer_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Primer Grado: recta por 2 puntos")
        ventana_hija.geometry("750x520")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)

        frame_izquierdo = tk.Frame(ventana_hija,
                                bg=COLOR_FONDO_PRINCIPAL,
                                padx=15,
                                pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo,
                text="Ecuación Lineal",
                font=("Impact", 16),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo,
                text="Ingresa 2 pares ordenados (x, y)",
                font=("Helvetica", 11, "italic"),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        frame_puntos = tk.Frame(frame_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        frame_puntos.pack(anchor="w", pady=(15, 0))

        # Valores por defecto: (0, -4) y (3, 2)  ->  y = 2x - 4
        self.p1_x, self.p1_y = self._fila_punto(frame_puntos, "A", "0", "-4")
        self.p2_x, self.p2_y = self._fila_punto(frame_puntos, "B", "3", "2")

        btn_calcular = tk.Button(frame_izquierdo,
                                text="Graficar",
                                font=fuente_botones,
                                bg=COLOR_BOTON_NORMAL,
                                fg=COLOR_TEXTO_BOTON,
                                activebackground=COLOR_BOTON_HOVER,
                                activeforeground=COLOR_TEXTO_BOTON,
                                cursor="hand2",
                                bd=0, padx=10, pady=5,
                                command=self.procesar_primer_grado)
        btn_calcular.pack(pady=20, fill="x")

        self.lbl_valores_clave_1ro = tk.Label(frame_izquierdo,
                                            text="Valores clave:\n-\n-",
                                            font=("Helvetica", 10),
                                            justify="left",
                                            fg=COLOR_TEXTO_TITULO,
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_1ro.pack(anchor="w", pady=10)

        self.frame_grafica_1ro = tk.Frame(ventana_hija,
                                        bg="white",
                                        bd=1,
                                        relief="sunken")
        self.frame_grafica_1ro.pack(side="right", expand=True, fill="both", padx=15, pady=15)


    def procesar_primer_grado(self):
        puntos = self._leer_puntos([(self.p1_x, self.p1_y), (self.p2_x, self.p2_y)])
        if puntos is None:
            return
        (x1, y1), (x2, y2) = puntos

        if x1 == x2 and y1 == y2:
            messagebox.showerror("Error matemático",
                                "Los dos puntos son iguales. Una recta necesita dos puntos distintos.")
            return

        n = self._num
        vertical = (x1 == x2)

        if vertical:
            # Recta vertical: x = k (no es función, no tiene m ni b)
            m = b = None
            raiz = x1
            texto_valores = (
                f"--- VALORES CLAVE ---\n"
                f"Recta vertical: x = {n(x1)}\n"
                f"Pendiente (m): indefinida\n"
                f"Intersección Y: " + ("(0, y) para todo y (es el eje Y)" if x1 == 0 else "No tiene") + "\n"
                f"Intersección X: ({n(x1)}, 0)"
            )
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            if not np.isclose(m, 0):
                raiz = -b / m
                texto_raiz = f"Raíz (Intersección X): ({n(raiz)}, 0)"
            else:
                raiz = None
                texto_raiz = ("Raíz (Intersección X): todo el eje X (la recta es el eje X)"
                            if np.isclose(b, 0) else
                            "Raíz (Intersección X): No tiene (paralela al eje X)")
            texto_valores = (
                f"--- VALORES CLAVE ---\n"
                f"{self._texto_poli([(m, 'x'), (b, '')])}\n"
                f"Pendiente (m): {n(m)}\n"
                f"Ordenada al origen (b): {n(b)}\n"
                f"Intersección Y: (0, {n(b)})\n"
                f"{texto_raiz}"
            )
        self.lbl_valores_clave_1ro.config(text=texto_valores)

        for widget in self.frame_grafica_1ro.winfo_children():
            widget.destroy()

        # Rango de la gráfica: que se vean los puntos, el origen y las intersecciones
        refs_x = [x1, x2, 0]
        refs_y = [y1, y2, 0]
        if raiz is not None:
            refs_x.append(raiz)
        if not vertical:
            refs_y.append(b)
        pad_x = max(2, 0.3 * (max(refs_x) - min(refs_x)))
        pad_y = max(2, 0.3 * (max(refs_y) - min(refs_y)))
        x_min, x_max = min(refs_x) - pad_x, max(refs_x) + pad_x

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        if vertical:
            ax.axvline(x1, color="#2E7D32", linewidth=2, label=f"x = {n(x1)}")
            ax.set_ylim(min(refs_y) - pad_y, max(refs_y) + pad_y)
        else:
            x = np.linspace(x_min, x_max, 200)
            ax.plot(x, m * x + b, color="#2E7D32", linewidth=2,
                    label=self._texto_poli([(m, 'x'), (b, '')]))
            ax.plot(0, b, 'go', label=f"Int. Y (0, {n(b)})")                  # Punto intersección Y
            if raiz is not None:
                ax.plot(raiz, 0, 'ro', label=f"Raíz ({n(raiz)}, 0)")          # Punto de la raíz
        ax.set_xlim(x_min, x_max)

        self._marcar_puntos(ax, [(x1, y1), (x2, y2)], ["A", "B"])

        ax.axhline(0, color='black', linewidth=1) # Eje X
        ax.axvline(0, color='black', linewidth=1) # Eje Y
        ax.grid(True, linestyle='--', alpha=0.6)   # Cuadrícula de fondo
        ax.set_title("Gráfica de la Ecuación Lineal", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.legend(fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_1ro)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        plt.close(fig)



    def grafica_segundo_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Segundo Grado: parábola por 3 puntos")
        ventana_hija.geometry("750x580")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)

        frame_izquierdo = tk.Frame(ventana_hija,
                                bg=COLOR_FONDO_PRINCIPAL,
                                padx=15,
                                pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo,
                text="Ecuación Cuadrática",
                font=("Impact", 16),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo,
                text="Ingresa 3 pares ordenados (x, y)\ncon valores de X distintos",
                font=("Helvetica", 11, "italic"),
                justify="center",
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        frame_puntos = tk.Frame(frame_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        frame_puntos.pack(anchor="w", pady=(15, 0))

        # Valores por defecto: (-1, 0), (0, -3), (3, 0)  ->  y = x² - 2x - 3
        self.q_p1_x, self.q_p1_y = self._fila_punto(frame_puntos, "A", "-1", "0")
        self.q_p2_x, self.q_p2_y = self._fila_punto(frame_puntos, "B", "0", "-3")
        self.q_p3_x, self.q_p3_y = self._fila_punto(frame_puntos, "C", "3", "0")

        btn_calcular = tk.Button(frame_izquierdo,
                                text="Graficar",
                                font=fuente_botones,
                                bg=COLOR_BOTON_NORMAL,
                                fg=COLOR_TEXTO_BOTON,
                                activebackground=COLOR_BOTON_HOVER,
                                activeforeground=COLOR_TEXTO_BOTON,
                                cursor="hand2",
                                bd=0, padx=10, pady=5,
                                command=self.procesar_segundo_grado)
        btn_calcular.pack(pady=15, fill="x")

        self.lbl_valores_clave_2do = tk.Label(frame_izquierdo,
                                            text="Valores clave:\n-\n-",
                                            font=("Helvetica", 10),
                                            justify="left",
                                            fg=COLOR_TEXTO_TITULO,
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_2do.pack(anchor="w", pady=10)

        self.frame_grafica_2do = tk.Frame(ventana_hija,
                                        bg="white",
                                        bd=1,
                                        relief="sunken")
        self.frame_grafica_2do.pack(side="right",
                                    expand=True,
                                    fill="both",
                                    padx=15, pady=15)


    def procesar_segundo_grado(self):
        puntos = self._leer_puntos([(self.q_p1_x, self.q_p1_y),
                                    (self.q_p2_x, self.q_p2_y),
                                    (self.q_p3_x, self.q_p3_y)])
        if puntos is None:
            return

        xs = [p[0] for p in puntos]
        ys = [p[1] for p in puntos]

        if len(set(xs)) < 3:
            messagebox.showerror("Error matemático",
                                "Los 3 puntos deben tener valores de X distintos.\n"
                                "(Si dos puntos comparten X, no se puede formar y = ax² + bx + c)")
            return

        # Cada punto cumple y = a·x² + b·x + c  ->  sistema 3x3 para encontrar a, b, c
        A = np.array([[x**2, x, 1.0] for x in xs])
        a, b, c = np.linalg.solve(A, np.array(ys))

        if np.isclose(a, 0, atol=1e-9):
            messagebox.showerror("Error matemático",
                                "Los 3 puntos están alineados: forman una recta, no una parábola.\n"
                                "Usa la opción de ecuación de primer grado, o cambia algún punto.")
            return

        n = self._num
        discriminante = b**2 - 4*a*c

        vx = -b / (2 * a)
        vy = a * (vx**2) + b * vx + c

        if np.isclose(discriminante, 0):
            x1 = -b / (2 * a)
            texto_raices = f"Raíz (Real única / repetida):\n  X = {n(x1)}"
            puntos_raices = [(x1, 0)]
        elif discriminante > 0:
            x1 = (-b + np.sqrt(discriminante)) / (2 * a)
            x2 = (-b - np.sqrt(discriminante)) / (2 * a)
            texto_raices = f"Raíces (Reales distintas):\n  X1 = {n(x1)}\n  X2 = {n(x2)}"
            puntos_raices = [(x1, 0), (x2, 0)]
        else:
            parte_real = -b / (2 * a)
            parte_imag = np.sqrt(abs(discriminante)) / (2 * abs(a))
            texto_raices = (f"Raíces (Complejas/Imaginarias):\n"
                            f"  X1 = {n(parte_real)} + {n(parte_imag)}i\n"
                            f"  X2 = {n(parte_real)} - {n(parte_imag)}i")
            puntos_raices = [] # No se cruza el eje X real

        ecuacion = self._texto_poli([(a, 'x²'), (b, 'x'), (c, '')])

        texto_valores = (
            f"--- VALORES CLAVE ---\n"
            f"{ecuacion}\n"
            f"a = {n(a)},  b = {n(b)},  c = {n(c)}\n"
            f"Discriminante (Δ): {n(discriminante)}\n"
            f"Vértice (H, K): ({n(vx)}, {n(vy)})\n"
            f"Intersección Y: (0, {n(c)})\n"
            f"{texto_raices}"
        )
        self.lbl_valores_clave_2do.config(text=texto_valores)
        for widget in self.frame_grafica_2do.winfo_children():
            widget.destroy()

        # Rango de la gráfica: que se vean los puntos, el vértice, el origen y las raíces
        refs_x = xs + [vx, 0] + [p[0] for p in puntos_raices]
        pad_x = max(2, 0.3 * (max(refs_x) - min(refs_x)))
        x = np.linspace(min(refs_x) - pad_x, max(refs_x) + pad_x, 300)
        y = a * (x**2) + b * x + c

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(x, y, color="#2E7D32", linewidth=2, label=ecuacion)

        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_title("Gráfica de la Ecuación Cuadrática", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")

        self._marcar_puntos(ax, puntos, ["A", "B", "C"])

        ax.plot(vx, vy, 'D', color="#8E24AA", label=f"Vértice ({n(vx)}, {n(vy)})")
        ax.plot(0, c, 'go', label=f"Int. Y (0, {n(c)})")

        for i, (px, py) in enumerate(puntos_raices):
            ax.plot(px, py, 'ro', label="Raíces (Int. X)" if i == 0 else None)

        ax.legend(fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_2do)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        plt.close(fig)



    def ventana_sistema_ecuaciones(self):
        ventana_sistemas = tk.Toplevel(self.ventana)
        ventana_sistemas.title("Sistemas de Ecuaciones")
        ventana_sistemas.geometry("400x300")
        ventana_sistemas.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_sistemas.iconphoto(False, self.icono)

        tk.Label(ventana_sistemas, 
                text="Selecciona el Tipo de Sistema", 
                font=("Impact", 18),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=25)

        tk.Button(ventana_sistemas,
                text="Sistemas de 2x2",
                font=fuente_botones,
                bg=COLOR_BOTON_NORMAL,
                fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2",
                bd=0,
                pady=10,
                command=self.sistema_2x2).pack(pady=12, fill="x", padx=50)

        tk.Button(ventana_sistemas,
                text="Sistemas de 3x3",
                font=fuente_botones,
                bg=COLOR_BOTON_NORMAL,
                fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2",
                bd=0,
                pady=10,
                command=self.sistema_3x3).pack(pady=12, fill="x", padx=50)

    def sistema_2x2(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 2x2")
        ventana_hija.geometry("800x550")  # Espacio suficiente para entradas y gráfica
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        frame_izquierdo = tk.Frame(ventana_hija, bg=COLOR_FONDO_PRINCIPAL, padx=15, pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo, text="Sistema de 2x2", font=("Impact", 16), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo, text="ax + by = c", font=("Helvetica", 11, "italic"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        frame_inputs = tk.Frame(frame_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, 
                text="Ecuación 1: ", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).grid(row=0, column=0, pady=5)
        self.entry_a1 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_a1.grid(row=0, column=1); self.entry_a1.insert(0, "1")
        tk.Label(frame_inputs, text="x + ", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=2)
        self.entry_b1 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_b1.grid(row=0, column=3); self.entry_b1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="y = ", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=4)
        self.entry_c1 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_c1.grid(row=0, column=5); self.entry_c1.insert(0, "5")

        tk.Label(frame_inputs, 
                text="Ecuación 2: ", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).grid(row=1, column=0, pady=5)
        self.entry_a2 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_a2.grid(row=1, column=1); self.entry_a2.insert(0, "1")
        tk.Label(frame_inputs, 
                text="x + ", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=1, column=2)
        self.entry_b2 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_b2.grid(row=1, column=3); self.entry_b2.insert(0, "-1") # Se resuelve ax + by = c; para restar, escribe un número negativo
        tk.Label(frame_inputs, 
                text="y = ", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=1, column=4)
        self.entry_c2 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_c2.grid(row=1, column=5); self.entry_c2.insert(0, "1")

        btn_calcular = tk.Button(frame_izquierdo, 
                                text="Resolver y Graficar", 
                                font=fuente_botones, 
                                bg=COLOR_BOTON_NORMAL, 
                                fg=COLOR_TEXTO_BOTON, 
                                activebackground=COLOR_BOTON_HOVER, 
                                activeforeground=COLOR_TEXTO_BOTON, 
                                cursor="hand2", 
                                bd=0, padx=10, pady=5, 
                                command=self.procesar_sistema_2x2)
        btn_calcular.pack(pady=15, fill="x")

        self.lbl_valores_clave_sist = tk.Label(frame_izquierdo, 
                                            text="Solución del sistema:\n-\n-", 
                                            font=("Helvetica", 10), 
                                            justify="left", 
                                            fg=COLOR_TEXTO_TITULO, 
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_sist.pack(anchor="w", pady=10)

        self.frame_grafica_sist = tk.Frame(ventana_hija,
                                        bg="white", 
                                        bd=1, 
                                        relief="sunken")
        self.frame_grafica_sist.pack(side="right", 
                                    expand=True, 
                                    fill="both", 
                                    padx=15, 
                                    pady=15)


    def procesar_sistema_2x2(self):
        try:
            a1 = float(self.entry_a1.get())
            b1 = float(self.entry_b1.get())
            c1 = float(self.entry_c1.get())
            
            a2 = float(self.entry_a2.get())
            b2 = float(self.entry_b2.get())
            c2 = float(self.entry_c2.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en todos los coeficientes.")
            return

        if (a1 == 0 and b1 == 0) or (a2 == 0 and b2 == 0):
            messagebox.showerror("Error matemático",
                                "En cada ecuación, 'a' y 'b' no pueden ser 0 a la vez (no sería una recta).")
            return

        A = np.array([[a1, b1], 
                    [a2, b2]])
        B = np.array([c1, c2])

        determinante = np.linalg.det(A)

        if np.isclose(determinante, 0):
            self.lbl_valores_clave_sist.config(text="--- VALORES CLAVE ---\nEl sistema NO tiene solución única.\n(Rectas paralelas o coincidentes)")
            solucion_existe = False
        else:
            sol_x, sol_y = np.linalg.solve(A, B)
            texto_valores = (
                f"--- VALORES CLAVE ---\n"
                f"Determinante: {determinante:.2f}\n"
                f"Punto de Intersección (Solución):\n"
                f"  X = {sol_x:.2f}\n"
                f"  Y = {sol_y:.2f}"
            )
            self.lbl_valores_clave_sist.config(text=texto_valores)
            solucion_existe = True

        for widget in self.frame_grafica_sist.winfo_children():
            widget.destroy()

        centro_x = sol_x if solucion_existe else 0
        x_vals = np.linspace(centro_x - 10, centro_x + 10, 100)

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        
        if b1 != 0:
            y_vals1 = (c1 - a1 * x_vals) / b1
            ax.plot(x_vals, y_vals1, color="#1B5E20", linewidth=2, label=f"{self._num(a1)}x + {self._num(b1)}y = {self._num(c1)}")
        else:
            ax.axvline(c1 / a1, color="#1B5E20", linewidth=2, linestyle="--", label=f"{self._num(a1)}x = {self._num(c1)}")

        if b2 != 0:
            y_vals2 = (c2 - a2 * x_vals) / b2
            ax.plot(x_vals, y_vals2, color="#E65100", linewidth=2, label=f"{self._num(a2)}x + {self._num(b2)}y = {self._num(c2)}")
        else:
            ax.axvline(c2 / a2, color="#E65100", linewidth=2, linestyle="--", label=f"{self._num(a2)}x = {self._num(c2)}")

        if solucion_existe:
            ax.plot(sol_x, sol_y, 'ro', markersize=8, label=f"Intersección ({sol_x:.1f}, {sol_y:.1f})")

        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_title("Intersección de Rectas (Sistema 2x2)", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_sist)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        plt.close(fig)



    def sistema_3x3(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 3x3")
        ventana_hija.geometry("800x550")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        frame_izquierdo = tk.Frame(ventana_hija, 
                                bg=COLOR_FONDO_PRINCIPAL, 
                                padx=15, 
                                pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo, 
                text="Sistema de 3x3", 
                font=("Impact", 16), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo, 
                text="ax + by + cz = d", 
                font=("Helvetica", 11, "italic"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        frame_inputs = tk.Frame(frame_izquierdo, 
                                bg=COLOR_FONDO_PRINCIPAL)
        frame_inputs.pack(pady=10)

        ## Ecuación 1 ##
        tk.Label(frame_inputs, 
                text="Eq 1: ", 
                font=("Helvetica", 9, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).grid(row=0, column=0, pady=5)
        self.entry_a3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_a3_1.grid(row=0, column=1); self.entry_a3_1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="x+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=2)
        self.entry_b3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_b3_1.grid(row=0, column=3); self.entry_b3_1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="y+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=4)
        self.entry_c3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_c3_1.grid(row=0, column=5); self.entry_c3_1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="z=", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=6)
        self.entry_d3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_d3_1.grid(row=0, column=7); self.entry_d3_1.insert(0, "6")

        ## Ecuación 2 ##
        tk.Label(frame_inputs, 
                text="Eq 2: ", 
                font=("Helvetica", 9, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).grid(row=1, column=0, pady=5)
        self.entry_a3_2 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_a3_2.grid(row=1, column=1); self.entry_a3_2.insert(0, "0")
        tk.Label(frame_inputs, 
                text="x+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=1, column=2)
        self.entry_b3_2 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_b3_2.grid(row=1, column=3); self.entry_b3_2.insert(0, "2")
        tk.Label(frame_inputs, 
                text="y+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=1, column=4)
        self.entry_c3_2 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_c3_2.grid(row=1, column=5); self.entry_c3_2.insert(0, "5")
        tk.Label(frame_inputs, 
                text="z=", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=1, column=6)
        self.entry_d3_2 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_d3_2.grid(row=1, column=7); self.entry_d3_2.insert(0, "-4")

        ## Ecuación 3 ##
        tk.Label(frame_inputs,
                text="Eq 3: ", 
                font=("Helvetica", 9, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).grid(row=2, column=0, pady=5)
        self.entry_a3_3 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_a3_3.grid(row=2, column=1); self.entry_a3_3.insert(0, "2")
        tk.Label(frame_inputs, 
                text="x+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=2, column=2)
        self.entry_b3_3 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_b3_3.grid(row=2, column=3); self.entry_b3_3.insert(0, "5")
        tk.Label(frame_inputs, 
                text="y+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=2, column=4)
        self.entry_c3_3 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_c3_3.grid(row=2, column=5); self.entry_c3_3.insert(0, "-1")
        tk.Label(frame_inputs, 
                text="z=", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=2, column=6)
        self.entry_d3_3 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_d3_3.grid(row=2, column=7); self.entry_d3_3.insert(0, "27")

        btn_calcular = tk.Button(frame_izquierdo, 
                                text="Resolver Sistema", 
                                font=fuente_botones, 
                                bg=COLOR_BOTON_NORMAL, 
                                fg=COLOR_TEXTO_BOTON, 
                                activebackground=COLOR_BOTON_HOVER, 
                                activeforeground=COLOR_TEXTO_BOTON, 
                                cursor="hand2", 
                                bd=0, padx=10, pady=5, 
                                command=self.procesar_sistema_3x3)
        btn_calcular.pack(pady=15, fill="x")

        self.lbl_valores_clave_3x3 = tk.Label(frame_izquierdo, 
                                            text="Solución del sistema:\n-\n-", 
                                            font=("Helvetica", 10), 
                                            justify="left", 
                                            fg=COLOR_TEXTO_TITULO, 
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_3x3.pack(anchor="w", pady=10)

        self.frame_grafica_3x3 = tk.Frame(ventana_hija, 
                                        bg="white", 
                                        bd=1, 
                                        relief="sunken")
        self.frame_grafica_3x3.pack(side="right", 
                                    expand=True, 
                                    fill="both", 
                                    padx=15, 
                                    pady=15)


    def _dibujar_plano(self, ax, a, b, c, d, x_rango, y_rango, z_rango, color):
        """Dibuja el plano ax + by + cz = d. Si c = 0 es un plano vertical y se despeja y (o x)."""
        if c != 0:
            X, Y = np.meshgrid(x_rango, y_rango)
            Z = (d - a * X - b * Y) / c
        elif b != 0:
            X, Z = np.meshgrid(x_rango, z_rango)
            Y = (d - a * X) / b
        else:
            Y, Z = np.meshgrid(y_rango, z_rango)
            X = np.full_like(Y, d / a)
        ax.plot_surface(X, Y, Z, alpha=0.5, color=color)


    def procesar_sistema_3x3(self):
        try:
            # 1. Recuperar los coeficientes de las 3 ecuaciones
            a1, b1, c1, d1 = float(self.entry_a3_1.get()), float(self.entry_b3_1.get()), float(self.entry_c3_1.get()), float(self.entry_d3_1.get())
            a2, b2, c2, d2 = float(self.entry_a3_2.get()), float(self.entry_b3_2.get()), float(self.entry_c3_2.get()), float(self.entry_d3_2.get())
            a3, b3, c3, d3 = float(self.entry_a3_3.get()), float(self.entry_b3_3.get()), float(self.entry_c3_3.get()), float(self.entry_d3_3.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en todos los coeficientes.")
            return

        if any(a == 0 and b == 0 and c == 0 for a, b, c in ((a1, b1, c1), (a2, b2, c2), (a3, b3, c3))):
            messagebox.showerror("Error matemático",
                                "En cada ecuación, 'a', 'b' y 'c' no pueden ser 0 a la vez (no sería un plano).")
            return

        # 2. Configurar matrices con NumPy
        A = np.array([[a1, b1, c1],
                    [a2, b2, c2],
                    [a3, b3, c3]])
        B = np.array([d1, d2, d3])

        determinante = np.linalg.det(A)

        # Verificar si hay solución única
        if np.isclose(determinante, 0):
            self.lbl_valores_clave_3x3.config(text="--- VALORES CLAVE ---\nEl sistema NO tiene solución única.\n(Planos paralelos o infinitas intersecciones)")
            solucion_existe = False
        else:
            sol_x, sol_y, sol_z = np.linalg.solve(A, B)
            texto_valores = (
                f"--- VALORES CLAVE ---\n"
                f"Determinante: {determinante:.2f}\n"
                f"Solución del Sistema:\n"
                f"  X = {sol_x:.2f}\n"
                f"  Y = {sol_y:.2f}\n"
                f"  Z = {sol_z:.2f}"
            )
            self.lbl_valores_clave_3x3.config(text=texto_valores)
            solucion_existe = True

        # 3. Limpiar contenedor gráfico
        for widget in self.frame_grafica_3x3.winfo_children():
            widget.destroy()

        # 4. Crear la Gráfica 3D usando Matplotlib
        # Creamos una cuadrícula de puntos en los ejes X e Y usando NumPy
        centro_x = sol_x if solucion_existe else 0
        centro_y = sol_y if solucion_existe else 0
        centro_z = sol_z if solucion_existe else 0

        x_rango = np.linspace(centro_x - 5, centro_x + 5, 20)
        y_rango = np.linspace(centro_y - 5, centro_y + 5, 20)
        z_rango = np.linspace(centro_z - 5, centro_z + 5, 20)

        # Inicializamos la figura de Matplotlib indicando explícitamente que es proyección 3D
        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        # Dibujamos los planos con transparencias (alpha) para que se vea dónde se cruzan
        self._dibujar_plano(ax, a1, b1, c1, d1, x_rango, y_rango, z_rango, 'green')
        self._dibujar_plano(ax, a2, b2, c2, d2, x_rango, y_rango, z_rango, 'orange')
        self._dibujar_plano(ax, a3, b3, c3, d3, x_rango, y_rango, z_rango, 'blue')

        # Siempre se enmarca la vista (con o sin solución) para que no se estire la escala
        ax.set_xlim(centro_x - 5, centro_x + 5)
        ax.set_ylim(centro_y - 5, centro_y + 5)
        ax.set_zlim(centro_z - 5, centro_z + 5)

        # Si hay solución, marcamos el punto exacto de intersección en el espacio con una esfera roja
        if solucion_existe:
            ax.scatter(sol_x, sol_y, sol_z, color='red', s=50, depthshade=False, label=f"Solución ({sol_x:.1f}, {sol_y:.1f}, {sol_z:.1f})")
            ax.legend(fontsize=8)

        # Configurar etiquetas espaciales
        ax.set_title("Intersección de Planos 3D", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.set_zlabel("Eje Z")
        
        # 5. Incrustar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_3x3)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        plt.close(fig)


### Ejecutar la aplicación ###
if __name__ == "__main__":
    raiz = tk.Tk()
    app = MenuPrincipal(raiz)
    raiz.mainloop()
