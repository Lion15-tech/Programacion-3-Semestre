# =============================================================================
# GRÁFICAS Y ECUACIONES - VERSIÓN EN CLASE
# -----------------------------------------------------------------------------
# Reorganizado dentro de una clase principal (AplicacionGraficas) manteniendo
# exactamente la misma lógica, interfaz y comportamiento original.
# =============================================================================
#
# RESUMEN DE CÓMO FUNCIONA TODO EL PROGRAMA (para explicarlo en el examen):
#
#   1. Se crea una ventana principal (root) con 4 botones.
#   2. Cada botón abre una ventana nueva (Toplevel) con cajas de texto (Entry).
#   3. Al presionar el botón de la ventana (o Enter en la última caja), se
#      ejecuta una función interna (graficar / calcular) que:
#         a) LEE los números de las cajas        -> leer_numero()
#         b) VALIDA que tengan sentido           -> if ... messagebox.showerror
#         c) CALCULA con fórmulas matemáticas    -> math / numpy
#         d) MUESTRA el resultado en un Label y, si aplica, dibuja una gráfica
#   4. Todo lo que se repite (botones, etiquetas, cajas, Enter, etc.) está en
#      métodos "ayudantes" para no escribir el mismo código muchas veces.
# =============================================================================

import tkinter as tk                  # Para crear ventanas, botones, etc.
# "as tk" es un apodo: así escribimos tk.Button en vez de tkinter.Button.
from tkinter import messagebox        # Para mostrar mensajes de error
# messagebox son las ventanitas emergentes (ej. messagebox.showerror).
import numpy as np                    # Para cálculos matemáticos
# numpy lo usamos para: arreglos (np.array), resolver sistemas de ecuaciones
# (np.linalg.solve), determinantes (np.linalg.det), listas de números
# parejos (np.linspace) y mallas para planos 3D (np.meshgrid).
from matplotlib.figure import Figure  # Para crear las gráficas
# Figure es el "lienzo en blanco" donde se dibuja la gráfica.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Para meter una gráfica dentro de una ventana de Tkinter
# FigureCanvasTkAgg es el "puente" entre matplotlib y tkinter: convierte una
# Figure en un widget que Tkinter sí puede mostrar dentro de un Frame.
import os
# os sirve para trabajar con rutas de archivos (lo usamos para encontrar el logo).
import math 
# math trae las funciones matemáticas básicas: sqrt (raíz), sin, cos, tan,
# asin, acos, atan, radians, degrees. La usamos en los triángulos.

# Una CLASE es un "molde" que agrupa datos (colores, la ventana principal) y
# funciones (métodos) que trabajan con esos datos. Así todos los métodos
# pueden compartir los colores usando "self".
class AplicacionGraficas:
    # __init__ es el "constructor": se ejecuta automáticamente UNA vez cuando
    # creamos la aplicación (ver el final del archivo: AplicacionGraficas(...)).
    # "self" = la propia aplicación; "root" = la ventana principal de tkinter.
    def __init__(self, root):
        # Guardamos root en self para poder usarlo en otros métodos
        # (por ejemplo para crear ventanas hijas con tk.Toplevel(self.root)).
        self.root = root

        # Colores guardados en variables de instancia
        # (se escriben en MAYÚSCULAS por costumbre: significa "no se van a cambiar").
        # Los colores están en formato hexadecimal: #RRGGBB (rojo, verde, azul).
        self.COLOR_FONDO = "#BCF6BC"            # Verde claro
        self.COLOR_TITULO = "#1E4620"           # Verde oscuro
        self.COLOR_BOTON = "#2E7D32"            # Verde de los botones
        self.COLOR_BOTON_PRESIONADO = "#1B5E20" # Verde más oscuro al hacer clic

        # Configurar la ventana principal
        self.root.title("Gráficas y Ecuaciones - CECYTEQ")   # texto de la barra superior
        self.root.geometry("400x420")                         # ancho x alto en píxeles
        self.root.config(bg=self.COLOR_FONDO)                 # bg = background (color de fondo)

        # Título: crear_etiqueta crea el Label y .pack() lo coloca en la ventana.
        # pady=30 deja 30 píxeles de espacio vertical arriba y abajo.
        self.crear_etiqueta(self.root, "Gráficas y Ecuaciones", ("Impact", 22)).pack(pady=30)

        # Cada botón llama a la función de su ventana
        # OJO: se escribe self.ventana_primer_grado SIN paréntesis, porque no
        # queremos ejecutarla ahora, sino guardarla para que se ejecute al hacer clic.
        # fill="x" estira el botón a lo ancho; padx=50 deja margen a los lados.
        self.crear_boton(self.root, "Gráfica de primer grado\n(recta)", self.ventana_primer_grado).pack(pady=10, fill="x", padx=50)
        self.crear_boton(self.root, "Gráfica de segundo grado\n(parábola)", self.ventana_segundo_grado).pack(pady=10, fill="x", padx=50)
        self.crear_boton(self.root, "Sistemas de ecuaciones", self.ventana_sistemas).pack(pady=10, fill="x", padx=50)
        self.crear_boton(self.root, "Triángulos", self.ventana_triangulos).pack(pady=10, fill="x", padx=50)


        #### CONFIGURACIÓN DEL ICONO ####
        # Obtiene la ruta de la carpeta actual donde está el script para cargar el logo
        # __file__ = ruta de este archivo .py; dirname() se queda solo con la carpeta.
        self.carpeta_proyecto = os.path.dirname(__file__)
        # os.path.join une carpeta + nombre de archivo con el separador correcto
        # (\ en Windows, / en Linux/Mac).
        self.ruta_icono = os.path.join(self.carpeta_proyecto, "logo_cecyteq.png")
        # try/except: si la imagen no existe, el programa NO se cae; solo imprime el error.
        try:
            self.icono = tk.PhotoImage(file=self.ruta_icono)   # carga la imagen
            self.root.iconphoto(True, self.icono)              # la pone como icono de la ventana
        except Exception as e:
            print(f"Error al cargar el icono: {e}")



    # =========================================================================
    #                    MÉTODOS AYUDANTES (se usan en todas las ventanas)
    # =========================================================================

    def crear_boton(self, padre, texto, comando):
        """Crea un botón verde. 'comando' es la función que se ejecuta al hacer clic."""
        # "padre" = el contenedor donde vivirá el botón (una ventana o un Frame).
        boton = tk.Button(padre, text=texto, command=comando,
                          font=("Helvetica", 11, "bold"),          # (tipo de letra, tamaño, estilo)
                          bg=self.COLOR_BOTON, fg="white",         # bg = fondo, fg = color del texto
                          activebackground=self.COLOR_BOTON_PRESIONADO,  # color mientras se mantiene el clic
                          activeforeground="white",
                          cursor="hand2", bd=0, pady=8)            # cursor de manita, sin borde, relleno vertical
        # Devolvemos el botón SIN hacer pack: quien lo llame decide cómo colocarlo.
        return boton

    def crear_etiqueta(self, padre, texto, fuente=("Helvetica", 11)):
        """Crea un texto (Label) con los colores del programa."""
        # fuente=("Helvetica", 11) es un valor por defecto: si no se manda
        # fuente, usa ese. justify="left" alinea a la izquierda si hay varias líneas.
        return tk.Label(padre, text=texto, font=fuente, justify="left",
                        bg=self.COLOR_FONDO, fg=self.COLOR_TITULO)

    def  crear_ventana(self, titulo, tamano):
        """Crea una ventana nueva dividida en dos partes:
        - panel_izq: donde van las cajas de texto, el botón y los resultados.
        - panel_graf: donde se dibuja la gráfica.
        Devuelve esos dos paneles."""
        ventana = tk.Toplevel(self.root)  # Toplevel = ventana secundaria
        # (si usáramos tk.Tk() otra vez tendríamos dos programas separados)
        ventana.title(titulo)
        ventana.geometry(tamano)          # Ejemplo: "750x520" (ancho x alto)
        ventana.config(bg=self.COLOR_FONDO)

        # Frame = caja contenedora invisible para ordenar widgets.
        # padx/pady dentro de Frame = margen interior.
        # side="left" lo pega a la izquierda; fill="y" lo estira de arriba a abajo.
        panel_izq = tk.Frame(ventana, bg=self.COLOR_FONDO, padx=15, pady=15)
        panel_izq.pack(side="left", fill="y")

        # El panel de la gráfica ocupa TODO el espacio que sobra (expand + fill="both").
        panel_graf = tk.Frame(ventana, bg="white")
        panel_graf.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        # Una función puede devolver 2 cosas a la vez (se reciben así:
        # panel_izq, panel_graf = self.crear_ventana(...)).
        return panel_izq, panel_graf

    def leer_numero(self, caja):
        """Lee el texto de una caja y lo convierte en número.
        Cambia la coma por punto, así "2,5" también funciona.
        Si el texto no es un número, float() provoca un ValueError
        (el error se atrapa después con try/except)."""
        # caja.get() devuelve lo que el usuario escribió, SIEMPRE como texto (str).
        # .replace(",", ".") cambia la coma decimal por punto.
        texto = caja.get().replace(",", ".")
        # float() convierte texto a número decimal. Si escribió "hola" -> ValueError.
        return float(texto)

    def leer_fila(self, cajas):
        """Lee TODAS las cajas de una lista y devuelve una lista de números."""
        numeros = []                                   # lista vacía donde guardaremos los números
        for caja in cajas:                             # recorre cada caja de la lista
            numeros.append(self.leer_numero(caja))     # la lee y agrega el número a la lista
        return numeros                                 # ej. [1.0, 1.0, 5.0]

    def crear_fila_punto(self, panel, letra, x_inicial, y_inicial):
        """Crea una línea con la forma:  A ( [x] , [y] )  y devuelve las dos cajas."""
        # Cada fila es su propio Frame para poder poner todo "de lado" (side="left")
        # sin mezclarse con las demás filas.
        fila = tk.Frame(panel, bg=self.COLOR_FONDO)
        fila.pack(pady=4)

        self.crear_etiqueta(fila, letra + " (").pack(side="left")      # "A ("

        # Entry = caja de texto de una línea. width=5 -> ancho de 5 caracteres.
        caja_x = tk.Entry(fila, width=5, justify="center")
        caja_x.insert(0, x_inicial)       # insert(posición, texto): pone el valor de ejemplo
        caja_x.pack(side="left")

        self.crear_etiqueta(fila, ",").pack(side="left")

        caja_y = tk.Entry(fila, width=5, justify="center")
        caja_y.insert(0, y_inicial)
        caja_y.pack(side="left")

        self.crear_etiqueta(fila, ")").pack(side="left")

        # Se devuelven las cajas porque después hay que leer lo que escriba el usuario.
        return caja_x, caja_y

    def crear_fila_ecuacion(self, panel, textos, valores):
        """Crea una ecuación con cajas de texto, por ejemplo:  [1] x + [1] y = [5]"""
        # "valores" = números iniciales de cada caja, ej. ["1", "1", "5"]
        # "textos"  = lo que va DESPUÉS de cada caja, ej. ["x +", "y ="]
        # Siempre hay una caja más que textos (la última caja no lleva texto).
        fila = tk.Frame(panel, bg=self.COLOR_FONDO)
        fila.pack(pady=4)

        cajas = []
        for i in range(len(valores)):             # i = 0, 1, 2... (una vuelta por caja)
            caja = tk.Entry(fila, width=5, justify="center")
            caja.insert(0, valores[i])
            caja.pack(side="left")
            cajas.append(caja)                    # guardamos la caja en la lista

            # Solo ponemos texto si todavía quedan textos (la última caja no tiene)
            if i < len(textos):
                self.crear_etiqueta(fila, textos[i]).pack(side="left")

        return cajas      # lista de Entry, en el orden en que aparecen

    def vincular_enter(self, lista_cajas, funcion_graficar):
        """Hace que al presionar Enter en una caja pase a la siguiente.
        Al presionar Enter en la última caja, ejecuta la función de graficar/resolver."""
        # Función interna: recibe el evento (event, que trae info de la tecla;
        # aquí no la usamos) y el índice de la caja donde se presionó Enter.
        def al_presionar_enter(event, indice):
            if indice < len(lista_cajas) - 1:
                # No es la última caja: manda el cursor a la siguiente.
                # focus_set() = "pon el cursor de escritura en esta caja".
                lista_cajas[indice + 1].focus_set()
            else:
                # Es la última: ejecuta calcular/graficar (con paréntesis, aquí sí se ejecuta).
                funcion_graficar()

        # enumerate() da el número (i) y la caja al mismo tiempo: (0, caja0), (1, caja1)...
        for i, caja in enumerate(lista_cajas):
            # bind("<Return>", ...) = "cuando se presione Enter en esta caja, haz esto".
            # lambda e, idx=i: ... es una mini-función. Se escribe "idx=i" para
            # GUARDAR el valor actual de i; si no, todas las cajas usarían el
            # último valor de i y el Enter se comportaría mal.
            caja.bind("<Return>", lambda e, idx=i: al_presionar_enter(e, idx))

    def mostrar_figura(self, figura, panel):
        """Mete la gráfica (figura) dentro de un panel de Tkinter."""
        # Primero borramos lo que hubiera en el panel (la gráfica anterior),
        # si no, cada vez que graficas se apilarían muchas gráficas.
        # winfo_children() = lista de todos los widgets que hay dentro del panel.
        for widget in panel.winfo_children():
            widget.destroy()

        # Convertimos la Figure de matplotlib en algo que Tkinter pueda mostrar.
        lienzo = FigureCanvasTkAgg(figura, master=panel)   # master = dónde va a vivir
        lienzo.draw()                                      # dibuja la gráfica
        # get_tk_widget() da el widget de Tkinter, ahora sí se puede hacer pack.
        lienzo.get_tk_widget().pack(expand=True, fill="both")

    def decorar_ejes(self, ax, titulo):
        """Agrega a una gráfica 2D los ejes, la cuadrícula, los títulos y la leyenda."""
        # "ax" (axes) = el área de dibujo dentro de la figura donde se grafica.
        ax.axhline(0, color="black", linewidth=1)     # línea horizontal en y = 0 (eje X)
        ax.axvline(0, color="black", linewidth=1)     # línea vertical en x = 0 (eje Y)
        ax.grid(True, linestyle="--", alpha=0.6)      # cuadrícula punteada; alpha = transparencia
        ax.set_title(titulo, fontweight="bold")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.legend(fontsize=8)     # muestra los "label=" que se pusieron al graficar

    def marcar_puntos(self, ax, puntos, letras):
        """Dibuja los puntos que escribió el usuario, con su letra y coordenadas."""
        # puntos = [(x1, y1), (x2, y2)...]   letras = ["A", "B"...]
        for i in range(len(puntos)):
            x, y = puntos[i]          # "desempaca" la pareja en dos variables
            # Solo el PRIMER punto lleva label, para que en la leyenda aparezca
            # "Puntos ingresados" una sola vez y no repetido.
            if i == 0:
                # "bo" = color Blue + marcador "o" (círculo). markersize = tamaño.
                ax.plot(x, y, "bo", markersize=8, label="Puntos ingresados")
            else:
                ax.plot(x, y, "bo", markersize=8)
            # ax.text escribe texto en la coordenada (x, y). {x:.1f} = 1 decimal.
            ax.text(x, y, f"  {letras[i]}({x:.1f}, {y:.1f})", color="blue", fontsize=8)

    def crear_campo(self, panel, texto, valor_inicial):
        """Crea una etiqueta con una caja de texto debajo y devuelve la caja."""
        # pady=(8, 0) = 8 píxeles de espacio ARRIBA y 0 abajo.
        self.crear_etiqueta(panel, texto).pack(pady=(8, 0))
        caja = tk.Entry(panel, width=10, justify="center")
        caja.insert(0, valor_inicial)
        caja.pack(pady=4)
        return caja

    def crear_opciones(self, panel, textos):
        """Crea botones de opción (solo se puede elegir UNO).
        Devuelve una variable: su .get() da la posición elegida (0, 1, 2...)."""
        # IntVar = variable especial de tkinter que guarda un número entero y
        # se actualiza sola cuando el usuario hace clic. value=0 -> empieza con la 1ª opción.
        eleccion = tk.IntVar(value=0)
        for i in range(len(textos)):
            # Radiobutton = circulito de selección. Todos comparten la MISMA
            # variable (variable=eleccion), por eso solo se puede elegir uno.
            # Cada uno tiene su propio value (i): al elegirlo, eleccion vale i.
            tk.Radiobutton(panel, text=textos[i], variable=eleccion, value=i,
                           bg=self.COLOR_FONDO, fg=self.COLOR_TITULO,
                           activebackground=self.COLOR_FONDO,
                           selectcolor="white", anchor="w").pack(fill="x")   # anchor="w" = texto pegado a la izquierda (west)
        return eleccion

    # ---------------------------------------------------------------------------
    #                        VENTANAS PARA EJERCICIOS
    # ---------------------------------------------------------------------------
    # ====================== ECUACIÓN DE PRIMER GRADO ===========================
    # IDEA MATEMÁTICA: una recta tiene la forma  y = m·x + b
    #   m = pendiente (cuánto sube o baja "y" por cada 1 que avanza "x")
    #   b = ordenada al origen (el valor de "y" cuando x = 0, donde cruza el eje Y)
    # Con 2 puntos A(x1, y1) y B(x2, y2) se puede encontrar m y b, y con eso graficar.
    def ventana_primer_grado(self):
        panel_izq, panel_graf = self.crear_ventana("Ecuación de primer grado", "750x520")

        self.crear_etiqueta(panel_izq, "Ecuación Lineal", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Escribe 2 puntos (x, y)").pack()

        # caja_x1 = caja donde se escribe la coordenada x del punto 1 (A), etc.
        # Los números "0", "-4"... son valores de ejemplo que aparecen al abrir.
        caja_x1, caja_y1 = self.crear_fila_punto(panel_izq, "A", "0", "-4")
        caja_x2, caja_y2 = self.crear_fila_punto(panel_izq, "B", "3", "2")

        # Label donde se escribirán los resultados. Aún no se coloca (pack) aquí;
        # se coloca al final, DESPUÉS del botón, para que quede debajo de él.
        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        # Función interna: se ejecuta al presionar el botón (o Enter en la última caja).
        # Puede usar caja_x1, resultado, panel_graf... porque está dentro del método.
        def graficar():
            # 1) LEER. Si alguna caja no tiene un número, float() lanza ValueError
            #    y "except" muestra el mensaje y termina la función con return.
            try:
                x1 = self.leer_numero(caja_x1)
                y1 = self.leer_numero(caja_y1)
                x2 = self.leer_numero(caja_x2)
                y2 = self.leer_numero(caja_y2)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            # 2) VALIDAR: con dos puntos iguales no se puede definir una recta.
            if x1 == x2 and y1 == y2:
                messagebox.showerror("Error", "Los dos puntos son iguales. Escribe dos puntos distintos.")
                return

            # 3) Crear el "lienzo" de la gráfica. figsize = (ancho, alto) en pulgadas;
            #    dpi = puntos por pulgada (calidad). add_subplot(111) crea UN área
            #    de dibujo (1 fila, 1 columna, posición 1) y la llamamos "ax".
            figura = Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111)

            # CASO ESPECIAL: misma x en los dos puntos = recta VERTICAL.
            # Aquí no se puede calcular la pendiente porque dividiríamos entre 0
            # (x2 - x1 = 0). Su ecuación es simplemente  x = número.
            if x1 == x2:
                # axvline dibuja una línea vertical en x = x1
                ax.axvline(x1, color="green", linewidth=2, label=f"x = {x1:.2f}")
                # set_xlim / set_ylim fijan el rango visible de cada eje.
                # min(x1, 0) y max(x1, 0) aseguran que el 0 también se vea.
                ax.set_xlim(min(x1, 0) - 3, max(x1, 0) + 3)
                ax.set_ylim(min(y1, y2, 0) - 3, max(y1, y2, 0) + 3)
                resultado.config(text=f"Recta vertical: x = {x1:.2f}\n"
                                      f"Pendiente: indefinida\n"
                                      f"Intersección X: ({x1:.2f}, 0)")
            else:
                # PENDIENTE: m = (cambio en y) / (cambio en x) = (y2 - y1) / (x2 - x1)
                m = (y2 - y1) / (x2 - x1)
                # ORDENADA AL ORIGEN: como el punto A cumple  y1 = m·x1 + b,
                # despejamos b:  b = y1 - m·x1
                b = y1 - m * x1

                # lista_x guarda las x importantes para decidir qué parte
                # de la recta dibujar (los puntos, el cruce con Y que está en x=0...)
                lista_x = [x1, x2, 0]

                if m != 0:
                    # RAÍZ = donde la recta cruza el eje X, o sea y = 0:
                    #   0 = m·x + b   ->   x = -b / m
                    raiz = -b / m
                    lista_x.append(raiz)
                    texto_raiz = f"Raíz (cruce con X): ({raiz:.2f}, 0)"
                else:
                    # Si m = 0 la recta es horizontal: nunca cruza el eje X
                    # (o es el eje X mismo), por eso no hay una sola raíz.
                    texto_raiz = "Raíz: no tiene una sola (recta horizontal)"

                # Dejamos 2 unidades de margen a cada lado del valor más chico y más grande.
                x_min = min(lista_x) - 2
                x_max = max(lista_x) + 2

                # np.linspace(inicio, fin, cantidad) crea 100 valores de x
                # igualmente separados entre x_min y x_max.
                x = np.linspace(x_min, x_max, 100)
                # Con numpy la operación se hace para los 100 valores de golpe:
                # y es otra lista de 100 números, uno por cada x.
                y = m * x + b

                # {m:.2f} = m con 2 decimales.  {b:+.2f} = b con 2 decimales y
                # SIEMPRE con signo (+ o -), así se lee  "y = 2.00x -4.00".
                ax.plot(x, y, color="green", linewidth=2, label=f"y = {m:.2f}x {b:+.2f}")
                # "go" = Green + "o" (círculo): marca el cruce con el eje Y en (0, b)
                ax.plot(0, b, "go", label=f"Cruce con Y (0, {b:.2f})")
                if m != 0:
                    # "ro" = Red + círculo: marca la raíz en (raiz, 0)
                    ax.plot(raiz, 0, "ro", label=f"Raíz ({raiz:.2f}, 0)")
                ax.set_xlim(x_min, x_max)

                resultado.config(text=f"y = {m:.2f}x {b:+.2f}\n"
                                      f"Pendiente (m): {m:.2f}\n"
                                      f"Ordenada al origen (b): {b:.2f}\n"
                                      f"{texto_raiz}")

            # Se dibujan los puntos A y B, los ejes/cuadrícula/leyenda y se
            # mete la figura terminada en el panel derecho de la ventana.
            self.marcar_puntos(ax, [(x1, y1), (x2, y2)], ["A", "B"])
            self.decorar_ejes(ax, "Gráfica de la recta")
            self.mostrar_figura(figura, panel_graf)

        # command=graficar (sin paréntesis) -> se ejecuta al hacer clic.
        self.crear_boton(panel_izq, "Graficar", graficar).pack(pady=15, fill="x")
        # anchor="w" pega el texto a la izquierda (w = west/oeste).
        resultado.pack(anchor="w")
        # Enter pasa de caja en caja y en la última ejecuta graficar.
        self.vincular_enter([caja_x1, caja_y1, caja_x2, caja_y2], graficar)

    # ========================= PARÁBOLA (SEGUNDO GRADO) ==========================
    # IDEA MATEMÁTICA: una parábola tiene la forma  y = a·x² + b·x + c
    # Hay 3 incógnitas (a, b, c), por eso necesitamos 3 puntos. Cada punto
    # (x, y) da una ecuación:
    #       a·x1² + b·x1 + c = y1
    #       a·x2² + b·x2 + c = y2
    #       a·x3² + b·x3 + c = y3
    # Eso es un SISTEMA 3x3 que se resuelve con numpy (como en sistemas de ecuaciones).
    def ventana_segundo_grado(self):
        panel_izq, panel_graf = self.crear_ventana("Ecuación de segundo grado", "750x580")

        self.crear_etiqueta(panel_izq, "Ecuación Cuadrática", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Escribe 3 puntos (x, y)\ncon valores de X distintos").pack()

        caja_x1, caja_y1 = self.crear_fila_punto(panel_izq, "A", "-1", "0")
        caja_x2, caja_y2 = self.crear_fila_punto(panel_izq, "B", "0", "-3")
        caja_x3, caja_y3 = self.crear_fila_punto(panel_izq, "C", "3", "0")

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def graficar():
            # 1) LEER los 6 números (si alguno no es número -> mensaje y salir)
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

            # 2) VALIDAR: si dos puntos tienen la misma x, una parábola no puede
            #    pasar por ambos (sería una función con dos y para la misma x).
            #    set() quita los repetidos: si quedan menos de 3 valores, había repetidos.
            if len(set([x1, x2, x3])) < 3:
                messagebox.showerror("Error", "Los 3 puntos deben tener valores de X distintos.")
                return

            # 3) PLANTEAR EL SISTEMA  matriz · [a, b, c] = valores_y
            #    Cada fila de la matriz es [x², x, 1] de un punto (los coeficientes
            #    de a, b y c en su ecuación).
            matriz = np.array([[x1**2, x1, 1],
                               [x2**2, x2, 1],
                               [x3**2, x3, 1]])
            # Lado derecho del sistema: las y de los 3 puntos.
            valores_y = np.array([y1, y2, y3])
            # np.linalg.solve resuelve el sistema y devuelve los 3 valores [a, b, c].
            a, b, c = np.linalg.solve(matriz, valores_y)

            # Si "a" es (casi) 0, no hay término x²: los puntos están en una
            # recta. Se compara con un número muy pequeño y no con == 0 porque
            # los decimales de la computadora tienen pequeños errores de redondeo.
            if abs(a) < 0.000000001:
                messagebox.showerror("Error", "Los 3 puntos están alineados: forman una recta, no una parábola.")
                return

            # DISCRIMINANTE: d = b² - 4ac (lo que va dentro de la raíz de la fórmula general)
            #   d > 0 -> dos raíces reales | d = 0 -> una raíz | d < 0 -> raíces complejas
            d = b**2 - 4*a*c
            # VÉRTICE (punto más alto o más bajo de la parábola):
            #   x del vértice = -b / (2a);  y del vértice = se evalúa la ecuación en esa x.
            # El "+ 0" evita que Python muestre "-0.00" (convierte -0.0 en 0.0).
            vertice_x = -b / (2*a) + 0
            vertice_y = a * vertice_x**2 + b * vertice_x + c

            # RAÍCES = valores de x donde y = 0 (donde la parábola cruza el eje X).
            # Se usa la fórmula general:  x = (-b ± √d) / (2a)
            raices = []     # lista vacía; se llena según el caso
            if abs(d) < 0.000000001:
                # d ≈ 0: una sola raíz (la parábola solo "toca" el eje X en el vértice)
                r = -b / (2*a)
                raices.append(r)
                texto_raices = f"Raíz única: X = {r:.2f}"
            elif d > 0:
                # d > 0: dos raíces reales distintas (el "+" y el "-" de ±)
                # np.sqrt = raíz cuadrada
                r1 = (-b + np.sqrt(d)) / (2*a)
                r2 = (-b - np.sqrt(d)) / (2*a)
                raices.append(r1)
                raices.append(r2)
                texto_raices = f"Raíces: X1 = {r1:.2f}\n            X2 = {r2:.2f}"
            else:
                # d < 0: la raíz de un negativo no es real -> raíces complejas
                # de la forma  parte_real ± parte_imaginaria·i
                # (no se grafican porque no están en el plano real; por eso
                # "raices" se queda vacía en este caso).
                parte_real = -b / (2*a) + 0
                # Se usa -d (positivo) dentro de la raíz y abs(a) para que
                # la parte imaginaria salga positiva y los signos ± se lean bien.
                parte_imaginaria = np.sqrt(-d) / (2*abs(a))
                texto_raices = (f"Raíces complejas:\n"
                                f"  X1 = {parte_real:.2f} + {parte_imaginaria:.2f}i\n"
                                f"  X2 = {parte_real:.2f} - {parte_imaginaria:.2f}i")

            # Ecuación como texto para el resultado y la leyenda ({b:+.2f} = con signo)
            ecuacion = f"y = {a:.2f}x² {b:+.2f}x {c:+.2f}"

            resultado.config(text=f"{ecuacion}\n"
                                  f"Discriminante: {d:.2f}\n"
                                  f"Vértice: ({vertice_x:.2f}, {vertice_y:.2f})\n"
                                  f"Cruce con Y: (0, {c:.2f})\n"
                                  f"{texto_raices}")

            # Rango del eje X: abarca los 3 puntos, el vértice, el 0 y las raíces
            # (+ une dos listas en una sola). Se agregan 2 unidades de margen.
            lista_x = [x1, x2, x3, vertice_x, 0] + raices
            x_min = min(lista_x) - 2
            x_max = max(lista_x) + 2

            # 200 valores de x -> más puntos que la recta para que la curva se vea suave.
            x = np.linspace(x_min, x_max, 200)
            # Se evalúa la parábola en todos los x a la vez (numpy lo permite).
            y = a * x**2 + b * x + c

            figura = Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111)

            ax.plot(x, y, color="green", linewidth=2, label=ecuacion)
            # "D" = marcador en forma de diamante para el vértice
            ax.plot(vertice_x, vertice_y, "D", color="purple",
                    label=f"Vértice ({vertice_x:.2f}, {vertice_y:.2f})")
            # En x = 0, y vale c (por eso el cruce con Y es (0, c))
            ax.plot(0, c, "go", label=f"Cruce con Y (0, {c:.2f})")
            if len(raices) > 0:
                # [0] * len(raices) crea una lista de ceros del mismo tamaño que
                # raices (todas las raíces están en y = 0).
                ax.plot(raices, [0] * len(raices), "ro", label="Raíces")

            self.marcar_puntos(ax, [(x1, y1), (x2, y2), (x3, y3)], ["A", "B", "C"])
            self.decorar_ejes(ax, "Gráfica de la parábola")
            self.mostrar_figura(figura, panel_graf)

        self.crear_boton(panel_izq, "Graficar", graficar).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_x1, caja_y1, caja_x2, caja_y2, caja_x3, caja_y3], graficar)


    # ====================== MENÚ PARA ELEGIR 2x2 O 3x3 ===========================
    # Esta ventana solo es un MENÚ: no calcula nada, únicamente tiene dos botones
    # que abren la ventana de sistema 2x2 o la de 3x3.
    def ventana_sistemas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Sistemas de Ecuaciones")
        ventana.geometry("400x250")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Selecciona el tipo de sistema", ("Impact", 18)).pack(pady=25)
        self.crear_boton(ventana, "Sistemas de 2x2", self.ventana_sistema_2x2).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Sistemas de 3x3", self.ventana_sistema_3x3).pack(pady=8, fill="x", padx=50)

    # ============================ SISTEMA DE 2x2 =================================
    # IDEA MATEMÁTICA: un sistema 2x2 son DOS ecuaciones con DOS incógnitas (x, y):
    #       a1·x + b1·y = c1
    #       a2·x + b2·y = c2
    # Cada ecuación es una RECTA. La solución del sistema es el punto donde se
    # cruzan las dos rectas. Casos posibles:
    #   - Se cruzan en 1 punto -> solución única.
    #   - Son paralelas -> no hay solución.   - Son la misma recta -> infinitas soluciones.
    # Para saber cuál caso es se usa el DETERMINANTE de la matriz de coeficientes:
    #   det = a1·b2 - a2·b1.  Si det ≠ 0 -> hay solución única. Si det = 0 -> no la hay.
    def dibujar_recta(self, ax, a, b, c, x, color):
        """Dibuja la recta  a·x + b·y = c  sobre los ejes 'ax'."""
        if b != 0:
            # Despejamos y:   b·y = c - a·x   ->   y = (c - a·x) / b
            # "x" es la lista de valores de x (numpy), así que "y" sale como lista también.
            y = (c - a * x) / b
            # {b:+.1f} muestra el signo de b, para que se lea  "1.0x +1.0y = 5.0"
            ax.plot(x, y, color=color, linewidth=2, label=f"{a:.1f}x {b:+.1f}y = {c:.1f}")
        else:
            # Si b = 0 la ecuación queda  a·x = c  ->  x = c / a  (recta VERTICAL).
            # No se puede despejar y (dividiríamos entre 0). Aquí "a" nunca es 0
            # porque ventana_sistema_2x2 ya validó que a y b no sean 0 a la vez.
            ax.axvline(c / a, color=color, linewidth=2, linestyle="--",
                       label=f"{a:.1f}x = {c:.1f}")

    def ventana_sistema_2x2(self):
        panel_izq, panel_graf = self.crear_ventana("Sistema de ecuaciones 2x2", "800x550")

        self.crear_etiqueta(panel_izq, "Sistema de 2x2", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Forma:  ax + by = c").pack()

        # Cada fila es una LISTA de 3 cajas [a, b, c]. El primer argumento de
        # textos (["x +", "y ="]) es lo que se escribe después de cada caja.
        # Se ve así:   [1] x + [1] y = [5]
        fila1 = self.crear_fila_ecuacion(panel_izq, ["x +", "y ="], ["1", "1", "5"])
        fila2 = self.crear_fila_ecuacion(panel_izq, ["x +", "y ="], ["1", "-1", "1"])

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def graficar():
            # leer_fila devuelve una lista de 3 números y Python la "desempaca"
            # en 3 variables: a1 = 1ª caja, b1 = 2ª caja, c1 = 3ª caja.
            # El número después de cada letra indica de qué ecuación es (1 o 2).
            try:
                a1, b1, c1 = self.leer_fila(fila1)
                a2, b2, c2 = self.leer_fila(fila2)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            # Si a y b son 0 a la vez, la ecuación queda "0 = c": ya no es una recta.
            if (a1 == 0 and b1 == 0) or (a2 == 0 and b2 == 0):
                messagebox.showerror("Error", "En cada ecuación, 'a' y 'b' no pueden ser 0 a la vez.")
                return

            # matriz = coeficientes (lo que multiplica a x e y) de cada ecuación.
            # resultados = lado derecho de cada ecuación (los números c1 y c2).
            # El sistema completo se escribe:  matriz · [x, y] = resultados
            matriz = np.array([[a1, b1],
                               [a2, b2]])
            resultados = np.array([c1, c2])

            # np.linalg.det calcula el determinante de la matriz.
            determinante = np.linalg.det(matriz)
            # Se compara con un número muy pequeño (no con == 0) por los errores
            # de redondeo de los decimales en la computadora.
            hay_solucion = abs(determinante) > 0.000000001

            if hay_solucion:
                # np.linalg.solve resuelve el sistema: devuelve los valores de x e y.
                x_sol, y_sol = np.linalg.solve(matriz, resultados)
                resultado.config(text=f"Determinante: {determinante:.2f}\n"
                                      f"Punto de cruce:\n"
                                      f"  X = {x_sol:.2f}\n"
                                      f"  Y = {y_sol:.2f}")
                # "centro" es la x alrededor de la cual se dibuja la gráfica,
                # para que el punto de cruce quede en medio de la imagen.
                centro = x_sol
            else:
                resultado.config(text="No hay solución única\n(rectas paralelas o iguales)")
                centro = 0

            # 100 valores de x desde 10 unidades antes del centro hasta 10 después.
            x = np.linspace(centro - 10, centro + 10, 100)

            figura = Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111)

            # Se dibuja cada recta con un color distinto para distinguirlas.
            self.dibujar_recta(ax, a1, b1, c1, x, "green")
            self.dibujar_recta(ax, a2, b2, c2, x, "orange")

            if hay_solucion:
                # Punto rojo grande (markersize=8) en el cruce de las rectas.
                ax.plot(x_sol, y_sol, "ro", markersize=8,
                        label=f"Cruce ({x_sol:.1f}, {y_sol:.1f})")

            self.decorar_ejes(ax, "Cruce de rectas (sistema 2x2)")
            self.mostrar_figura(figura, panel_graf)

        self.crear_boton(panel_izq, "Resolver y Graficar", graficar).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        # fila1 + fila2 une las dos listas de cajas en una sola de 6 cajas,
        # así Enter recorre todas en orden: a1, b1, c1, a2, b2, c2.
        self.vincular_enter(fila1 + fila2, graficar)

    # ============================ SISTEMA DE 3x3 =================================
    # IDEA MATEMÁTICA: ahora son TRES ecuaciones con TRES incógnitas (x, y, z):
    #       a1·x + b1·y + c1·z = d1
    #       a2·x + b2·y + c2·z = d2
    #       a3·x + b3·y + c3·z = d3
    # Cada ecuación es un PLANO en 3D. La solución es el punto donde se cruzan
    # los 3 planos. Igual que en 2x2: si el determinante ≠ 0 hay un solo punto;
    # si es 0, los planos son paralelos o se cruzan en una línea (sin punto único).
    def dibujar_plano(self, ax, a, b, c, d, rango_x, rango_y, rango_z, color):
        """Dibuja el plano  a·x + b·y + c·z = d  en una gráfica 3D."""
        # Para dibujar una superficie hay que calcular el valor de UNA variable
        # a partir de las otras dos. Se elige despejar la que tenga coeficiente ≠ 0.
        if c != 0:
            # np.meshgrid arma una "malla": con rango_x (20 valores) y rango_y
            # (20 valores) crea todas las combinaciones (x, y) -> 20 x 20 puntos.
            # X e Y son tablas (matrices) con esas combinaciones.
            X, Y = np.meshgrid(rango_x, rango_y)
            # Despejamos z:  c·z = d - a·x - b·y   ->   z = (d - a·x - b·y) / c
            Z = (d - a * X - b * Y) / c
        elif b != 0:
            # Si c = 0 no se puede despejar z; el plano es vertical.
            # Despejamos y:  a·x + b·y = d  ->  y = (d - a·x) / b
            # y z puede tomar cualquier valor (por eso se usa rango_z).
            X, Z = np.meshgrid(rango_x, rango_z)
            Y = (d - a * X) / b
        else:
            # Si b y c son 0, la ecuación es  a·x = d  ->  x = d / a  (plano vertical).
            # a no es 0 porque se validó que a, b y c no sean 0 a la vez.
            Y, Z = np.meshgrid(rango_y, rango_z)
            # np.full_like(Y, valor) crea una tabla del MISMO tamaño que Y,
            # pero rellena toda con el mismo número (d / a): x es constante.
            X = np.full_like(Y, d / a)

        # plot_surface dibuja la superficie con las 3 tablas X, Y, Z.
        # alpha=0.5 la hace semitransparente para ver los otros planos.
        ax.plot_surface(X, Y, Z, alpha=0.5, color=color)

    def ventana_sistema_3x3(self):
        panel_izq, panel_graf = self.crear_ventana("Sistema de ecuaciones 3x3", "800x550")

        self.crear_etiqueta(panel_izq, "Sistema de 3x3", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Forma:  ax + by + cz = d").pack()

        # Cada fila tiene 4 cajas [a, b, c, d]:   [1] x + [1] y + [1] z = [6]
        fila1 = self.crear_fila_ecuacion(panel_izq, ["x +", "y +", "z ="], ["1", "1", "1", "6"])
        fila2 = self.crear_fila_ecuacion(panel_izq, ["x +", "y +", "z ="], ["0", "2", "5", "-4"])
        fila3 = self.crear_fila_ecuacion(panel_izq, ["x +", "y +", "z ="], ["2", "5", "-1", "27"])

        resultado = self.crear_etiqueta(panel_izq, "Resultados:")

        def graficar():
            # Se leen las 3 filas de 4 números cada una (a, b, c, d de cada plano).
            try:
                a1, b1, c1, d1 = self.leer_fila(fila1)
                a2, b2, c2, d2 = self.leer_fila(fila2)
                a3, b3, c3, d3 = self.leer_fila(fila3)
            except ValueError:
                messagebox.showerror("Error", "Escribe solo números en las cajas.")
                return

            # La "\" al final de la línea sirve para continuar la condición en la
            # siguiente línea. Si a, b y c son 0 a la vez, no es un plano.
            if (a1 == 0 and b1 == 0 and c1 == 0) or \
               (a2 == 0 and b2 == 0 and c2 == 0) or \
               (a3 == 0 and b3 == 0 and c3 == 0):
                messagebox.showerror("Error", "En cada ecuación, 'a', 'b' y 'c' no pueden ser 0 a la vez.")
                return

            # matriz 3x3 con los coeficientes (a, b, c) de cada plano, y
            # "resultados" con los números d de cada ecuación (lado derecho).
            matriz = np.array([[a1, b1, c1],
                               [a2, b2, c2],
                               [a3, b3, c3]])
            resultados = np.array([d1, d2, d3])

            # Mismo criterio que en 2x2: determinante distinto de 0 = solución única.
            determinante = np.linalg.det(matriz)
            hay_solucion = abs(determinante) > 0.000000001

            if hay_solucion:
                # solve devuelve las 3 incógnitas: x, y, z
                x_sol, y_sol, z_sol = np.linalg.solve(matriz, resultados)
                resultado.config(text=f"Determinante: {determinante:.2f}\n"
                                      f"Solución:\n"
                                      f"  X = {x_sol:.2f}\n"
                                      f"  Y = {y_sol:.2f}\n"
                                      f"  Z = {z_sol:.2f}")
                # La gráfica se centra en el punto solución.
                centro_x, centro_y, centro_z = x_sol, y_sol, z_sol
            else:
                resultado.config(text="No hay solución única\n(planos paralelos o con\ninfinitos cruces)")
                centro_x, centro_y, centro_z = 0, 0, 0

            # Rango de cada eje: 5 unidades antes y después del centro, 20 valores
            # cada uno (20 x 20 = 400 puntos por plano; suficiente y rápido).
            rango_x = np.linspace(centro_x - 5, centro_x + 5, 20)
            rango_y = np.linspace(centro_y - 5, centro_y + 5, 20)
            rango_z = np.linspace(centro_z - 5, centro_z + 5, 20)

            figura = Figure(figsize=(5, 4), dpi=100)
            # projection="3d" convierte el área de dibujo en una gráfica 3D.
            ax = figura.add_subplot(111, projection="3d")

            # Se dibuja cada plano con un color distinto.
            self.dibujar_plano(ax, a1, b1, c1, d1, rango_x, rango_y, rango_z, "green")
            self.dibujar_plano(ax, a2, b2, c2, d2, rango_x, rango_y, rango_z, "orange")
            self.dibujar_plano(ax, a3, b3, c3, d3, rango_x, rango_y, rango_z, "blue")

            # Fijamos los límites de cada eje al mismo rango usado para calcular
            # los planos, para que la gráfica no se salga de la zona dibujada.
            ax.set_xlim(centro_x - 5, centro_x + 5)
            ax.set_ylim(centro_y - 5, centro_y + 5)
            ax.set_zlim(centro_z - 5, centro_z + 5)

            if hay_solucion:
                # scatter dibuja un punto suelto en 3D. s = tamaño del punto.
                # depthshade=False evita que el punto se vea más tenue por la profundidad.
                ax.scatter(x_sol, y_sol, z_sol, color="red", s=50, depthshade=False,
                           label=f"Solución ({x_sol:.1f}, {y_sol:.1f}, {z_sol:.1f})")
                ax.legend(fontsize=8)

            # En 3D no se usa decorar_ejes (era para 2D), así que se ponen los
            # títulos de la gráfica y de los 3 ejes aquí.
            ax.set_title("Cruce de planos (sistema 3x3)", fontweight="bold")
            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.set_zlabel("Eje Z")

            self.mostrar_figura(figura, panel_graf)

        self.crear_boton(panel_izq, "Resolver Sistema", graficar).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        # Enter recorre las 12 cajas en orden y en la última resuelve.
        self.vincular_enter(fila1 + fila2 + fila3, graficar)


    # ====================== MENÚ PARA ELEGIR TRIANGULOS ===========================
    # Menú: solo tiene 2 botones que abren otros menús (rectángulo u oblicuángulo).
    def ventana_triangulos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Triángulos")
        ventana.geometry("400x300")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Selecciona el tipo de triángulo", ("Impact", 18)).pack(pady=25)
        self.crear_boton(ventana, "Triángulo Rectángulo", self.ventana_tri_rec_que_lados).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Triángulo Oblicuángulo", self.ventana_tri_oblic_que_lados).pack(pady=8, fill="x", padx=50)

    # ----------------------- VENTANAS TRIANGULO RECTANGULO ---------------------------------
    # DATOS BÁSICOS DE UN TRIÁNGULO RECTÁNGULO (tiene un ángulo de 90°):
    #   - Los lados que forman el ángulo recto se llaman CATETOS (a y b).
    #   - El lado opuesto al ángulo recto, el más largo, es la HIPOTENUSA (c).
    #   - El ángulo A (alpha, α) está frente al cateto a; el ángulo B (beta, β)
    #     frente al cateto b; el ángulo C (gamma, γ) es el recto: siempre 90°.
    #   - TEOREMA DE PITÁGORAS:  c² = a² + b²
    #   - Los 3 ángulos de cualquier triángulo suman 180°, y como C = 90°,
    #     entonces  A + B = 90°  ->  B = 90 - A.
    #   - RAZONES TRIGONOMÉTRICAS (con respecto al ángulo α):
    #         sen(α) = cateto opuesto / hipotenusa
    #         cos(α) = cateto adyacente / hipotenusa
    #         tan(α) = cateto opuesto / cateto adyacente
    #   - Para encontrar el ÁNGULO a partir de una razón se usan las funciones
    #     inversas: asin, acos, atan. Devuelven el ángulo en RADIANES, así que se
    #     convierte a grados con math.degrees().
    # Menú: pregunta qué datos conoce el usuario y abre la ventana correspondiente.
    def ventana_tri_rec_que_lados(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Triángulo Rectángulo")
        ventana.geometry("400x300")
        ventana.config(bg=self.COLOR_FONDO)

        self.crear_etiqueta(ventana, "Selecciona los datos a ingresar", ("Impact", 18)).pack(pady=25)
        self.crear_boton(ventana, "Cateto y Cateto", self.ventana_tri_rec_CyC).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Hipotenusa y Cateto", self.ventana_tri_rec_HyC).pack(pady=8, fill="x", padx=50)
        self.crear_boton(ventana, "Lado y Ángulo agudo", self.ventana_tri_rec_LyA).pack(pady=8, fill="x", padx=50)
    # El siguiente bloque entre comillas triples NO se ejecuta: es solo una nota
    # (un texto suelto) con la lógica que se planeó para los triángulos rectángulos.
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
    # ---- Triángulo rectángulo: se conocen los DOS CATETOS (a y b) ----
    def ventana_tri_rec_CyC(self):
        # Ventana sencilla sin panel de gráfica
        # (aquí se usa tk.Toplevel directo y no crear_ventana, porque no se
        # necesita el panel de la gráfica: solo se calculan datos)
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

        def calcular():
            # Aquí todo (leer, validar y calcular) está dentro de un solo try.
            # Si leer_numero falla (texto no numérico) salta al except ValueError.
            try:
                a = self.leer_numero(caja_a)
                b = self.leer_numero(caja_b)

                # Un lado de 0 o negativo no existe.
                if a <= 0 or b <= 0:
                    messagebox.showerror(
                        "Error", "Los catetos deben ser mayores a 0."
                    )
                    return

                # Cálculos matemáticos
                # Hipotenusa por Pitágoras:  c = √(a² + b²)   (math.sqrt = raíz cuadrada)
                c = math.sqrt(a**2 + b**2)
                # tan(α) = opuesto / adyacente = a / b  ->  α = atan(a / b)
                # math.atan da radianes; math.degrees los pasa a grados.
                alpha = math.degrees(math.atan(a / b))
                # Los ángulos agudos suman 90°  ->  β = 90 - α
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
        # IMPORTANTE: vincular_enter va DESPUÉS de definir calcular, porque
        # necesita recibir la función ya creada.
        self.vincular_enter([caja_a, caja_b], calcular)

    # ---- Triángulo rectángulo: se conocen la HIPOTENUSA (c) y un CATETO (a) ----
    def ventana_tri_rec_HyC(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Rectángulo - Hipotenusa y Cateto", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Rectángulo", ("Impact", 16)).pack(pady=5)

        # crear_campo = etiqueta + caja de texto. Devuelve la caja.
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

            # La hipotenusa es el lado más largo. Si c <= a, no existe el triángulo
            # (también evitaría una raíz de número negativo más abajo).
            if c <= a:
                messagebox.showerror("Error", "La hipotenusa debe ser mayor que el cateto.")
                return

            # Cálculos matemáticos
            # Pitágoras despejando el cateto que falta:  c² = a² + b²  ->  b = √(c² - a²)
            b = math.sqrt(c**2 - a**2)
            # sen(α) = opuesto / hipotenusa = a / c  ->  α = asin(a / c), pasado a grados
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

    # ---- Triángulo rectángulo: se conoce UN LADO y UN ÁNGULO AGUDO (α) ----
    def ventana_tri_rec_LyA(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Rectángulo - Lado y Ángulo", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Rectángulo", ("Impact", 16)).pack(pady=5)

        caja_lado = self.crear_campo(panel_izq, "Lado conocido:", "10")
        caja_alpha = self.crear_campo(panel_izq, "Ángulo agudo α (en grados):", "30")

        self.crear_etiqueta(panel_izq, "El lado conocido es:").pack(pady=(10, 0))
        # tipo_lado es una IntVar: .get() da 0, 1 o 2 según la opción elegida
        # (0 = Hipotenusa, 1 = Cateto opuesto, 2 = Cateto adyacente).
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

            # Un ángulo agudo mide menos de 90° (y más de 0°).
            if alpha <= 0 or alpha >= 90:
                messagebox.showerror("Error", "El ángulo agudo debe estar entre 0° y 90°.")
                return

            beta = 90 - alpha
            alpha_rad = math.radians(alpha)   # sin, cos y tan trabajan con radianes
            # math.radians pasa grados a radianes (180° = π radianes).

            # a = cateto opuesto a α,  b = cateto adyacente a α,  c = hipotenusa
            opcion = tipo_lado.get()          # 0 = hipotenusa, 1 = opuesto, 2 = adyacente
            if opcion == 0:
                # Se conoce c. Se despejan a y b de las razones trigonométricas:
                #   sen(α) = a / c  ->  a = c·sen(α)
                #   cos(α) = b / c  ->  b = c·cos(α)
                c = lado
                a = c * math.sin(alpha_rad)
                b = c * math.cos(alpha_rad)
            elif opcion == 1:
                # Se conoce a (opuesto).
                #   sen(α) = a / c  ->  c = a / sen(α)
                #   tan(α) = a / b  ->  b = a / tan(α)
                a = lado
                c = a / math.sin(alpha_rad)
                b = a / math.tan(alpha_rad)
            else:
                # Se conoce b (adyacente).
                #   cos(α) = b / c  ->  c = b / cos(α)
                #   tan(α) = a / b  ->  a = b·tan(α)
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
    # DATOS BÁSICOS: un triángulo OBLICUÁNGULO no tiene ningún ángulo de 90°.
    # No se puede usar Pitágoras ni sen/cos/tan directos, así que se usan dos leyes
    # que funcionan en CUALQUIER triángulo. Convención: el lado "a" está frente al
    # ángulo A, el lado "b" frente a B y el lado "c" frente a C.
    #
    #   LEY DE COSENOS (se parece a Pitágoras, pero con un término extra):
    #        a² = b² + c² - 2·b·c·cos(A)      (igual para b² y c²)
    #     Despejando el ángulo:   cos(A) = (b² + c² - a²) / (2·b·c)
    #     Sirve cuando se conocen 3 lados (LLL) o 2 lados y el ángulo entre ellos (LAL).
    #
    #   LEY DE SENOS (la razón lado / seno de su ángulo opuesto es la misma en los 3):
    #        a / sen(A) = b / sen(B) = c / sen(C)
    #     Sirve cuando se conoce un lado y su ángulo opuesto (AAL y LLA).
    #
    #   Los 3 ángulos siempre suman 180°  ->  el último ángulo = 180 - los otros dos.
    # Menú: pregunta qué datos conoce el usuario (L = lado, A = ángulo) y abre
    # la ventana correspondiente.
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

    # ---- LLL: se conocen los 3 lados -> se buscan los 3 ángulos (Ley de cosenos) ----
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
            # (si no, los lados no "alcanzan" a cerrarse para formar un triángulo).
            if not (a + b > c and a + c > b and b + c > a):
                messagebox.showerror("Error", "Con esos lados no se puede formar un triángulo.")
                return

            # Ley de cosenos
            # Se despeja el coseno de cada ángulo con la fórmula de arriba.
            cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
            cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
            # acos = inverso del coseno (devuelve radianes) -> degrees lo pasa a grados.
            A = math.degrees(math.acos(cos_A))
            B = math.degrees(math.acos(cos_B))
            # El tercer ángulo no necesita fórmula: los 3 suman 180°.
            C = 180 - A - B

            resultado.config(text=f"Ángulo A (α): {A:.2f}°\n"
                                  f"Ángulo B (β): {B:.2f}°\n"
                                  f"Ángulo C (γ): {C:.2f}°")

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_a, caja_b, caja_c], calcular)

    # ---- LAL: dos lados y el ángulo ENTRE ellos (a, C, b) ----
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

            # Un ángulo de un triángulo mide entre 0° y 180° (sin incluirlos).
            if C <= 0 or C >= 180:
                messagebox.showerror("Error", "El ángulo debe estar entre 0° y 180°.")
                return

            # Ley de cosenos para el lado que falta
            # c² = a² + b² - 2·a·b·cos(C)  ->  c = √(...)
            # math.cos necesita radianes, por eso math.radians(C).
            c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(math.radians(C)))

            # Ley de cosenos otra vez para un ángulo, y el último sale con 180 - ...
            # Se usa coseno (y no seno) porque acos da un único ángulo entre 0° y 180°;
            # con seno podría haber dos posibles ángulos (agudo u obtuso) y habría confusión.
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

    # ---- AAL: dos ángulos y un lado (Ley de senos) ----
    def ventana_tri_oblic_AAL(self):
        panel_izq, panel_graf = self.crear_ventana("Triángulo Oblicuángulo - AAL", "750x520")
        self.crear_etiqueta(panel_izq, "Triángulo Oblicuángulo", ("Impact", 16)).pack(pady=5)
        self.crear_etiqueta(panel_izq, "Ingresa dos Ángulos y un Lado:").pack()

        caja_A = self.crear_campo(panel_izq, "Ángulo A (en grados):", "40")
        caja_B = self.crear_campo(panel_izq, "Ángulo B (en grados):", "60")
        caja_lado = self.crear_campo(panel_izq, "Lado conocido:", "10")

        self.crear_etiqueta(panel_izq, "El lado conocido es:").pack(pady=(10, 0))
        # tipo_lado.get() = 0, 1 o 2 según el lado que el usuario diga que conoce.
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

            # Si A + B ya llega a 180°, no queda nada para el tercer ángulo.
            if A + B >= 180:
                messagebox.showerror("Error", "La suma de A y B debe ser menor a 180°.")
                return

            # El tercer ángulo sale de que los 3 suman 180°.
            C = 180 - A - B

            # Ley de senos: lado / sen(su ángulo opuesto) vale lo mismo para los 3 lados.
            # Se guardan los 3 ángulos en una lista en el MISMO orden que las opciones
            # (posición 0 = A, 1 = B, 2 = C), así la opción elegida sirve de índice.
            angulos = [A, B, C]
            angulo_opuesto = angulos[tipo_lado.get()]   # 0 = a, 1 = b, 2 = c
            # Con el lado conocido y su ángulo opuesto se calcula esa razón común.
            # Se le llama "constante" porque es el mismo valor para a, b y c.
            constante = lado / math.sin(math.radians(angulo_opuesto))

            # De  lado / sen(ángulo) = constante  se despeja:  lado = constante · sen(ángulo)
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

    # ---- LLA: dos lados y un ángulo NO comprendido entre ellos (a, b, A) ----
    # Este es el "caso ambiguo": con esos datos puede haber 0, 1 o 2 triángulos.
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
            # a / sen(A) = b / sen(B)  ->  sen(B) = b·sen(A) / a
            sin_B = b * math.sin(math.radians(A)) / a

            # Un seno nunca puede valer más de 1: si pasa, el lado "a" es muy corto
            # y no alcanza a tocar al otro lado -> no existe el triángulo.
            # Se acepta un poquito más de 1 (1.000000001) por errores de redondeo.
            if sin_B > 1.000000001:
                messagebox.showerror("Error", "No existe ningún triángulo con esos datos.")
                return

            if sin_B > 1:
                sin_B = 1        # corrige errores muy pequeños de redondeo
                                 # (asin de un número mayor a 1 daría error)

            # Posibles valores de B: uno agudo y (casi siempre) otro obtuso
            # Dos ángulos distintos tienen el mismo seno: B1 y 180° - B1.
            # Por eso puede haber dos triángulos distintos con los mismos datos.
            B1 = math.degrees(math.asin(sin_B))
            posibles_B = [B1]
            # Si sin_B es casi 1, B1 ≈ 90° y 180 - B1 ≈ 90° también: serían el
            # mismo ángulo, así que no se agrega el segundo.
            if sin_B < 0.999999999:
                posibles_B.append(180 - B1)

            # Nos quedamos solo con los que sí forman triángulo (el ángulo C debe ser positivo)
            # soluciones = lista de tuplas (B, C, c), una por cada triángulo válido.
            soluciones = []
            for B in posibles_B:
                C = 180 - A - B
                if C > 0.000000001:
                    # Ley de senos otra vez:  c / sen(C) = a / sen(A)  ->  c = a·sen(C) / sen(A)
                    c = a * math.sin(math.radians(C)) / math.sin(math.radians(A))
                    soluciones.append((B, C, c))

            # Si ninguna opción dejó C positivo, tampoco hay triángulo.
            if len(soluciones) == 0:
                messagebox.showerror("Error", "No existe ningún triángulo con esos datos.")
                return

            # Se arma un texto con TODAS las soluciones. "+=" agrega texto al final
            # del que ya hay. (i + 1) es para numerar desde 1 en vez de 0.
            texto = f"Soluciones encontradas: {len(soluciones)}\n"
            for i in range(len(soluciones)):
                B, C, c = soluciones[i]      # desempaca la tupla en 3 variables
                texto += (f"\nSolución {i + 1}:\n"
                          f"  Lado c: {c:.2f}\n"
                          f"  Ángulo B (β): {B:.2f}°\n"
                          f"  Ángulo C (γ): {C:.2f}°\n")
            resultado.config(text=texto)

        self.crear_boton(panel_izq, "Calcular", calcular).pack(pady=15, fill="x")
        resultado.pack(anchor="w")
        self.vincular_enter([caja_a, caja_b, caja_A], calcular)


# -------------- CORRER EL PROGRAMA ----------------
# "if __name__ == '__main__'" significa: "ejecuta esto solo si abrí ESTE archivo
# directamente" (y no si otro archivo lo importa).
if __name__ == "__main__":
    ventana_principal = tk.Tk()                       # crea la ventana principal de tkinter
    app = AplicacionGraficas(ventana_principal)       # crea la aplicación (ejecuta __init__)
    ventana_principal.mainloop()                      # mantiene el programa abierto esperando clics y teclas
