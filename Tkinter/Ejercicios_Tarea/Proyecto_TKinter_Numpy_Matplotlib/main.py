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


    #### VENTANAS HIJAS ####
    def grafica_primer_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Primer Grado: y = mx + b")
        ventana_hija.geometry("750x500")  # La hicimos más ancha para que quepa la gráfica al lado
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
                text="y = mx + b", 
                font=("Helvetica", 12, "italic"), 
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)


        tk.Label(frame_izquierdo, 
                text="Valor de m (Pendiente):", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        
        self.entry_m = tk.Entry(frame_izquierdo, 
                                font=("Helvetica", 11), 
                                width=10)
        self.entry_m.pack(anchor="w", pady=2)
        self.entry_m.insert(0, "2") # Valor por defecto para que no inicie vacío


        tk.Label(frame_izquierdo, 
                text="Valor de b (Intersección Y):", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        
        self.entry_b = tk.Entry(frame_izquierdo, 
                                font=("Helvetica", 11), 
                                width=10)
        self.entry_b.pack(anchor="w", pady=2)
        self.entry_b.insert(0, "-4") # Valor por defecto

        btn_calcular = tk.Button(frame_izquierdo, 
                                text="Calcular y Graficar", 
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
        try:
            m = float(self.entry_m.get())
            b = float(self.entry_b.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en 'm' y 'b'.")
            return

        if m != 0:
            raiz = -b / m
            texto_raiz = f"Raíz (Intersección X): ({raiz:.2f}, 0)"
        else:
            texto_raiz = "Raíz (Intersección X): No tiene (paralela al eje X)"

        texto_valores = (
            f"--- VALORES CLAVE ---\n"
            f"Pendiente (m): {m}\n"
            f"Ordenada al origen (b): {b}\n"
            f"Intersección Y: (0, {b})\n"
            f"{texto_raiz}"
        )
        self.lbl_valores_clave_1ro.config(text=texto_valores)

        for widget in self.frame_grafica_1ro.winfo_children():
            widget.destroy()

        centro_x = raiz if m != 0 else 0
        x = np.linspace(centro_x - 10, centro_x + 10, 100)
        y = m * x + b

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(x, y, color="#2E7D32", linewidth=2, label=f"y = {m}x + {b}")
        
        ax.axhline(0, color='black', linewidth=1) # Eje X
        ax.axvline(0, color='black', linewidth=1) # Eje Y
        ax.grid(True, linestyle='--', alpha=0.6)   # Cuadrícula de fondo
        ax.set_title("Gráfica de la Ecuación Lineal", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.legend()

        ax.plot(0, b, 'ro') # Punto intersección Y
        if m != 0:
            ax.plot(raiz, 0, 'ro') # Punto de la raíz

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_1ro)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        plt.close(fig)



    def grafica_segundo_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Segundo Grado: y = ax² + bx + c")
        ventana_hija.geometry("750x550") # Un poco más alta por los datos extra
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
                text="y = ax² + bx + c", 
                font=("Helvetica", 12, "italic"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)


        tk.Label(frame_izquierdo, 
                text="Valor de a (Cuadrático):", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        
        self.entry_a2 = tk.Entry(frame_izquierdo, 
                                font=("Helvetica", 11), 
                                width=10)
        self.entry_a2.pack(anchor="w", pady=2)
        self.entry_a2.insert(0, "1") # x² por defecto

        tk.Label(frame_izquierdo, 
                text="Valor de b (Lineal):", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        
        self.entry_b2 = tk.Entry(frame_izquierdo, 
                                font=("Helvetica", 11), 
                                width=10)
        self.entry_b2.pack(anchor="w", pady=2)
        self.entry_b2.insert(0, "-2") # -2x por defecto

        tk.Label(frame_izquierdo, 
                text="Valor de c (Independiente):", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        
        self.entry_c2 = tk.Entry(frame_izquierdo, 
                                font=("Helvetica", 11), 
                                width=10)
        self.entry_c2.pack(anchor="w", pady=2)
        self.entry_c2.insert(0, "-3") # -3 por defecto

        btn_calcular = tk.Button(frame_izquierdo, 
                                text="Calcular y Graficar", 
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
        try:
            a = float(self.entry_a2.get())
            b = float(self.entry_b2.get())
            c = float(self.entry_c2.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en 'a', 'b' y 'c'.")
            return

        if a == 0:
            messagebox.showerror("Error matemático", "El coeficiente 'a' no puede ser 0 en una ecuación cuadrática.")
            return

        discriminante = b**2 - 4*a*c
        
        vx = -b / (2 * a)
        vy = a * (vx**2) + b * vx + c

        if discriminante > 0:
            x1 = (-b + np.sqrt(discriminante)) / (2 * a)
            x2 = (-b - np.sqrt(discriminante)) / (2 * a)
            texto_raices = f"Raíces (Reales distintos):\n  X1 = {x1:.2f}\n  X2 = {x2:.2f}"
            puntos_raices = [(x1, 0), (x2, 0)]
        elif discriminante == 0:
            x1 = -b / (2 * a)
            texto_raices = f"Raíz (Real única / repetida):\n  X = {x1:.2f}"
            puntos_raices = [(x1, 0)]
        else:
            parte_real = -b / (2 * a)
            parte_imag = np.sqrt(abs(discriminante)) / (2 * a)
            texto_raices = f"Raíces (Complejas/Imaginarias):\n  X1 = {parte_real:.2f} + {parte_imag:.2f}i\n  X2 = {parte_real:.2f} - {parte_imag:.2f}i"
            puntos_raices = [] # No se cruza el eje X real

        texto_valores = (
            f"--- VALORES CLAVE ---\n"
            f"Discriminante (Δ): {discriminante:.2f}\n"
            f"Vértice (H, K): ({vx:.2f}, {vy:.2f})\n"
            f"Intersección Y: (0, {c})\n"
            f"{texto_raices}"
        )
        self.lbl_valores_clave_2do.config(text=texto_valores)
        for widget in self.frame_grafica_2do.winfo_children():
            widget.destroy()

        x = np.linspace(vx - 10, vx + 10, 200)
        y = a * (x**2) + b * x + c

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(x, y, color="#2E7D32", linewidth=2, label=f"y = {a}x² + {b}x + {c}")
        
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_title("Gráfica de la Ecuación Cuadrática", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")

        ax.plot(vx, vy, 'bo', label=f"Vértice ({vx:.1f}, {vy:.1f})") # Vértice en azul ('bo')
        ax.plot(0, c, 'go', label=f"Int. Y (0, {c})")             # Intersección Y en verde ('go')
        
        for px, py in puntos_raices:
            ax.plot(px, py, 'ro')
        if puntos_raices:
            ax.plot(puntos_raices[0][0], puntos_raices[0][1], 'ro', label="Raíces (Int. X)")

        ax.legend()

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
                text="x - ", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=1, column=2)
        self.entry_b2 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_b2.grid(row=1, column=3); self.entry_b2.insert(0, "1") # Ojo: lo resolveremos considerando algebraicamente ax + by = c, el "-" es meramente visual o el usuario ingresará el signo
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
            ax.plot(x_vals, y_vals1, color="#1B5E20", linewidth=2, label=f"{a1}x + {b1}y = {c1}")
        else:
            ax.axvline(c1 / a1, color="#1B5E20", linewidth=2, linestyle="--", label=f"{a1}x = {c1}")

        if b2 != 0:
            y_vals2 = (c2 - a2 * x_vals) / b2
            ax.plot(x_vals, y_vals2, color="#E65100", linewidth=2, label=f"{a2}x + {b2}y = {c2}")
        else:
            ax.axvline(c2 / a2, color="#E65100", linewidth=2, linestyle="--", label=f"{a2}x = {c2}")

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
                                    padx=15, pady=15)
        
        self.frame_grafica_3x3 = tk.Frame(ventana_hija, 
                                        bg="white", 
                                        bd=1, 
                                        relief="sunken")
        self.frame_grafica_3x3.pack(side="right", 
                                    expand=True, 
                                    fill="both", 
                                    padx=15, 
                                    pady=15)


    def procesar_sistema_3x3(self):
        try:
            # 1. Recuperar los coeficientes de las 3 ecuaciones
            a1, b1, c1, d1 = float(self.entry_a3_1.get()), float(self.entry_b3_1.get()), float(self.entry_c3_1.get()), float(self.entry_d3_1.get())
            a2, b2, c2, d2 = float(self.entry_a3_2.get()), float(self.entry_b3_2.get()), float(self.entry_c3_2.get()), float(self.entry_d3_2.get())
            a3, b3, c3, d3 = float(self.entry_a3_3.get()), float(self.entry_b3_3.get()), float(self.entry_c3_3.get()), float(self.entry_d3_3.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en todos los coeficientes.")
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
        
        x_rango = np.linspace(centro_x - 5, centro_x + 5, 20)
        y_rango = np.linspace(centro_y - 5, centro_y + 5, 20)
        X, Y = np.meshgrid(x_rango, y_rango) # Crea la malla 2D para evaluar los planos

        # Inicializamos la figura de Matplotlib indicando explícitamente que es proyección 3D
        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        # Despejamos 'z' de cada ecuación para graficar el plano: z = (d - ax - by) / c
        # (Agregamos un control rápido por si 'c' es 0, sumando una millonésima para evitar división por cero en la muestra)
        Z1 = (d1 - a1 * X - b1 * Y) / (c1 if c1 != 0 else 1e-6)
        Z2 = (d2 - a2 * X - b2 * Y) / (c2 if c2 != 0 else 1e-6)
        Z3 = (d3 - a3 * X - b3 * Y) / (c3 if c3 != 0 else 1e-6)

        # Dibujamos las superficies (planos) con transparencias (alpha) para que se vea dónde se cruzan
        ax.plot_surface(X, Y, Z1, alpha=0.5, color='green', label='Ecuación 1')
        ax.plot_surface(X, Y, Z2, alpha=0.5, color='orange', label='Ecuación 2')
        ax.plot_surface(X, Y, Z3, alpha=0.5, color='blue', label='Ecuación 3')

        # Si hay solución, marcamos el punto exacto de intersección en el espacio con una esfera roja
        if solucion_existe:
            ax.scatter(sol_x, sol_y, sol_z, color='red', s=50, depthshade=False, label=f"Solución ({sol_x:.1f}, {sol_y:.1f}, {sol_z:.1f})")

        # Configurar etiquetas espaciales
        ax.set_title("Intersección de Planos 3D", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.set_zlabel("Eje Z")
        
        # Ajustamos los límites para centrar la visualización en la respuesta
        if solucion_existe:
            ax.set_xlim(sol_x - 5, sol_x + 5)
            ax.set_ylim(sol_y - 5, sol_y + 5)
            ax.set_zlim(sol_z - 5, sol_z + 5)

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
