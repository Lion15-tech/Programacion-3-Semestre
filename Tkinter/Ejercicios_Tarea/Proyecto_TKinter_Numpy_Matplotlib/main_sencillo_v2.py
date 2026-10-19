# =============================================================================
# GRÁFICAS Y ECUACIONES - VERSIÓN EN CLASE
# -----------------------------------------------------------------------------
# Reorganizado dentro de una clase principal (AplicacionGraficas) manteniendo
# exactamente la misma lógica, interfaz y comportamiento original.
# =============================================================================

import tkinter as tk                  # Para crear ventanas, botones, etc.
from tkinter import messagebox        # Para mostrar mensajes de error
import numpy as np                    # Para cálculos matemáticos
from matplotlib.figure import Figure  # Para crear las gráficas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Para meter una gráfica dentro de una ventana de Tkinter
import os
import math 

class AplicacionGraficas:
    def __init__(self, root):
        self.root = root

        # Colores guardados en variables de instancia
        self.COLOR_FONDO = "#BCF6BC"            # Verde claro
        self.COLOR_TITULO = "#1E4620"           # Verde oscuro
        self.COLOR_BOTON = "#2E7D32"            # Verde de los botones
        self.COLOR_BOTON_PRESIONADO = "#1B5E20" # Verde más oscuro al hacer clic

        # Configurar la ventana principal
        self.root.title("Gráficas y Ecuaciones - CECYTEQ")
        self.root.geometry("400x420")
        self.root.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(self.root, "Gráficas y Ecuaciones", ("Impact", 22)).pack(pady=30)

        # Cada botón llama a la función de su ventana
        self.crear_boton(self.root, "Gráfica de primer grado\n(recta)", self.ventana_primer_grado).pack(pady=10, fill="x", padx=50)
        self.crear_boton(self.root, "Gráfica de segundo grado\n(parábola)", self.ventana_segundo_grado).pack(pady=10, fill="x", padx=50)
        self.crear_boton(self.root, "Sistemas de ecuaciones", self.ventana_sistemas).pack(pady=10, fill="x", padx=50)
        self.crear_boton(self.root, "Triángulos", self.ventana_triangulos).pack(pady=10, fill="x", padx=50)


        #### CONFIGURACIÓN DEL ICONO ####
        # Obtiene la ruta de la carpeta actual donde está el script para cargar el logo
        self.carpeta_proyecto = os.path.dirname(__file__)
        self.ruta_icono = os.path.join(self.carpeta_proyecto, "logo_cecyteq.png")
        try:
            self.icono = tk.PhotoImage(file=self.ruta_icono)
            self.root.iconphoto(True, self.icono)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")



    def crear_boton(self, padre, texto, comando):
        """Crea un botón verde. 'comando' es la función que se ejecuta al hacer clic."""
        boton = tk.Button(padre, text=texto, command=comando,
                          font=("Helvetica", 11, "bold"),
                          bg=self.COLOR_BOTON, fg="white",
                          activebackground=self.COLOR_BOTON_PRESIONADO,
                          activeforeground="white",
                          cursor="hand2", bd=0, pady=8)
        return boton

    def crear_etiqueta(self, padre, texto, fuente=("Helvetica", 11)):
        """Crea un texto (Label) con los colores del programa."""
        return tk.Label(padre, text=texto, font=fuente, justify="left",
                        bg=self.COLOR_FONDO, fg=self.COLOR_TITULO)

    def  crear_ventana(self, titulo, tamano):
        """Crea una ventana nueva dividida en dos partes:
        - panel_izq: donde van las cajas de texto, el botón y los resultados.
        - panel_graf: donde se dibuja la gráfica.
        Devuelve esos dos paneles."""
        ventana = tk.Toplevel(self.root)  # Toplevel = ventana secundaria
        ventana.title(titulo)
        ventana.geometry(tamano)          # Ejemplo: "750x520" (ancho x alto)
        ventana.config(bg=self.COLOR_FONDO)

        panel_izq = tk.Frame(ventana, bg=self.COLOR_FONDO, padx=15, pady=15)
        panel_izq.pack(side="left", fill="y")

        panel_graf = tk.Frame(ventana, bg="white")
        panel_graf.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        return panel_izq, panel_graf

    def leer_numero(self, caja):
        """Lee el texto de una caja y lo convierte en número.
        Cambia la coma por punto, así "2,5" también funciona.
        Si el texto no es un número, float() provoca un ValueError
        (el error se atrapa después con try/except)."""
        texto = caja.get().replace(",", ".")
        return float(texto)

    def leer_fila(self, cajas):
        """Lee TODAS las cajas de una lista y devuelve una lista de números."""
        numeros = []
        for caja in cajas:
            numeros.append(self.leer_numero(caja))
        return numeros

    def crear_fila_punto(self, panel, letra, x_inicial, y_inicial):
        """Crea una línea con la forma:  A ( [x] , [y] )  y devuelve las dos cajas."""
        fila = tk.Frame(panel, bg=self.COLOR_FONDO)
        fila.pack(pady=4)

        self.crear_etiqueta(fila, letra + " (").pack(side="left")

        caja_x = tk.Entry(fila, width=5, justify="center")
        caja_x.insert(0, x_inicial)
        caja_x.pack(side="left")

        self.crear_etiqueta(fila, ",").pack(side="left")

        caja_y = tk.Entry(fila, width=5, justify="center")
        caja_y.insert(0, y_inicial)
        caja_y.pack(side="left")

        self.crear_etiqueta(fila, ")").pack(side="left")

        return caja_x, caja_y

    def crear_fila_ecuacion(self, panel, textos, valores):
        """Crea una ecuación con cajas de texto, por ejemplo:  [1] x + [1] y = [5]"""
        fila = tk.Frame(panel, bg=self.COLOR_FONDO)
        fila.pack(pady=4)

        cajas = []
        for i in range(len(valores)):
            caja = tk.Entry(fila, width=5, justify="center")
            caja.insert(0, valores[i])
            caja.pack(side="left")
            cajas.append(caja)

            if i < len(textos):
                self.crear_etiqueta(fila, textos[i]).pack(side="left")

        return cajas

    def vincular_enter(self, lista_cajas, funcion_graficar):
        """Hace que al presionar Enter en una caja pase a la siguiente.
        Al presionar Enter en la última caja, ejecuta la función de graficar/resolver."""
        def al_presionar_enter(event, indice):
            if indice < len(lista_cajas) - 1:
                lista_cajas[indice + 1].focus_set()
            else:
                funcion_graficar()

        for i, caja in enumerate(lista_cajas):
            caja.bind("<Return>", lambda e, idx=i: al_presionar_enter(e, idx))

    def mostrar_figura(self, figura, panel):
        """Mete la gráfica (figura) dentro de un panel de Tkinter."""
        for widget in panel.winfo_children():
            widget.destroy()

        lienzo = FigureCanvasTkAgg(figura, master=panel)
        lienzo.draw()
        lienzo.get_tk_widget().pack(expand=True, fill="both")

    def decorar_ejes(self, ax, titulo):
        """Agrega a una gráfica 2D los ejes, la cuadrícula, los títulos y la leyenda."""
        ax.axhline(0, color="black", linewidth=1)
        ax.axvline(0, color="black", linewidth=1)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_title(titulo, fontweight="bold")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.legend(fontsize=8)

    def marcar_puntos(self, ax, puntos, letras):
        """Dibuja los puntos que escribió el usuario, con su letra y coordenadas."""
        for i in range(len(puntos)):
            x, y = puntos[i]
            if i == 0:
                ax.plot(x, y, "bo", markersize=8, label="Puntos ingresados")
            else:
                ax.plot(x, y, "bo", markersize=8)
            ax.text(x, y, f"  {letras[i]}({x:.1f}, {y:.1f})", color="blue", fontsize=8)

    def crear_campo(self, panel, texto, valor_inicial):
        """Crea una etiqueta con una caja de texto debajo y devuelve la caja."""
        self.crear_etiqueta(panel, texto).pack(pady=(8, 0))
        caja = tk.Entry(panel, width=10, justify="center")
        caja.insert(0, valor_inicial)
        caja.pack(pady=4)
        return caja

    def crear_opciones(self, panel, textos):
        """Crea botones de opción (solo se puede elegir UNO).
        Devuelve una variable: su .get() da la posición elegida (0, 1, 2...)."""
        eleccion = tk.IntVar(value=0)
        for i in range(len(textos)):
            tk.Radiobutton(panel, text=textos[i], variable=eleccion, value=i,
                           bg=self.COLOR_FONDO, fg=self.COLOR_TITULO,
                           activebackground=self.COLOR_FONDO,
                           selectcolor="white", anchor="w").pack(fill="x")
        return eleccion

    # ---------------------------------------------------------------------------
    #                        VENTANAS PARA EJERCICIOS
    # ---------------------------------------------------------------------------
    # ====================== ECUACIÓN DE PRIMER GRADO ===========================
    def ventana_primer_grado(self):
        panel_izq, panel_graf = self.crear_ventana("Ecuación de primer grado", "750x520")

        self.crear_etiqueta(panel_izq, "Ecuación Lineal", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Escribe 2 puntos (x, y)").pack()

        caja_x1, caja_y1 = self.crear_fila_punto(panel_izq, "A", "0", "-4")
        caja_x2, caja_y2 = self.crear_fila_punto(panel_izq, "B", "3", "2")

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def graficar():
            try:
                x1 = self.leer_numero(caja_x1)
                y1 = self.leer_numero(caja_y1)
                x2 = self.leer_numero(caja_x2)
                y2 = self.leer_numero(caja_y2)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if x1 == x2 and y1 == y2:
                messagebox.showerror("Error", "Los dos puntos son iguales. Escribe dos puntos distintos.")
                return

            figura = Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111)

            if x1 == x2:
                ax.axvline(x1, color="green", linewidth=2, label=f"x = {x1:.2f}")
                ax.set_xlim(min(x1, 0) - 3, max(x1, 0) + 3)
                ax.set_ylim(min(y1, y2, 0) - 3, max(y1, y2, 0) + 3)
                resultado.config(text=f"Recta vertical: x = {x1:.2f}\n"
                                      f"Pendiente: indefinida\n"
                                      f"Intersección X: ({x1:.2f}, 0)")
            else:
                m = (y2 - y1) / (x2 - x1)
                b = y1 - m * x1

                lista_x = [x1, x2, 0]

                if m != 0:
                    raiz = -b / m
                    lista_x.append(raiz)
                    texto_raiz = f"Raíz (cruce con X): ({raiz:.2f}, 0)"
                else:
                    texto_raiz = "Raíz: no tiene una sola (recta horizontal)"

                x_min = min(lista_x) - 2
                x_max = max(lista_x) + 2

                x = np.linspace(x_min, x_max, 100)
                y = m * x + b

                ax.plot(x, y, color="green", linewidth=2, label=f"y = {m:.2f}x {b:+.2f}")
                ax.plot(0, b, "go", label=f"Cruce con Y (0, {b:.2f})")
                if m != 0:
                    ax.plot(raiz, 0, "ro", label=f"Raíz ({raiz:.2f}, 0)")
                ax.set_xlim(x_min, x_max)

                resultado.config(text=f"y = {m:.2f}x {b:+.2f}\n"
                                      f"Pendiente (m): {m:.2f}\n"
                                      f"Ordenada al origen (b): {b:.2f}\n"
                                      f"{texto_raiz}")

            self.marcar_puntos(ax, [(x1, y1), (x2, y2)], ["A", "B"])
            self.decorar_ejes(ax, "Gráfica de la recta")
            self.mostrar_figura(figura, panel_graf)

        self.crear_boton(panel_izq, "Graficar", graficar).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_x1, caja_y1, caja_x2, caja_y2], graficar)

    # ========================= PARÁBOLA (SEGUNDO GRADO) ==========================
    def ventana_segundo_grado(self):
        panel_izq, panel_graf = self.crear_ventana("Ecuación de segundo grado", "750x580")

        self.crear_etiqueta(panel_izq, "Ecuación Cuadrática", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Escribe 3 puntos (x, y)\ncon valores de X distintos").pack()

        caja_x1, caja_y1 = self.crear_fila_punto(panel_izq, "A", "-1", "0")
        caja_x2, caja_y2 = self.crear_fila_punto(panel_izq, "B", "0", "-3")
        caja_x3, caja_y3 = self.crear_fila_punto(panel_izq, "C", "3", "0")

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def graficar():
            try:
                x1 = self.leer_numero(caja_x1)
                y1 = self.leer_numero(caja_y1)
                x2 = self.leer_numero(caja_x2)
                y2 = self.leer_numero(caja_y2)
                x3 = self.leer_numero(caja_x3)
                y3 = self.leer_numero(caja_y3)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if len(set([x1, x2, x3])) < 3:
                messagebox.showerror("Error", "Los 3 puntos deben tener valores de X distintos.")
                return

            matriz = np.array([[x1**2, x1, 1],
                               [x2**2, x2, 1],
                               [x3**2, x3, 1]])
            valores_y = np.array([y1, y2, y3])
            a, b, c = np.linalg.solve(matriz, valores_y)

            if abs(a) < 0.000000001:
                messagebox.showerror("Error", "Los 3 puntos están alineados: forman una recta, no una parábola.")
                return

            d = b**2 - 4*a*c
            vertice_x = -b / (2*a) + 0
            vertice_y = a * vertice_x**2 + b * vertice_x + c

            raices = []
            if abs(d) < 0.000000001:
                r = -b / (2*a)
                raices.append(r)
                texto_raices = f"Raíz única: X = {r:.2f}"
            elif d > 0:
                r1 = (-b + np.sqrt(d)) / (2*a)
                r2 = (-b - np.sqrt(d)) / (2*a)
                raices.append(r1)
                raices.append(r2)
                texto_raices = f"Raíces: X1 = {r1:.2f}\n            X2 = {r2:.2f}"
            else:
                parte_real = -b / (2*a) + 0
                parte_imaginaria = np.sqrt(-d) / (2*abs(a))
                texto_raices = (f"Raíces complejas:\n"
                                f"  X1 = {parte_real:.2f} + {parte_imaginaria:.2f}i\n"
                                f"  X2 = {parte_real:.2f} - {parte_imaginaria:.2f}i")

            ecuacion = f"y = {a:.2f}x² {b:+.2f}x {c:+.2f}"

            resultado.config(text=f"{ecuacion}\n"
                                  f"Discriminante: {d:.2f}\n"
                                  f"Vértice: ({vertice_x:.2f}, {vertice_y:.2f})\n"
                                  f"Cruce con Y: (0, {c:.2f})\n"
                                  f"{texto_raices}")

            lista_x = [x1, x2, x3, vertice_x, 0] + raices
            x_min = min(lista_x) - 2
            x_max = max(lista_x) + 2

            x = np.linspace(x_min, x_max, 200)
            y = a * x**2 + b * x + c

            figura = Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111)

            ax.plot(x, y, color="green", linewidth=2, label=ecuacion)
            ax.plot(vertice_x, vertice_y, "D", color="purple",
                    label=f"Vértice ({vertice_x:.2f}, {vertice_y:.2f})")
            ax.plot(0, c, "go", label=f"Cruce con Y (0, {c:.2f})")
            if len(raices) > 0:
                ax.plot(raices, [0] * len(raices), "ro", label="Raíces")

            self.marcar_puntos(ax, [(x1, y1), (x2, y2), (x3, y3)], ["A", "B", "C"])
            self.decorar_ejes(ax, "Gráfica de la parábola")
            self.mostrar_figura(figura, panel_graf)

        self.crear_boton(panel_izq, "Graficar", graficar).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_x1, caja_y1, caja_x2, caja_y2, caja_x3, caja_y3], graficar)


    # ====================== MENÚ PARA ELEGIR 2x2 O 3x3 ===========================
    def ventana_sistemas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Sistemas de Ecuaciones")
        ventana.geometry("400x250")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Selecciona el tipo de sistema", ("Impact", 18)).pack(pady=25)
        self.crear_boton(ventana, "Sistemas de 2x2", self.ventana_sistema_2x2).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Sistemas de 3x3", self.ventana_sistema_3x3).pack(pady=8, fill="x", padx=50)

    # ============================ SISTEMA DE 2x2 =================================
    def dibujar_recta(self, ax, a, b, c, x, color):
        """Dibuja la recta  a·x + b·y = c  sobre los ejes 'ax'."""
        if b != 0:
            y = (c - a * x) / b
            ax.plot(x, y, color=color, linewidth=2, label=f"{a:.1f}x {b:+.1f}y = {c:.1f}")
        else:
            ax.axvline(c / a, color=color, linewidth=2, linestyle="--",
                       label=f"{a:.1f}x = {c:.1f}")

    def ventana_sistema_2x2(self):
        panel_izq, panel_graf = self.crear_ventana("Sistema de ecuaciones 2x2", "800x550")

        self.crear_etiqueta(panel_izq, "Sistema de 2x2", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Forma:  ax + by = c").pack()

        fila1 = self.crear_fila_ecuacion(panel_izq, ["x +", "y ="], ["1", "1", "5"])
        fila2 = self.crear_fila_ecuacion(panel_izq, ["x +", "y ="], ["1", "-1", "1"])

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def graficar():
            try:
                a1, b1, c1 = self.leer_fila(fila1)
                a2, b2, c2 = self.leer_fila(fila2)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if (a1 == 0 and b1 == 0) or (a2 == 0 and b2 == 0):
                messagebox.showerror("Error", "En cada ecuación, 'a' y 'b' no pueden ser 0 a la vez.")
                return

            matriz = np.array([[a1, b1],
                               [a2, b2]])
            resultados = np.array([c1, c2])

            determinante = np.linalg.det(matriz)
            hay_solucion = abs(determinante) > 0.000000001

            if hay_solucion:
                x_sol, y_sol = np.linalg.solve(matriz, resultados)
                resultado.config(text=f"Determinante: {determinante:.2f}\n"
                                      f"Punto de cruce:\n"
                                      f"  X = {x_sol:.2f}\n"
                                      f"  Y = {y_sol:.2f}")
                centro = x_sol
            else:
                resultado.config(text="No hay solución única\n(rectas paralelas o iguales)")
                centro = 0

            x = np.linspace(centro - 10, centro + 10, 100)

            figura = Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111)

            self.dibujar_recta(ax, a1, b1, c1, x, "green")
            self.dibujar_recta(ax, a2, b2, c2, x, "orange")

            if hay_solucion:
                ax.plot(x_sol, y_sol, "ro", markersize=8,
                        label=f"Cruce ({x_sol:.1f}, {y_sol:.1f})")

            self.decorar_ejes(ax, "Cruce de rectas (sistema 2x2)")
            self.mostrar_figura(figura, panel_graf)

        self.crear_boton(panel_izq, "Resolver y Graficar", graficar).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter(fila1 + fila2, graficar)

    # ============================ SISTEMA DE 3x3 =================================
    def dibujar_plano(self, ax, a, b, c, d, rango_x, rango_y, rango_z, color):
        """Dibuja el plano  a·x + b·y + c·z = d  en una gráfica 3D."""
        if c != 0:
            X, Y = np.meshgrid(rango_x, rango_y)
            Z = (d - a * X - b * Y) / c
        elif b != 0:
            X, Z = np.meshgrid(rango_x, rango_z)
            Y = (d - a * X) / b
        else:
            Y, Z = np.meshgrid(rango_y, rango_z)
            X = np.full_like(Y, d / a)

        ax.plot_surface(X, Y, Z, alpha=0.5, color=color)

    def ventana_sistema_3x3(self):
        panel_izq, panel_graf = self.crear_ventana("Sistema de ecuaciones 3x3", "800x550")

        self.crear_etiqueta(panel_izq, "Sistema de 3x3", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Forma:  ax + by + cz = d").pack()

        fila1 = self.crear_fila_ecuacion(panel_izq, ["x +", "y +", "z ="], ["1", "1", "1", "6"])
        fila2 = self.crear_fila_ecuacion(panel_izq, ["x +", "y +", "z ="], ["0", "2", "5", "-4"])
        fila3 = self.crear_fila_ecuacion(panel_izq, ["x +", "y +", "z ="], ["2", "5", "-1", "27"])

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def graficar():
            try:
                a1, b1, c1, d1 = self.leer_fila(fila1)
                a2, b2, c2, d2 = self.leer_fila(fila2)
                a3, b3, c3, d3 = self.leer_fila(fila3)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if (a1 == 0 and b1 == 0 and c1 == 0) or \
               (a2 == 0 and b2 == 0 and c2 == 0) or \
               (a3 == 0 and b3 == 0 and c3 == 0):
                messagebox.showerror("Error", "En cada ecuación, 'a', 'b' y 'c' no pueden ser 0 a la vez.")
                return

            matriz = np.array([[a1, b1, c1],
                               [a2, b2, c2],
                               [a3, b3, c3]])
            resultados = np.array([d1, d2, d3])

            determinante = np.linalg.det(matriz)
            hay_solucion = abs(determinante) > 0.000000001

            if hay_solucion:
                x_sol, y_sol, z_sol = np.linalg.solve(matriz, resultados)
                resultado.config(text=f"Determinante: {determinante:.2f}\n"
                                      f"Solución:\n"
                                      f"  X = {x_sol:.2f}\n"
                                      f"  Y = {y_sol:.2f}\n"
                                      f"  Z = {z_sol:.2f}")
                centro_x, centro_y, centro_z = x_sol, y_sol, z_sol
            else:
                resultado.config(text="No hay solución única\n(planos paralelos o con\ninfinitos cruces)")
                centro_x, centro_y, centro_z = 0, 0, 0

            rango_x = np.linspace(centro_x - 5, centro_x + 5, 20)
            rango_y = np.linspace(centro_y - 5, centro_y + 5, 20)
            rango_z = np.linspace(centro_z - 5, centro_z + 5, 20)

            figura = Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111, projection="3d")

            self.dibujar_plano(ax, a1, b1, c1, d1, rango_x, rango_y, rango_z, "green")
            self.dibujar_plano(ax, a2, b2, c2, d2, rango_x, rango_y, rango_z, "orange")
            self.dibujar_plano(ax, a3, b3, c3, d3, rango_x, rango_y, rango_z, "blue")

            ax.set_xlim(centro_x - 5, centro_x + 5)
            ax.set_ylim(centro_y - 5, centro_y + 5)
            ax.set_zlim(centro_z - 5, centro_z + 5)

            if hay_solucion:
                ax.scatter(x_sol, y_sol, z_sol, color="red", s=50, depthshade=False,
                           label=f"Solución ({x_sol:.1f}, {y_sol:.1f}, {z_sol:.1f})")
                ax.legend(fontsize=8)

            ax.set_title("Cruce de planos (sistema 3x3)", fontweight="bold")
            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.set_zlabel("Eje Z")

            self.mostrar_figura(figura, panel_graf)

        self.crear_boton(panel_izq, "Resolver Sistema", graficar).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter(fila1 + fila2 + fila3, graficar)


    # ====================== MENÚ PARA ELEGIR TRIANGULOS ===========================
    def ventana_triangulos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Triángulos")
        ventana.geometry("400x300")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Selecciona el tipo de triángulo", ("Impact", 18)).pack(pady=25)
        self.crear_boton(ventana, "Triángulo Rectángulo", self.ventana_tri_rec_que_lados).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Triángulo Oblicuángulo", self.ventana_tri_oblic_que_lados).pack(pady=8, fill="x", padx=50)

    # ----------------------- VENTANAS TRIANGULO RECTANGULO ---------------------------------
    def ventana_tri_rec_que_lados(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Triángulo Rectángulo")
        ventana.geometry("400x300")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Selecciona los datos a ingresar", ("Impact", 18)).pack(pady=25)
        self.crear_boton(ventana, "Cateto y Cateto", self.ventana_tri_rec_CyC).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Hipotenusa y Cateto", self.ventana_tri_rec_HyC).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Lado y Ángulo agudo", self.ventana_tri_rec_LyA).pack(pady=8, fill="x", padx=50)
    '''
        LÓGICA DE PROGRAMACIÓN MATEMÁTICA (RECI_LyL):
        -----------------------------------------------------------------------
        Entradas posibles (Pedir al usuario identificar si introduce Catetos o Hipotenusa):
        - Opción A: Cateto_a, Cateto_b
        - Opción B: Hipotenusa_c, Cateto_a

        Cálculos matemáticos:
        SI es Opción A (Dos Catetos):
            1. Hipotenusa: c = math.sqrt(a**2 + b**2)
            2. Ángulo A: alpha = math.degrees(math.atan(a / b))
            3. Ángulo B: beta = 90 - alpha
        SI es Opción B (Hipotenusa y un Cateto):
            1. Cateto faltante: b = math.sqrt(c**2 - a**2)
            2. Ángulo A: alpha = math.degrees(math.asin(a / c))
            3. Ángulo B: beta = 90 - alpha
        
        Nota de validación: Si es Opción B, 'c' debe ser estrictamente mayor que 'a'.
        El tercer ángulo siempre es C = 90°.
    '''
    def ventana_tri_rec_CyC(self):
        # Ventana sencilla sin panel de gráfica
        ventana = tk.Toplevel(self.root)
        ventana.title("Triángulo Rectángulo - Catetos")
        ventana.geometry("380x380")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Dos Catetos", ("Impact", 16)).pack(
            pady=10
        )

        # Entradas para los catetos
        self.crear_etiqueta(ventana, "Cateto a:").pack()
        caja_a = tk.Entry(ventana, width=10, justify="center")
        caja_a.pack(pady=4)

        self.crear_etiqueta(ventana, "Cateto b:").pack()
        caja_b = tk.Entry(ventana, width=10, justify="center")
        caja_b.pack(pady=4)

        resultado = self.crear_etiqueta(ventana, "Resultados:")
        self.vincular_enter([caja_a, caja_b], calcular)
        def calcular():
            try:
                a = self.leer_numero(caja_a)
                b = self.leer_numero(caja_b)

                if a <= 0 or b <= 0:
                    messagebox.showerror(
                        "Error", "Los catetos deben ser mayores a 0."
                    )
                    return

                # Cálculos matemáticos
                c = math.sqrt(a**2 + b**2)
                alpha = math.degrees(math.atan(a / b))
                beta = 90 - alpha

                # Mostrar datos formateados a 2 decimales
                resultado.config(
                    text=f"Hipotenusa (c): {c:.2f}\n"
                    f"Ángulo A (α): {alpha:.2f}°\n"
                    f"Ángulo B (β): {beta:.2f}°\n"
                    f"Ángulo C (γ): 90.00°"
                )
            except ValueError:
                messagebox.showerror(
                    "Error", "Escribe valores numéricos válidos."
                )

        self.crear_boton(ventana, "Calcular", calcular).pack(pady=12)
        resultado.pack(pady=10)

    def ventana_tri_rec_HyC(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Rectángulo - Hipotenusa y Cateto", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Rectángulo", ("Impact", 16)).pack(pady=5)

        caja_c = self.crear_campo(panel_izq, "Hipotenusa (c):", "5")
        caja_a = self.crear_campo(panel_izq, "Cateto conocido (a):", "3")

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def calcular():
            try:
                c = self.leer_numero(caja_c)
                a = self.leer_numero(caja_a)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if c <= 0 or a <= 0:
                messagebox.showerror("Error", "Los lados deben ser mayores a 0.")
                return

            if c <= a:
                messagebox.showerror("Error", "La hipotenusa debe ser mayor que el cateto.")
                return

            # Cálculos matemáticos
            b = math.sqrt(c**2 - a**2)
            alpha = math.degrees(math.asin(a / c))
            beta = 90 - alpha

            resultado.config(text=f"Cateto a: {a:.2f}\n"
                                  f"Cateto b: {b:.2f}\n"
                                  f"Hipotenusa (c): {c:.2f}\n"
                                  f"Ángulo A (α): {alpha:.2f}°\n"
                                  f"Ángulo B (β): {beta:.2f}°\n"
                                  f"Ángulo C (γ): 90.00°")

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_c, caja_a], calcular)

    def ventana_tri_rec_LyA(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Rectángulo - Lado y Ángulo", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Rectángulo", ("Impact", 16)).pack(pady=5)

        caja_lado = self.crear_campo(panel_izq, "Lado conocido:", "10")
        caja_alpha = self.crear_campo(panel_izq, "Ángulo agudo α (en grados):", "30")

        self.crear_etiqueta(panel_izq, "El lado conocido es:").pack(pady=(10, 0))
        tipo_lado = self.crear_opciones(panel_izq, ["Hipotenusa",
                                                    "Cateto opuesto a α",
                                                    "Cateto adyacente a α"])

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def calcular():
            try:
                lado = self.leer_numero(caja_lado)
                alpha = self.leer_numero(caja_alpha)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if lado <= 0:
                messagebox.showerror("Error", "El lado debe ser mayor a 0.")
                return

            if alpha <= 0 or alpha >= 90:
                messagebox.showerror("Error", "El ángulo agudo debe estar entre 0° y 90°.")
                return

            beta = 90 - alpha
            alpha_rad = math.radians(alpha)   # sin, cos y tan trabajan con radianes

            # a = cateto opuesto a α,  b = cateto adyacente a α,  c = hipotenusa
            opcion = tipo_lado.get()          # 0 = hipotenusa, 1 = opuesto, 2 = adyacente
            if opcion == 0:
                c = lado
                a = c * math.sin(alpha_rad)
                b = c * math.cos(alpha_rad)
            elif opcion == 1:
                a = lado
                c = a / math.sin(alpha_rad)
                b = a / math.tan(alpha_rad)
            else:
                b = lado
                c = b / math.cos(alpha_rad)
                a = b * math.tan(alpha_rad)

            resultado.config(text=f"Cateto a (opuesto a α): {a:.2f}\n"
                                  f"Cateto b (adyacente a α): {b:.2f}\n"
                                  f"Hipotenusa (c): {c:.2f}\n"
                                  f"Ángulo A (α): {alpha:.2f}°\n"
                                  f"Ángulo B (β): {beta:.2f}°\n"
                                  f"Ángulo C (γ): 90.00°")

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_lado, caja_alpha], calcular)

    # ----------------------- VENTANA TRIANGULO OBLICUÁNGULO ------------------------------
    def ventana_tri_oblic_que_lados(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Triángulo Oblicuángulo")   
        ventana.geometry("400x400")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Selecciona los datos a ingresar", ("Impact", 18)).pack(pady=25)
        self.crear_boton(ventana, "Lado, Lado y Lado (LLL)", self.ventana_tri_oblic_LLL).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Lado, Ángulo y Lado (LAL)", self.ventana_tri_oblic_LAL).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Ángulo, Ángulo y Lado (AAL)", self.ventana_tri_oblic_AAL).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Lado, Lado y Ángulo (LLA)", self.ventana_tri_oblic_LLA).pack(pady=8, fill="x", padx=50)

    def ventana_tri_oblic_LLL(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Oblicuángulo - LLL", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Oblicuángulo", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Ingresa los 3 Lados:").pack()

        caja_a = self.crear_campo(panel_izq, "Lado a:", "5")
        caja_b = self.crear_campo(panel_izq, "Lado b:", "6")
        caja_c = self.crear_campo(panel_izq, "Lado c:", "7")

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def calcular():
            try:
                a = self.leer_numero(caja_a)
                b = self.leer_numero(caja_b)
                c = self.leer_numero(caja_c)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if a <= 0 or b <= 0 or c <= 0:
                messagebox.showerror("Error", "Los lados deben ser mayores a 0.")
                return

            # Desigualdad triangular: cada lado debe ser menor que la suma de los otros dos
            if not (a + b > c and a + c > b and b + c > a):
                messagebox.showerror("Error", "Con esos lados no se puede formar un triángulo.")
                return

            # Ley de cosenos
            cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
            cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
            A = math.degrees(math.acos(cos_A))
            B = math.degrees(math.acos(cos_B))
            C = 180 - A - B

            resultado.config(text=f"Ángulo A (α): {A:.2f}°\n"
                                  f"Ángulo B (β): {B:.2f}°\n"
                                  f"Ángulo C (γ): {C:.2f}°")

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_a, caja_b, caja_c], calcular)

    def ventana_tri_oblic_LAL(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Oblicuángulo - LAL", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Oblicuángulo", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Ingresa Lado, Ángulo y Lado:").pack()

        caja_a = self.crear_campo(panel_izq, "Lado a:", "5")
        caja_C = self.crear_campo(panel_izq, "Ángulo C (entre a y b, en grados):", "60")
        caja_b = self.crear_campo(panel_izq, "Lado b:", "8")

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def calcular():
            try:
                a = self.leer_numero(caja_a)
                C = self.leer_numero(caja_C)
                b = self.leer_numero(caja_b)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if a <= 0 or b <= 0:
                messagebox.showerror("Error", "Los lados deben ser mayores a 0.")
                return

            if C <= 0 or C >= 180:
                messagebox.showerror("Error", "El ángulo debe estar entre 0° y 180°.")
                return

            # Ley de cosenos para el lado que falta
            c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(math.radians(C)))

            # Ley de cosenos otra vez para un ángulo, y el último sale con 180 - ...
            cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
            A = math.degrees(math.acos(cos_A))
            B = 180 - A - C

            resultado.config(text=f"Lado c: {c:.2f}\n"
                                  f"Ángulo A (α): {A:.2f}°\n"
                                  f"Ángulo B (β): {B:.2f}°\n"
                                  f"Ángulo C (γ): {C:.2f}°")

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_a, caja_C, caja_b], calcular)

    def ventana_tri_oblic_AAL(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Oblicuángulo - AAL", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Oblicuángulo", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Ingresa dos Ángulos y un Lado:").pack()

        caja_A = self.crear_campo(panel_izq, "Ángulo A (en grados):", "40")
        caja_B = self.crear_campo(panel_izq, "Ángulo B (en grados):", "60")
        caja_lado = self.crear_campo(panel_izq, "Lado conocido:", "10")

        self.crear_etiqueta(panel_izq, "El lado conocido es:").pack(pady=(10, 0))
        tipo_lado = self.crear_opciones(panel_izq, ["Lado a (opuesto a A)",
                                                    "Lado b (opuesto a B)",
                                                    "Lado c (opuesto a C)"])

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def calcular():
            try:
                A = self.leer_numero(caja_A)
                B = self.leer_numero(caja_B)
                lado = self.leer_numero(caja_lado)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if A <= 0 or B <= 0 or lado <= 0:
                messagebox.showerror("Error", "Los ángulos y el lado deben ser mayores a 0.")
                return

            if A + B >= 180:
                messagebox.showerror("Error", "La suma de A y B debe ser menor a 180°.")
                return

            C = 180 - A - B

            # Ley de senos: lado / sen(su ángulo opuesto) vale lo mismo para los 3 lados.
            angulos = [A, B, C]
            angulo_opuesto = angulos[tipo_lado.get()]   # 0 = a, 1 = b, 2 = c
            constante = lado / math.sin(math.radians(angulo_opuesto))

            a = constante * math.sin(math.radians(A))
            b = constante * math.sin(math.radians(B))
            c = constante * math.sin(math.radians(C))

            resultado.config(text=f"Lado a: {a:.2f}\n"
                                  f"Lado b: {b:.2f}\n"
                                  f"Lado c: {c:.2f}\n"
                                  f"Ángulo A (α): {A:.2f}°\n"
                                  f"Ángulo B (β): {B:.2f}°\n"
                                  f"Ángulo C (γ): {C:.2f}°")

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_A, caja_B, caja_lado], calcular)

    def ventana_tri_oblic_LLA(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Oblicuángulo - LLA", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Oblicuángulo", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Ingresa Lado, Lado y Ángulo:").pack()

        caja_a = self.crear_campo(panel_izq, "Lado a:", "8")
        caja_b = self.crear_campo(panel_izq, "Lado b:", "10")
        caja_A = self.crear_campo(panel_izq, "Ángulo A (opuesto a a, en grados):", "30")

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def calcular():
            try:
                a = self.leer_numero(caja_a)
                b = self.leer_numero(caja_b)
                A = self.leer_numero(caja_A)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            if a <= 0 or b <= 0:
                messagebox.showerror("Error", "Los lados deben ser mayores a 0.")
                return

            if A <= 0 or A >= 180:
                messagebox.showerror("Error", "El ángulo debe estar entre 0° y 180°.")
                return

            # Ley de senos para buscar el ángulo B
            sin_B = b * math.sin(math.radians(A)) / a

            if sin_B > 1.000000001:
                messagebox.showerror("Error", "No existe ningún triángulo con esos datos.")
                return

            if sin_B > 1:
                sin_B = 1        # corrige errores muy pequeños de redondeo

            # Posibles valores de B: uno agudo y (casi siempre) otro obtuso
            B1 = math.degrees(math.asin(sin_B))
            posibles_B = [B1]
            if sin_B < 0.999999999:
                posibles_B.append(180 - B1)

            # Nos quedamos solo con los que sí forman triángulo (el ángulo C debe ser positivo)
            soluciones = []
            for B in posibles_B:
                C = 180 - A - B
                if C > 0.000000001:
                    c = a * math.sin(math.radians(C)) / math.sin(math.radians(A))
                    soluciones.append((B, C, c))

            if len(soluciones) == 0:
                messagebox.showerror("Error", "No existe ningún triángulo con esos datos.")
                return

            texto = f"Soluciones encontradas: {len(soluciones)}\n"
            for i in range(len(soluciones)):
                B, C, c = soluciones[i]
                texto += (f"\nSolución {i + 1}:\n"
                          f"  Lado c: {c:.2f}\n"
                          f"  Ángulo B (β): {B:.2f}°\n"
                          f"  Ángulo C (γ): {C:.2f}°\n")
            resultado.config(text=texto)

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_a, caja_b, caja_A], calcular)


# -------------- CORRER EL PROGRAMA ----------------
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AplicacionGraficas(ventana_principal)
    ventana_principal.mainloop()