import tkinter as tk
from tkinter import messagebox
import os
import numpy as np # Importamos NumPy para manejar arreglos numéricos y cálculos matemáticos complejos (como linspace y linalg)
import matplotlib.pyplot as plt # Importamos pyplot de Matplotlib para crear las gráficas (líneas, puntos, planos)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # ¡MUY IMPORTANTE! Esta clase sirve como "puente" para poder incrustar una gráfica de Matplotlib dentro de una ventana de Tkinter


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
        # Configuración de la ventana principal
        self.ventana = ventana
        self.ventana.title("Gráficas y Ecuaciones - CECYTEQ")
        self.ventana.geometry("480x450")
        self.ventana.config(bg=COLOR_FONDO_PRINCIPAL)

        #### CONFIGURACIÓN DEL ICONO ####
        # Obtiene la ruta de la carpeta actual donde está el script para cargar el logo
        self.carpeta_proyecto = os.path.dirname(__file__)
        self.ruta_icono = os.path.join(self.carpeta_proyecto, "logo_cecyteq.png")

        try:
            self.icono = tk.PhotoImage(file=self.ruta_icono)
            self.ventana.iconphoto(False, self.icono)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        # Configuración de cuadrícula (Grid) para centrar y distribuir los elementos
        # weight=1 le dice a Tkinter que expanda esa fila/columna si la ventana cambia de tamaño
        self.ventana.rowconfigure(0, weight=1)
        self.ventana.rowconfigure(1, weight=1)
        self.ventana.rowconfigure(2, weight=1)
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)

        # Etiqueta de Título principal
        tk.Label(self.ventana,
                text="Gráficas \ny \nEcuaciones", 
                font=fuente_titulo,
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL,
                relief="flat",
                padx=20).grid(row=0, column=0, rowspan=3, sticky="nsew") 

        # Botones del menú principal. Cada uno tiene asignado un comando (command) que abre una ventana hija diferente
        btn_primer = tk.Button(self.ventana,
                text="Gráfica una ecuación \nde primer grado",
                font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2", bd=0, pady=10)
        btn_primer.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        btn_primer.config(command=self.grafica_primer_grado)

        btn_segundo = tk.Button(self.ventana,
                text="Gráfica una ecuación \nde segundo grado",
                font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2", bd=0, pady=10)
        btn_segundo.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        btn_segundo.config(command=self.grafica_segundo_grado)

        btn_sistemas = tk.Button(self.ventana,
                text="Sistemas de ecuaciones",
                font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2", bd=0, pady=10)
        btn_sistemas.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        btn_sistemas.config(command=self.ventana_sistema_ecuaciones)


    #### VENTANAS HIJAS ####
    def grafica_primer_grado(self):
        # tk.Toplevel() es la forma en que Tkinter crea una nueva ventana flotante (hija)
        # que depende de la ventana principal (self.ventana). Si cierras la principal, esta también se cierra.
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Primer Grado: y = mx + b")
        ventana_hija.geometry("750x500")  # Dimensiones más anchas para acomodar el panel izquierdo de datos y el derecho de la gráfica
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        # --- PANEL IZQUIERDO: Entradas de datos ---
        frame_izquierdo = tk.Frame(ventana_hija, bg=COLOR_FONDO_PRINCIPAL, padx=15, pady=15)
        frame_izquierdo.pack(side="left", fill="y") # Se empaqueta a la izquierda y se expande en el eje Y (verticalmente)

        tk.Label(frame_izquierdo, text="Ecuación Lineal", font=("Impact", 16), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo, text="y = mx + b", font=("Helvetica", 12, "italic"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        # Campos de entrada (Entry) para 'm' (pendiente) y 'b' (intersección)
        tk.Label(frame_izquierdo, text="Valor de m (Pendiente):", font=("Helvetica", 10, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        self.entry_m = tk.Entry(frame_izquierdo, font=("Helvetica", 11), width=10)
        self.entry_m.pack(anchor="w", pady=2)
        self.entry_m.insert(0, "2") # Valor por defecto

        tk.Label(frame_izquierdo, text="Valor de b (Intersección Y):", font=("Helvetica", 10, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        self.entry_b = tk.Entry(frame_izquierdo, font=("Helvetica", 11), width=10)
        self.entry_b.pack(anchor="w", pady=2)
        self.entry_b.insert(0, "-4") # Valor por defecto

        # Botón que detona la acción de graficar
        btn_calcular = tk.Button(frame_izquierdo, text="Calcular y Graficar", font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON, cursor="hand2", bd=0, padx=10, pady=5, command=self.procesar_primer_grado)
        btn_calcular.pack(pady=20, fill="x")

        # Etiqueta para mostrar los resultados matemáticos (raíces, vértices, etc.)
        self.lbl_valores_clave_1ro = tk.Label(frame_izquierdo, text="Valores clave:\n-\n-", font=("Helvetica", 10), justify="left", fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_1ro.pack(anchor="w", pady=10)

        # --- PANEL DERECHO: Contenedor para la Gráfica ---
        # Creamos un Frame vacío. Este Frame será el "lienzo" (master) donde incrustaremos la gráfica de Matplotlib más adelante.
        self.frame_grafica_1ro = tk.Frame(ventana_hija, bg="white", bd=1, relief="sunken")
        self.frame_grafica_1ro.pack(side="right", expand=True, fill="both", padx=15, pady=15)


    #### PROCESO DE GRAFICACIÓN (Ecuación 1er Grado) ####
    def procesar_primer_grado(self):
        try:
            # Obtiene y convierte los datos ingresados a números decimales (float)
            m = float(self.entry_m.get())
            b = float(self.entry_b.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en 'm' y 'b'.")
            return

        # Matemáticas básicas para encontrar la raíz (intersección en X)
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

        # ¡MUY IMPORTANTE!: Antes de dibujar una nueva gráfica, debemos destruir (limpiar)
        # cualquier gráfica anterior que esté en el frame. Si no hacemos esto, las gráficas se enciman.
        for widget in self.frame_grafica_1ro.winfo_children():
            widget.destroy()

        # Generación de coordenadas (x, y) usando NumPy
        centro_x = raiz if m != 0 else 0
        # np.linspace crea un arreglo de 100 números uniformemente espaciados entre centro_x-10 y centro_x+10
        x = np.linspace(centro_x - 10, centro_x + 10, 100) 
        y = m * x + b # Aplica la fórmula a todo el arreglo 'x' de una sola ve  z

        # --- CREACIÓN DE LA GRÁFICA CON MATPLOTLIB ---
        # plt.subplots crea la Figura (el marco completo) y los Ejes (el área donde se dibuja)
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(x, y, color="#2E7D32", linewidth=2, label=f"y = {m}x + {b}") # Dibuja la línea
        
        # Dibujamos líneas negras delgadas para representar los ejes X e Y (origen)
        ax.axhline(0, color='black', linewidth=1) # Eje X
        ax.axvline(0, color='black', linewidth=1) # Eje Y
        ax.grid(True, linestyle='--', alpha=0.6)   # Cuadrícula de fondo
        ax.set_title("Gráfica de la Ecuación Lineal", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.legend()

        ax.plot(0, b, 'ro') # Dibuja un punto rojo ('ro') en la intersección Y
        if m != 0:
            ax.plot(raiz, 0, 'ro') # Dibuja un punto rojo en la raíz

        # --- INCRUSTANDO LA GRÁFICA EN TKINTER ---
        # FigureCanvasTkAgg toma la figura 'fig' de Matplotlib y la convierte en un Canvas de Tkinter
        # apuntando al Frame 'self.frame_grafica_1ro' como su contenedor maestro (master)
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_1ro)
        canvas.draw() # Ordena renderizar/dibujar la gráfica
        
        # get_tk_widget() obtiene el widget real de Tkinter subyacente y lo empaqueta (pack) para que se vea
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        # Cerramos la figura en la memoria de Matplotlib para evitar fugas de memoria (memory leaks)
        plt.close(fig)



    def grafica_segundo_grado(self):
        # Misma lógica: Crear una ventana hija usando Toplevel
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Segundo Grado: y = ax² + bx + c")
        ventana_hija.geometry("750x550") 
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        # Panel izquierdo para datos de ax^2 + bx + c
        frame_izquierdo = tk.Frame(ventana_hija, bg=COLOR_FONDO_PRINCIPAL, padx=15, pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo, text="Ecuación Cuadrática", font=("Impact", 16), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo, text="y = ax² + bx + c", font=("Helvetica", 12, "italic"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        tk.Label(frame_izquierdo, text="Valor de a (Cuadrático):", font=("Helvetica", 10, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        self.entry_a2 = tk.Entry(frame_izquierdo, font=("Helvetica", 11), width=10)
        self.entry_a2.pack(anchor="w", pady=2)
        self.entry_a2.insert(0, "1")

        tk.Label(frame_izquierdo, text="Valor de b (Lineal):", font=("Helvetica", 10, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        self.entry_b2 = tk.Entry(frame_izquierdo, font=("Helvetica", 11), width=10)
        self.entry_b2.pack(anchor="w", pady=2)
        self.entry_b2.insert(0, "-2")

        tk.Label(frame_izquierdo, text="Valor de c (Independiente):", font=("Helvetica", 10, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(anchor="w", pady=(10,0))
        self.entry_c2 = tk.Entry(frame_izquierdo, font=("Helvetica", 11), width=10)
        self.entry_c2.pack(anchor="w", pady=2)
        self.entry_c2.insert(0, "-3")

        btn_calcular = tk.Button(frame_izquierdo, text="Calcular y Graficar", font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON, cursor="hand2", bd=0, padx=10, pady=5, command=self.procesar_segundo_grado)
        btn_calcular.pack(pady=15, fill="x")

        self.lbl_valores_clave_2do = tk.Label(frame_izquierdo, text="Valores clave:\n-\n-", font=("Helvetica", 10), justify="left", fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_2do.pack(anchor="w", pady=10)

        # Panel derecho vacío para incrustar la gráfica posteriormente
        self.frame_grafica_2do = tk.Frame(ventana_hija, bg="white", bd=1, relief="sunken")
        self.frame_grafica_2do.pack(side="right", expand=True, fill="both", padx=15, pady=15)


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

        # Calcular el discriminante (lo que va dentro de la raíz cuadrada en la fórmula general)
        discriminante = b**2 - 4*a*c
        
        # Calcular el Vértice de la parábola
        vx = -b / (2 * a)
        vy = a * (vx**2) + b * vx + c

        # Análisis del discriminante para buscar las raíces (donde cruza el eje X)
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
            # Manejo de números complejos si no toca el eje X
            parte_real = -b / (2 * a)
            parte_imag = np.sqrt(abs(discriminante)) / (2 * a)
            texto_raices = f"Raíces (Complejas/Imaginarias):\n  X1 = {parte_real:.2f} + {parte_imag:.2f}i\n  X2 = {parte_real:.2f} - {parte_imag:.2f}i"
            puntos_raices = [] # No hay cruce en el plano real

        texto_valores = (
            f"--- VALORES CLAVE ---\n"
            f"Discriminante (Δ): {discriminante:.2f}\n"
            f"Vértice (H, K): ({vx:.2f}, {vy:.2f})\n"
            f"Intersección Y: (0, {c})\n"
            f"{texto_raices}"
        )
        self.lbl_valores_clave_2do.config(text=texto_valores)
        
        # Limpieza del lienzo anterior
        for widget in self.frame_grafica_2do.winfo_children():
            widget.destroy()

        # Genera puntos de X alrededor del vértice de la parábola para que siempre se vea bien centrada
        x = np.linspace(vx - 10, vx + 10, 200)
        y = a * (x**2) + b * x + c

        # --- DIBUJO DE LA PARÁBOLA ---
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(x, y, color="#2E7D32", linewidth=2, label=f"y = {a}x² + {b}x + {c}")
        
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_title("Gráfica de la Ecuación Cuadrática", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")

        # Dibujar los puntos notables (vértice, intersección y raíces)
        ax.plot(vx, vy, 'bo', label=f"Vértice ({vx:.1f}, {vy:.1f})") # Azul para el vértice
        ax.plot(0, c, 'go', label=f"Int. Y (0, {c})")             # Verde para la Int. Y
        
        for px, py in puntos_raices:
            ax.plot(px, py, 'ro') # Rojo para las raíces
        if puntos_raices:
            ax.plot(puntos_raices[0][0], puntos_raices[0][1], 'ro', label="Raíces (Int. X)")

        ax.legend()

        # --- INCRUSTAR EN TKINTER ---
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_2do)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        plt.close(fig)



    def ventana_sistema_ecuaciones(self):
        # Esta es una ventana intermedia (un submenú) para decidir entre sistemas 2x2 o 3x3
        ventana_sistemas = tk.Toplevel(self.ventana)
        ventana_sistemas.title("Sistemas de Ecuaciones")
        ventana_sistemas.geometry("400x300")
        ventana_sistemas.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_sistemas.iconphoto(False, self.icono)

        tk.Label(ventana_sistemas, text="Selecciona el Tipo de Sistema", font=("Impact", 18), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=25)

        tk.Button(ventana_sistemas, text="Sistemas de 2x2", font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON, cursor="hand2", bd=0, pady=10, command=self.sistema_2x2).pack(pady=12, fill="x", padx=50)

        tk.Button(ventana_sistemas, text="Sistemas de 3x3", font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON, cursor="hand2", bd=0, pady=10, command=self.sistema_3x3).pack(pady=12, fill="x", padx=50)

    def sistema_2x2(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 2x2")
        ventana_hija.geometry("800x550")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        frame_izquierdo = tk.Frame(ventana_hija, bg=COLOR_FONDO_PRINCIPAL, padx=15, pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo, text="Sistema de 2x2", font=("Impact", 16), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo, text="ax + by = c", font=("Helvetica", 11, "italic"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        # Aquí usamos grid dentro de un frame empaquetado para alinear bonito los inputs estilo: [ ]x + [ ]y = [ ]
        frame_inputs = tk.Frame(frame_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        frame_inputs.pack(pady=10)

        # Entradas para la Ecuación 1
        tk.Label(frame_inputs, text="Ecuación 1: ", font=("Helvetica", 10, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).grid(row=0, column=0, pady=5)
        self.entry_a1 = tk.Entry(frame_inputs, width=5, font=("Helvetica", 11)); self.entry_a1.grid(row=0, column=1); self.entry_a1.insert(0, "1")
        tk.Label(frame_inputs, text="x + ", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=0, column=2)
        self.entry_b1 = tk.Entry(frame_inputs, width=5, font=("Helvetica", 11)); self.entry_b1.grid(row=0, column=3); self.entry_b1.insert(0, "1")
        tk.Label(frame_inputs, text="y = ", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=0, column=4)
        self.entry_c1 = tk.Entry(frame_inputs, width=5, font=("Helvetica", 11)); self.entry_c1.grid(row=0, column=5); self.entry_c1.insert(0, "5")

        # Entradas para la Ecuación 2
        tk.Label(frame_inputs, text="Ecuación 2: ", font=("Helvetica", 10, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).grid(row=1, column=0, pady=5)
        self.entry_a2 = tk.Entry(frame_inputs, width=5, font=("Helvetica", 11)); self.entry_a2.grid(row=1, column=1); self.entry_a2.insert(0, "1")
        tk.Label(frame_inputs, text="x - ", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=1, column=2)
        self.entry_b2 = tk.Entry(frame_inputs, width=5, font=("Helvetica", 11)); self.entry_b2.grid(row=1, column=3); self.entry_b2.insert(0, "1") 
        tk.Label(frame_inputs, text="y = ", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=1, column=4)
        self.entry_c2 = tk.Entry(frame_inputs, width=5, font=("Helvetica", 11)); self.entry_c2.grid(row=1, column=5); self.entry_c2.insert(0, "1")

        btn_calcular = tk.Button(frame_izquierdo, text="Resolver y Graficar", font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON, cursor="hand2", bd=0, padx=10, pady=5, command=self.procesar_sistema_2x2)
        btn_calcular.pack(pady=15, fill="x")

        self.lbl_valores_clave_sist = tk.Label(frame_izquierdo, text="Solución del sistema:\n-\n-", font=("Helvetica", 10), justify="left", fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_sist.pack(anchor="w", pady=10)

        # Contenedor gráfico vacío
        self.frame_grafica_sist = tk.Frame(ventana_hija, bg="white", bd=1, relief="sunken")
        self.frame_grafica_sist.pack(side="right", expand=True, fill="both", padx=15, pady=15)


    def procesar_sistema_2x2(self):
        try:
            a1, b1, c1 = float(self.entry_a1.get()), float(self.entry_b1.get()), float(self.entry_c1.get())
            a2, b2, c2 = float(self.entry_a2.get()), float(self.entry_b2.get()), float(self.entry_c2.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en todos los coeficientes.")
            return

        # Genera una Matriz A con los coeficientes (x, y) y una Matriz B con los resultados
        A = np.array([[a1, b1], [a2, b2]])
        B = np.array([c1, c2])

        # Calcula el determinante usando el módulo algebra lineal de numpy (linalg)
        determinante = np.linalg.det(A)

        if np.isclose(determinante, 0):
            # Si el determinante es 0, las rectas no se cruzan en un solo punto (son paralelas o la misma recta)
            self.lbl_valores_clave_sist.config(text="--- VALORES CLAVE ---\nEl sistema NO tiene solución única.\n(Rectas paralelas o coincidentes)")
            solucion_existe = False
        else:
            # Resuelve el sistema lineal (A * X = B)
            sol_x, sol_y = np.linalg.solve(A, B)
            texto_valores = (f"--- VALORES CLAVE ---\nDeterminante: {determinante:.2f}\nPunto de Intersección (Solución):\n  X = {sol_x:.2f}\n  Y = {sol_y:.2f}")
            self.lbl_valores_clave_sist.config(text=texto_valores)
            solucion_existe = True

        for widget in self.frame_grafica_sist.winfo_children():
            widget.destroy()

        centro_x = sol_x if solucion_existe else 0
        x_vals = np.linspace(centro_x - 10, centro_x + 10, 100)

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        # Graficamos la línea 1 despejando 'y': y = (c1 - a1*x) / b1
        if b1 != 0:
            y_vals1 = (c1 - a1 * x_vals) / b1
            ax.plot(x_vals, y_vals1, color="#1B5E20", linewidth=2, label=f"{a1}x + {b1}y = {c1}")
        else:
            # Si b1 es 0, es una línea vertical x = c/a
            ax.axvline(c1 / a1, color="#1B5E20", linewidth=2, linestyle="--", label=f"{a1}x = {c1}")

        # Graficamos la línea 2
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

        # Incrustar en Tkinter de la misma forma que en los métodos pasados
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
        
        frame_izquierdo = tk.Frame(ventana_hija, bg=COLOR_FONDO_PRINCIPAL, padx=15, pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo, text="Sistema de 3x3", font=("Impact", 16), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        tk.Label(frame_izquierdo, text="ax + by + cz = d", font=("Helvetica", 11, "italic"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        frame_inputs = tk.Frame(frame_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        frame_inputs.pack(pady=10)

        ## Creación masiva de campos Entry para las 3 ecuaciones ##
        ## Ecuación 1 ##
        tk.Label(frame_inputs, text="Eq 1: ", font=("Helvetica", 9, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).grid(row=0, column=0, pady=5)
        self.entry_a3_1 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_a3_1.grid(row=0, column=1); self.entry_a3_1.insert(0, "1")
        tk.Label(frame_inputs, text="x+", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=0, column=2)
        self.entry_b3_1 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_b3_1.grid(row=0, column=3); self.entry_b3_1.insert(0, "1")
        tk.Label(frame_inputs, text="y+", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=0, column=4)
        self.entry_c3_1 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_c3_1.grid(row=0, column=5); self.entry_c3_1.insert(0, "1")
        tk.Label(frame_inputs, text="z=", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=0, column=6)
        self.entry_d3_1 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_d3_1.grid(row=0, column=7); self.entry_d3_1.insert(0, "6")

        ## Ecuación 2 ##
        tk.Label(frame_inputs, text="Eq 2: ", font=("Helvetica", 9, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).grid(row=1, column=0, pady=5)
        self.entry_a3_2 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_a3_2.grid(row=1, column=1); self.entry_a3_2.insert(0, "0")
        tk.Label(frame_inputs, text="x+", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=1, column=2)
        self.entry_b3_2 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_b3_2.grid(row=1, column=3); self.entry_b3_2.insert(0, "2")
        tk.Label(frame_inputs, text="y+", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=1, column=4)
        self.entry_c3_2 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_c3_2.grid(row=1, column=5); self.entry_c3_2.insert(0, "5")
        tk.Label(frame_inputs, text="z=", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=1, column=6)
        self.entry_d3_2 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_d3_2.grid(row=1, column=7); self.entry_d3_2.insert(0, "-4")

        ## Ecuación 3 ##
        tk.Label(frame_inputs, text="Eq 3: ", font=("Helvetica", 9, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).grid(row=2, column=0, pady=5)
        self.entry_a3_3 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_a3_3.grid(row=2, column=1); self.entry_a3_3.insert(0, "2")
        tk.Label(frame_inputs, text="x+", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=2, column=2)
        self.entry_b3_3 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_b3_3.grid(row=2, column=3); self.entry_b3_3.insert(0, "5")
        tk.Label(frame_inputs, text="y+", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=2, column=4)
        self.entry_c3_3 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_c3_3.grid(row=2, column=5); self.entry_c3_3.insert(0, "-1")
        tk.Label(frame_inputs, text="z=", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_TITULO).grid(row=2, column=6)
        self.entry_d3_3 = tk.Entry(frame_inputs, width=4, font=("Helvetica", 10)); self.entry_d3_3.grid(row=2, column=7); self.entry_d3_3.insert(0, "27")

        btn_calcular = tk.Button(frame_izquierdo, text="Resolver Sistema", font=fuente_botones, bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO_BOTON, cursor="hand2", bd=0, padx=10, pady=5, command=self.procesar_sistema_3x3)
        btn_calcular.pack(pady=15, fill="x")

        self.lbl_valores_clave_3x3 = tk.Label(frame_izquierdo, text="Solución del sistema:\n-\n-", font=("Helvetica", 10), justify="left", fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_3x3.pack(anchor="w", pady=10)

        # Aquí había código duplicado creando 'frame_grafica_3x3' dos veces. Lo dejaremos solo una vez.
        self.frame_grafica_3x3 = tk.Frame(ventana_hija, bg="white", bd=1, relief="sunken")
        self.frame_grafica_3x3.pack(side="right", expand=True, fill="both", padx=15, pady=15)


    def procesar_sistema_3x3(self):
        try:
            # 1. Recuperar los coeficientes de las 3 ecuaciones
            a1, b1, c1, d1 = float(self.entry_a3_1.get()), float(self.entry_b3_1.get()), float(self.entry_c3_1.get()), float(self.entry_d3_1.get())
            a2, b2, c2, d2 = float(self.entry_a3_2.get()), float(self.entry_b3_2.get()), float(self.entry_c3_2.get()), float(self.entry_d3_2.get())
            a3, b3, c3, d3 = float(self.entry_a3_3.get()), float(self.entry_b3_3.get()), float(self.entry_c3_3.get()), float(self.entry_d3_3.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en todos los coeficientes.")
            return

        # 2. Configurar matrices con NumPy (Matriz 3x3 para A y vector 1x3 para B)
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
            # Si hay solución, resuelve X, Y, Z
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

        # 3. Limpiar contenedor gráfico antes de montar el nuevo gráfico 3D
        for widget in self.frame_grafica_3x3.winfo_children():
            widget.destroy()

        # 4. Crear la Gráfica 3D usando Matplotlib
        centro_x = sol_x if solucion_existe else 0
        centro_y = sol_y if solucion_existe else 0
        
        x_rango = np.linspace(centro_x - 5, centro_x + 5, 20)
        y_rango = np.linspace(centro_y - 5, centro_y + 5, 20)
        
        # np.meshgrid toma los rangos 1D y crea matrices 2D que representan una cuadrícula en el piso XY
        X, Y = np.meshgrid(x_rango, y_rango) 

        # --- DIBUJANDO EL ESPACIO 3D ---
        # Inicializamos la figura de Matplotlib indicando explícitamente que es proyección 3D (projection='3d')
        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111, projection='3d') # Crea unos ejes tridimensionales

        # Despejamos 'z' de cada ecuación para graficar el plano: z = (d - ax - by) / c
        # (Agregamos un control rápido por si 'c' es 0, sumando un valor casi cero (1e-6) para evitar divisiones fatales)
        Z1 = (d1 - a1 * X - b1 * Y) / (c1 if c1 != 0 else 1e-6)
        Z2 = (d2 - a2 * X - b2 * Y) / (c2 if c2 != 0 else 1e-6)
        Z3 = (d3 - a3 * X - b3 * Y) / (c3 if c3 != 0 else 1e-6)

        # plot_surface dibuja los planos tridimensionales. "alpha" regula la transparencia para ver a través de ellos.
        ax.plot_surface(X, Y, Z1, alpha=0.5, color='green', label='Ecuación 1')
        ax.plot_surface(X, Y, Z2, alpha=0.5, color='orange', label='Ecuación 2')
        ax.plot_surface(X, Y, Z3, alpha=0.5, color='blue', label='Ecuación 3')

        # Si hay solución, marcamos el punto exacto de intersección en el espacio con una esfera (scatter)
        if solucion_existe:
            ax.scatter(sol_x, sol_y, sol_z, color='red', s=50, depthshade=False, label=f"Solución ({sol_x:.1f}, {sol_y:.1f}, {sol_z:.1f})")

        # Configurar etiquetas espaciales en los 3 ejes
        ax.set_title("Intersección de Planos 3D", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.set_zlabel("Eje Z")
        
        # Ajustamos los límites de la "caja" 3D para centrar la visualización donde está el punto de respuesta
        if solucion_existe:
            ax.set_xlim(sol_x - 5, sol_x + 5)
            ax.set_ylim(sol_y - 5, sol_y + 5)
            ax.set_zlim(sol_z - 5, sol_z + 5)

        # 5. Incrustar en Tkinter el gráfico 3D
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_3x3)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        plt.close(fig)


### Bucle Principal que Ejecuta la aplicación ###
if __name__ == "__main__":
    raiz = tk.Tk() # Inicializa el motor de interfaz gráfica
    app = MenuPrincipal(raiz) # Llama a la clase principal pasándole la ventana raíz
    raiz.mainloop() # loop infinito de Tkinter que mantiene la ventana abierta esperando clics/eventos