# =============================================================================
# GRÁFICAS Y ECUACIONES - CECYTEQ
# -----------------------------------------------------------------------------
# Aplicación de escritorio hecha con Tkinter (interfaz gráfica) + NumPy
# (cálculo matemático) + Matplotlib (gráficas incrustadas en la ventana).
#
# Qué hace el programa:
#   1) Menú principal con 3 botones.
#   2) "Primer grado": recibe 2 puntos y calcula/grafica la recta que pasa
#      por ellos (y = mx + b).
#   3) "Segundo grado": recibe 3 puntos y calcula/grafica la parábola que pasa
#      por ellos (y = ax² + bx + c).
#   4) "Sistemas de ecuaciones": 2x2 (dos rectas que se cruzan en un punto) y
#      3x3 (tres planos que se cruzan en un punto del espacio 3D).
#
# Estructura: una sola clase, MenuPrincipal, que contiene TODAS las ventanas
# y la lógica. Cada ventana tiene un método "construir" (dibuja los widgets) y
# un método "procesar" (lee datos, calcula y grafica al pulsar el botón).
# =============================================================================

# --- IMPORTACIONES -----------------------------------------------------------

# tkinter es la librería estándar de Python para crear ventanas, botones, etc.
# Se importa con el alias "tk" para escribir tk.Button, tk.Label, etc.
import tkinter as tk

# messagebox es un submódulo de tkinter para mostrar ventanitas emergentes
# (por ejemplo, mensajes de error). Hay que importarlo aparte.
from tkinter import messagebox

# os sirve para trabajar con rutas de archivos de forma compatible entre
# Windows, Linux y Mac (aquí se usa para encontrar la imagen del icono).
import os

# NumPy: cálculo numérico. Aquí se usa para: crear rangos de valores
# (linspace), resolver sistemas de ecuaciones (linalg.solve), calcular
# determinantes (linalg.det), comparar decimales (isclose) y crear mallas (meshgrid).
# ---- GUÍA RÁPIDA DE NUMPY (qué es y qué funciones se usan aquí) ----
# NumPy trabaja con "arreglos" (np.array): listas de números de un solo tipo
# guardadas de forma compacta. Su gran ventaja es la VECTORIZACIÓN: una
# operación como  m * x + b  se aplica a TODOS los elementos del arreglo a la
# vez (sin escribir un for), y es mucho más rápida que hacerlo con listas.
# Ejemplo:  x = np.array([0, 1, 2]);  2 * x - 4  ->  array([-4, -2, 0])
#
# Funciones de NumPy usadas en este programa:
#   np.linspace(a, b, n)   -> n números IGUALMENTE espaciados de a hasta b
#                             (incluye a y b). Sirve para "muestrear" una curva.
#   np.array([...])        -> crea un arreglo (1D = vector, 2D = matriz).
#   np.linalg.det(A)       -> determinante de una matriz cuadrada.
#   np.linalg.solve(A, B)  -> resuelve el sistema A·v = B (ver más abajo).
#   np.isclose(a, b)       -> compara decimales con tolerancia (ver más abajo).
#   np.sqrt(v)             -> raíz cuadrada.
#   np.meshgrid(x, y)      -> convierte dos vectores en dos mallas 2D (para 3D).
#   np.full_like(M, k)     -> arreglo del mismo tamaño que M relleno con k.
import numpy as np

# pyplot es la interfaz principal de Matplotlib para crear figuras y ejes.
# ---- GUÍA RÁPIDA DE MATPLOTLIB (cómo se construye una gráfica) ----
# Matplotlib dibuja con 3 piezas jerárquicas:
#   Figure (fig): el "lienzo" completo, como una hoja en blanco.
#   Axes   (ax) : una gráfica dentro de la hoja (con sus ejes, cuadrícula,
#                 título...). Una Figure puede tener varios Axes.
#   Artists     : todo lo que se dibuja sobre un Axes (líneas, puntos, texto...).
#
# Receta que se repite en TODAS las ventanas del programa:
#   1) fig, ax = plt.subplots(...)  -> crear lienzo + ejes.
#   2) ax.plot(...), ax.axvline(...) -> dibujar líneas y puntos.
#   3) ax.set_title / set_xlabel / grid / legend -> decorar.
#   4) FigureCanvasTkAgg(fig, master=panel) -> convertir la figura en un
#      widget de Tkinter y mostrarlo dentro de la ventana.
#   5) plt.close(fig) -> liberar la figura del administrador de pyplot.
import matplotlib.pyplot as plt

# FigureCanvasTkAgg es el "puente" entre Matplotlib y Tkinter: convierte una
# figura de Matplotlib en un widget que se puede colocar dentro de una ventana Tk.
# Un "backend" es el motor que convierte una figura en algo visible.
# "TkAgg" = Agg (renderiza la figura como una imagen de píxeles en memoria,
# usando la librería gráfica Anti-Grain Geometry) + Tk (la muestra en un
# widget de Tkinter). FigureCanvasTkAgg es la clase que hace ese puente.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


### Paleta de Colores ###
# Los colores se guardan en constantes (nombres en MAYÚSCULAS por convención)
# para que, si se quiere cambiar el estilo, se modifique en UN solo lugar.
# Los colores están en formato hexadecimal "#RRGGBB" (rojo, verde, azul).
COLOR_FONDO_PRINCIPAL = "#BCF6BC"  # Verde menta muy claro para el fondo
COLOR_TEXTO_TITULO    = "#1E4620"  # Verde bosque oscuro para los títulos
COLOR_BOTON_NORMAL    = "#2E7D32"  # Verde estándar para los botones
# Nota: en Tkinter, "activebackground" es el color mientras el botón está
# PRESIONADO (al hacer clic), no al pasar el mouse por encima (hover real).
COLOR_BOTON_HOVER     = "#1B5E20"  # Verde más oscuro cuando clckeas con el mouse
COLOR_TEXTO_BOTON     = "#FFFFFF"  # Texto blanco para que contraste con los botones

### Fuentes ###
# Una fuente en Tkinter es una tupla: (nombre, tamaño) o (nombre, tamaño, estilo).
# Si la fuente no existe en el sistema, Tkinter usa una de reemplazo.
fuente_titulo = ("Impact", 22)
fuente_botones = ("Helvetica", 11, "bold")  # "bold" = negritas


# =============================================================================
# CLASE PRINCIPAL
# =============================================================================
class MenuPrincipal:
    # __init__ es el constructor: se ejecuta automáticamente al crear
    # MenuPrincipal(raiz). Aquí se construye la ventana del menú principal.
    # "ventana" es la ventana raíz (tk.Tk) que se crea al final del archivo.
    def __init__(self, ventana):
        # Se guarda la ventana en self para usarla en los demás métodos
        # (por ejemplo, para crear ventanas hijas con Toplevel).
        self.ventana = ventana

        # Texto que aparece en la barra de título de la ventana.
        self.ventana.title("Gráficas y Ecuaciones - CECYTEQ")

        # Tamaño inicial en píxeles: "ancho x alto".
        self.ventana.geometry("480x450")

        # Color de fondo de la ventana.
        self.ventana.config(bg=COLOR_FONDO_PRINCIPAL)

        #### CONFIGURACIÓN DEL ICONO ####
        # __file__ es la ruta de este archivo .py; dirname extrae su carpeta.
        # Así el programa busca el icono junto al script, sin importar desde
        # dónde se ejecute.
        self.carpeta_proyecto = os.path.dirname(__file__)

        # os.path.join une carpeta + nombre de archivo con el separador correcto.
        self.ruta_icono = os.path.join(self.carpeta_proyecto, "logo_cecyteq.png")

        # try/except: si falta el archivo o está dañado, el programa NO se cae;
        # solo imprime el error en consola y continúa sin icono.
        try:
            # PhotoImage carga la imagen PNG en memoria para Tkinter.
            # Se guarda en self.icono (si fuera variable local, Python la
            # borraría y el icono desaparecería: Tkinter no conserva referencia).
            self.icono = tk.PhotoImage(file=self.ruta_icono)

            # iconphoto pone la imagen como icono de la ventana. El primer
            # argumento False significa "solo esta ventana" (True = también
            # las ventanas hijas futuras).
            self.ventana.iconphoto(False, self.icono)
        except Exception as e:
            # Si algo falla, se informa en la terminal.
            print(f"Error al cargar el icono: {e}")

        # Configuración de cuadrícula (Grid)
        # Grid divide la ventana en filas y columnas. "weight=1" indica que la
        # fila/columna se estira para repartirse el espacio sobrante
        # (3 filas con el mismo peso = reparto en tercios).
        self.ventana.rowconfigure(0, weight=1)
        self.ventana.rowconfigure(1, weight=1)
        self.ventana.rowconfigure(2, weight=1)

        # 2 columnas con el mismo peso: izquierda (título), derecha (botones).
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)

        
        # Título lateral. Se crea el Label y se coloca con .grid() en la misma línea.
        tk.Label(self.ventana,
                # "\n" son saltos de línea: el título queda en 3 renglones.
                text="Gráficas \ny \nEcuaciones", 
                font=fuente_titulo,
                # fg = foreground = color del texto.
                fg=COLOR_TEXTO_TITULO,
                # bg = background = color de fondo (igual al de la ventana).
                bg=COLOR_FONDO_PRINCIPAL,
                # relief="flat" = sin borde 3D.
                relief="flat",
                # padx = margen interno horizontal.
                padx=20).grid(row=0, column=0, rowspan=3, sticky="nsew") 
        # Explicación de grid: fila 0, columna 0; rowspan=3 = ocupa las 3 filas
        # a lo alto; sticky="nsew" = se pega a norte, sur, este y oeste
        # (rellena toda su celda).

        # --- Botón 1: gráfica de primer grado ---
        btn_primer = tk.Button(self.ventana,
                text="Gráfica una ecuación \nde primer grado",
                font=fuente_botones,
                bg=COLOR_BOTON_NORMAL,            # color normal
                fg=COLOR_TEXTO_BOTON,             # color del texto
                activebackground=COLOR_BOTON_HOVER,   # color al presionar
                activeforeground=COLOR_TEXTO_BOTON,   # texto al presionar
                cursor="hand2",                   # el mouse cambia a "manita"
                bd=0,                             # borde de 0 px (estilo plano)
                pady=10)                          # margen interno vertical
        # Se coloca en la fila 0, columna 1 (derecha). padx/pady = margen
        # externo; sticky="ew" = se estira de este a oeste (todo el ancho).
        btn_primer.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        # command = función que se ejecuta al hacer clic. Se pasa SIN paréntesis
        # (si llevara paréntesis se ejecutaría de inmediato al crear el botón).
        btn_primer.config(command=self.grafica_primer_grado)

        # --- Botón 2: gráfica de segundo grado (misma estructura) ---
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

        # --- Botón 3: sistemas de ecuaciones (misma estructura) ---
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
    # Métodos auxiliares reutilizados por varias ventanas.

    # @staticmethod: el método no necesita "self" (no usa datos del objeto),
    # solo recibe un número y devuelve texto. Se llama como self._num(valor).
    # El guion bajo inicial "_" indica "uso interno" por convención.
    @staticmethod
    def _num(n):
        """Formatea un número sin ceros sobrantes (2.00 -> 2, -0.00 -> 0)."""
        # f"{n:.2f}" convierte a texto con 2 decimales (2 -> "2.00").
        # rstrip("0") quita ceros finales ("2.00" -> "2."), luego rstrip(".")
        # quita el punto sobrante ("2." -> "2"). "2.50" -> "2.5".
        s = f"{n:.2f}".rstrip("0").rstrip(".")
        # Casos raros: "-0.00" queda como "-0" y un resultado vacío se
        # convierte en "0" para no mostrar "-0" al usuario.
        return "0" if s in ("-0", "") else s

    def _texto_poli(self, terminos):
        """Arma 'y = ...' a partir de [(coeficiente, 'x²'), (coeficiente, 'x'), (coeficiente, '')]."""
        # Construye la ecuación como texto, p. ej. "y = x² - 2x - 3".
        # "terminos" es una lista de tuplas (coeficiente, parte_variable).
        texto = ""
        for coef, var in terminos:
            # np.isclose compara con tolerancia (evita errores de decimales
            # tipo 0.0000000001). Si el coeficiente es ~0, ese término no se escribe.
            # POR QUÉ np.isclose y no "coef == 0": los números decimales (float) se guardan
            # en binario y arrastran pequeños errores (por ejemplo 0.1 + 0.2 = 0.30000000000000004).
            # Después de resolver sistemas con NumPy un coeficiente que "debería ser 0"
            # puede salir como 1e-16. np.isclose(a, b) devuelve True si
            #     |a - b| <= atol + rtol * |b|      (por defecto atol=1e-8 y rtol=1e-5)
            # es decir, si son "prácticamente iguales". Así 1e-16 se trata como 0.
            if np.isclose(coef, 0):
                continue
            # Se trabaja con el valor absoluto; el signo se agrega después.
            magnitud = abs(coef)
            # Si el coeficiente es 1 y hay variable, se escribe "x" y no "1x".
            if var != "" and np.isclose(magnitud, 1):
                cuerpo = var
            else:
                # Si no, número formateado + variable (ej. "2x", "3x²" o "4").
                cuerpo = self._num(magnitud) + var
            # Primer término: solo lleva "-" si es negativo (no lleva "+").
            if texto == "":
                texto = ("-" if coef < 0 else "") + cuerpo
            else:
                # Siguientes términos: " + 3x" o " - 3x" con espacios.
                texto += f" {'-' if coef < 0 else '+'} {cuerpo}"
        # Si todos los coeficientes eran 0, devuelve "y = 0".
        return "y = " + (texto if texto else "0")

    def _fila_punto(self, padre, etiqueta, x_defecto, y_defecto):
        """Crea una fila '(  x  ,  y  )' y devuelve sus dos Entry."""
        # Crea una línea de interfaz como:  A ( [  x  ] , [  y  ] )
        # "padre" = contenedor donde se coloca; "etiqueta" = letra (A, B, C);
        # x_defecto / y_defecto = valores iniciales de las cajas de texto.

        # Frame = contenedor invisible que agrupa widgets (aquí, una fila).
        fila = tk.Frame(padre, bg=COLOR_FONDO_PRINCIPAL)
        # pack: coloca el widget uno tras otro. anchor="w" = alineado a la
        # izquierda (west); pady=4 = separación vertical.
        fila.pack(anchor="w", pady=4)

        # Etiqueta con la letra del punto (A, B o C), ancho fijo de 3 caracteres.
        tk.Label(fila, text=etiqueta, font=("Helvetica", 10, "bold"),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL,
                width=3, anchor="w").pack(side="left")
        # side="left" coloca cada widget a la derecha del anterior (en horizontal).
        # Paréntesis de apertura "(" decorativo.
        tk.Label(fila, text="(", font=("Helvetica", 12),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(side="left")

        # Entry = caja de texto de una línea (aquí para la coordenada x).
        # width=5 caracteres de ancho; justify="center" centra el texto.
        entry_x = tk.Entry(fila, font=("Helvetica", 11), width=5, justify="center")
        entry_x.pack(side="left")
        # insert(0, texto) escribe el valor por defecto desde la posición 0.
        entry_x.insert(0, x_defecto)

        # Coma separadora entre x e y.
        tk.Label(fila, text=",", font=("Helvetica", 12),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(side="left")

        # Caja de texto para la coordenada y (misma configuración).
        entry_y = tk.Entry(fila, font=("Helvetica", 11), width=5, justify="center")
        entry_y.pack(side="left")
        entry_y.insert(0, y_defecto)

        # Paréntesis de cierre ")".
        tk.Label(fila, text=")", font=("Helvetica", 12),
                fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(side="left")
        # Se devuelven las dos cajas para poder leer sus valores después.
        return entry_x, entry_y

    def _leer_puntos(self, pares_entries):
        """Lee una lista de (entry_x, entry_y) y devuelve [(x, y), ...] o None si hay error."""
        try:
            # Lista por comprensión: para cada par (ex, ey) se lee el texto con
            # .get(), se cambia la coma por punto (acepta "2,5" como decimal)
            # y se convierte a float. Devuelve [(x1, y1), (x2, y2), ...].
            return [(float(ex.get().replace(",", ".")), float(ey.get().replace(",", ".")))
                    for ex, ey in pares_entries]
        except ValueError:
            # float() lanza ValueError si el texto no es un número (vacío, letras...).
            # Se muestra una ventana de error y se devuelve None como señal de fallo.
            messagebox.showerror("Error de datos",
                                "Por favor, introduce números válidos en todas las coordenadas.")
            return None

    def _marcar_puntos(self, ax, puntos, nombres):
        """Dibuja los pares ordenados ingresados con su etiqueta de coordenadas."""
        # "ax" = los ejes de Matplotlib donde se dibuja.
        # zip junta cada punto con su nombre; enumerate agrega el índice i.
        for i, ((px, py), nombre) in enumerate(zip(puntos, nombres)):
            # Dibuja un círculo azul ('o') de tamaño 8. zorder=5 = se dibuja
            # por encima de las líneas. Solo el primer punto lleva etiqueta de
            # leyenda ("Puntos ingresados") para que no se repita en la leyenda.
            # ax.plot(x, y, formato, ...) dibuja datos en el plano. Si x e y son UN solo
            # número, dibuja un único punto. El texto 'o' es un "código de marcador":
            # 'o' = círculo, 'D' = rombo, 'go' = verde + círculo, 'ro' = rojo + círculo.
            # Parámetros usados: markersize = tamaño del marcador en puntos tipográficos;
            # zorder = orden de capas (mayor = más arriba); label = nombre que se mostrará
            # en la leyenda (si es None, ese elemento NO aparece en la leyenda).
            # Ojo con las coordenadas: ax.plot trabaja en "coordenadas de datos", o sea,
            # las mismas unidades de los ejes (el punto (3, 2) se ubica en x=3, y=2).
            ax.plot(px, py, 'o', color="#1565C0", markersize=8, zorder=5,
                    label="Puntos ingresados" if i == 0 else None)
            # annotate escribe el texto "A(1, 2)" junto al punto.
            # xytext=(7, 7) lo desplaza 7 puntos arriba-derecha del punto;
            # "offset points" indica que el desplazamiento es en puntos de pantalla.
            ax.annotate(f"{nombre}({self._num(px)}, {self._num(py)})", (px, py),
                        textcoords="offset points", xytext=(7, 7), fontsize=8, color="#1565C0")


    #### VENTANAS HIJAS ####
    # ------------------------------------------------------------------
    # VENTANA: ECUACIÓN DE PRIMER GRADO (recta por 2 puntos)
    # Este método SOLO construye la interfaz. El cálculo se hace en
    # procesar_primer_grado, que se ejecuta al presionar "Graficar".
    # ------------------------------------------------------------------
    def grafica_primer_grado(self):
        # Toplevel = ventana secundaria que depende de la ventana principal.
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Primer Grado: recta por 2 puntos")
        ventana_hija.geometry("750x520")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        # Solo se asigna el icono si se cargó correctamente en __init__
        # (hasattr verifica que exista el atributo self.icono).
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)

        # Panel izquierdo: contiene título, entradas, botón y resultados.
        frame_izquierdo = tk.Frame(ventana_hija,
                                bg=COLOR_FONDO_PRINCIPAL,
                                padx=15,
                                pady=15)
        # side="left" lo pega a la izquierda; fill="y" lo estira a lo alto.
        frame_izquierdo.pack(side="left", fill="y")

        # Título del panel.
        tk.Label(frame_izquierdo,
                text="Ecuación Lineal",
                font=("Impact", 16),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        # Instrucción para el usuario (en cursiva).
        tk.Label(frame_izquierdo,
                text="Ingresa 2 pares ordenados (x, y)",
                font=("Helvetica", 11, "italic"),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        # Contenedor de las filas de puntos. pady=(15, 0): 15 px arriba, 0 abajo.
        frame_puntos = tk.Frame(frame_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        frame_puntos.pack(anchor="w", pady=(15, 0))

        # Valores por defecto: (0, -4) y (3, 2)  ->  y = 2x - 4
        # Se crean 2 filas de entradas. Se guardan en self.* porque el método
        # procesar_primer_grado necesita leerlas más tarde.
        self.p1_x, self.p1_y = self._fila_punto(frame_puntos, "A", "0", "-4")
        self.p2_x, self.p2_y = self._fila_punto(frame_puntos, "B", "3", "2")

        # Botón "Graficar": al presionarlo ejecuta procesar_primer_grado.
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
        # fill="x" = el botón ocupa todo el ancho del panel.
        btn_calcular.pack(pady=20, fill="x")

        # Etiqueta donde se mostrarán pendiente, intersecciones, etc.
        # Se guarda en self para poder cambiar su texto con .config(text=...).
        # justify="left" alinea las líneas a la izquierda.
        self.lbl_valores_clave_1ro = tk.Label(frame_izquierdo,
                                            text="Valores clave:\n-\n-",
                                            font=("Helvetica", 10),
                                            justify="left",
                                            fg=COLOR_TEXTO_TITULO,
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_1ro.pack(anchor="w", pady=10)

        # Panel derecho (fondo blanco, borde hundido): aquí se incrusta la gráfica.
        self.frame_grafica_1ro = tk.Frame(ventana_hija,
                                        bg="white",
                                        bd=1,
                                        relief="sunken")
        # expand=True + fill="both": ocupa todo el espacio restante.
        self.frame_grafica_1ro.pack(side="right", expand=True, fill="both", padx=15, pady=15)


    # Calcula la recta por 2 puntos y la grafica.
    def procesar_primer_grado(self):
        # 1) Leer los datos. Si hay error (texto no numérico), _leer_puntos
        # muestra el mensaje y devuelve None → se cancela con "return".
        puntos = self._leer_puntos([(self.p1_x, self.p1_y), (self.p2_x, self.p2_y)])
        if puntos is None:
            return
        # Desempaquetado de la lista en 4 variables.
        (x1, y1), (x2, y2) = puntos

        # 2) Validación: dos puntos idénticos no definen una recta única.
        if x1 == x2 and y1 == y2:
            messagebox.showerror("Error matemático",
                                "Los dos puntos son iguales. Una recta necesita dos puntos distintos.")
            return

        # "n" es un alias corto de la función de formato para escribir menos.
        n = self._num
        # Si x1 == x2 la recta es vertical (x = constante).
        vertical = (x1 == x2)

        if vertical:
            # Recta vertical: x = k (no es función, no tiene m ni b)
            # Se ponen m y b en None (no existen) y la "raíz" es x1.
            m = b = None
            raiz = x1
            # Texto de resultados. La expresión (... if x1 == 0 else ...) elige
            # el mensaje: si x = 0 la recta ES el eje Y.
            texto_valores = (
                f"--- VALORES CLAVE ---\n"
                f"Recta vertical: x = {n(x1)}\n"
                f"Pendiente (m): indefinida\n"
                f"Intersección Y: " + ("(0, y) para todo y (es el eje Y)" if x1 == 0 else "No tiene") + "\n"
                f"Intersección X: ({n(x1)}, 0)"
            )
        else:
            # Pendiente: m = (y2 - y1) / (x2 - x1).
            # ===== MATEMÁTICA: RECTA QUE PASA POR DOS PUNTOS =====
            # Forma pendiente-ordenada:  y = m·x + b
            #   m = pendiente = cuánto sube y por cada unidad que avanza x:
            #           m = (y2 - y1) / (x2 - x1)      ("cambio en y" entre "cambio en x")
            #   b = ordenada al origen = valor de y cuando x = 0. Como el punto (x1, y1)
            #       debe cumplir la ecuación:  y1 = m·x1 + b   ->   b = y1 - m·x1
            # Ejemplo con los valores por defecto A(0, -4) y B(3, 2):
            #   m = (2 - (-4)) / (3 - 0) = 6/3 = 2   y   b = -4 - 2·0 = -4   ->  y = 2x - 4
            # (Si x1 == x2 el denominador sería 0: por eso la recta vertical se trató antes.)
            m = (y2 - y1) / (x2 - x1)
            # Ordenada al origen: de y = mx + b se despeja b = y1 - m·x1.
            b = y1 - m * x1
            # Si m no es 0, la recta cruza el eje X en x = -b/m (la raíz).
            if not np.isclose(m, 0):
                # La RAÍZ es donde la recta cruza el eje X, o sea donde y = 0:
                #     0 = m·x + b   ->   m·x = -b   ->   x = -b / m
                # Solo existe si m ≠ 0 (si m = 0 la recta es horizontal y nunca cruza, o bien
                # coincide con el eje X). Con y = 2x - 4:  x = -(-4)/2 = 2  ->  punto (2, 0).
                raiz = -b / m
                texto_raiz = f"Raíz (Intersección X): ({n(raiz)}, 0)"
            else:
                # Recta horizontal (m = 0): no hay raíz única.
                raiz = None
                # Si además b = 0, es el propio eje X; si no, es paralela a él.
                texto_raiz = ("Raíz (Intersección X): todo el eje X (la recta es el eje X)"
                            if np.isclose(b, 0) else
                            "Raíz (Intersección X): No tiene (paralela al eje X)")
            # Texto final con ecuación, pendiente, b, intersección Y y raíz.
            texto_valores = (
                f"--- VALORES CLAVE ---\n"
                f"{self._texto_poli([(m, 'x'), (b, '')])}\n"
                f"Pendiente (m): {n(m)}\n"
                f"Ordenada al origen (b): {n(b)}\n"
                f"Intersección Y: (0, {n(b)})\n"
                f"{texto_raiz}"
            )
        # Se muestra el texto en la etiqueta del panel izquierdo.
        self.lbl_valores_clave_1ro.config(text=texto_valores)

        # Se borra la gráfica anterior (si la hay) destruyendo los widgets
        # hijos del panel; así no se apilan gráficas al presionar varias veces.
        for widget in self.frame_grafica_1ro.winfo_children():
            widget.destroy()

        # Rango de la gráfica: que se vean los puntos, el origen y las intersecciones
        # Listas de coordenadas que deben quedar visibles en la ventana.
        # ===== CÓMO SE ELIGE LA "VENTANA" DE LA GRÁFICA =====
        # Una recta es infinita, así que hay que decidir qué tramo mostrar. Se reúnen
        # las coordenadas que SÍ deben verse (puntos, origen, raíz, intersección con Y)
        # y se toma el mínimo y el máximo de cada eje. Luego se agrega un margen
        # ("padding") de 30% del rango (con mínimo de 2 unidades) para que nada quede
        # pegado al borde. Resultado: xmin - pad ... xmax + pad.
        refs_x = [x1, x2, 0]
        refs_y = [y1, y2, 0]
        if raiz is not None:
            refs_x.append(raiz)
        if not vertical:
            refs_y.append(b)
        # Margen alrededor: el 30% del rango, pero mínimo 2 unidades.
        pad_x = max(2, 0.3 * (max(refs_x) - min(refs_x)))
        pad_y = max(2, 0.3 * (max(refs_y) - min(refs_y)))
        # Límites del eje X: mínimo y máximo con el margen.
        x_min, x_max = min(refs_x) - pad_x, max(refs_x) + pad_x

        # Crea la figura (5x4 pulgadas, 100 puntos por pulgada) y sus ejes.
        # plt.subplots() crea a la vez una Figure y un Axes y los devuelve como tupla
        # (por eso se desempaqueta en "fig, ax").
        #   figsize=(5, 4) -> tamaño en PULGADAS: 5 de ancho por 4 de alto.
        #   dpi=100        -> "puntos por pulgada" (resolución).
        # Tamaño final en píxeles = pulgadas × dpi = 500 × 400 px, que es
        # aproximadamente lo que cabe en el panel derecho de la ventana.
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        if vertical:
            # axvline dibuja una línea vertical en x = x1.
            # ax.axvline(x) dibuja una línea VERTICAL infinita en la posición x del eje X
            # (hermana de ax.axhline(y), que dibuja una HORIZONTAL). Se usa aquí porque una
            # recta vertical no se puede escribir como y = f(x), así que no se puede
            # calcular con una lista de valores: se dibuja directamente.
            ax.axvline(x1, color="#2E7D32", linewidth=2, label=f"x = {n(x1)}")
            # Para vertical hay que fijar el rango Y manualmente.
            ax.set_ylim(min(refs_y) - pad_y, max(refs_y) + pad_y)
        else:
            # linspace crea 200 valores de x igualmente espaciados; con ellos
            # se calcula y = m·x + b para toda la recta (NumPy opera en bloque).
            # ===== CÓMO SE DIBUJA UNA CURVA EN COMPUTADORA =====
            # Matplotlib no sabe dibujar "la función y = m·x + b" en forma continua; solo
            # une puntos con segmentos pequeños. Por eso:
            #   1) np.linspace crea 200 valores de x entre x_min y x_max, equidistantes.
            #   2) La expresión  m * x + b  se evalúa en los 200 valores a la vez
            #      (vectorización) y produce 200 valores de y.
            #   3) ax.plot(x, y) une los 200 puntos (x_i, y_i) con segmentos.
            # Para una recta bastarían 2 puntos; con 200 se usa el mismo código que la
            # parábola, donde sí se necesitan muchos puntos para que se vea suave.
            x = np.linspace(x_min, x_max, 200)
            ax.plot(x, m * x + b, color="#2E7D32", linewidth=2,
                    label=self._texto_poli([(m, 'x'), (b, '')]))
            # Marca la intersección con el eje Y. Se sabe que está en (0, b) porque al
            # evaluar y = m·0 + b se obtiene b. 'go' = punto verde (g=green, o=círculo).
            ax.plot(0, b, 'go', label=f"Int. Y (0, {n(b)})")                  # Punto intersección Y
            if raiz is not None:
                ax.plot(raiz, 0, 'ro', label=f"Raíz ({n(raiz)}, 0)")          # Punto de la raíz
        # Se fijan los límites del eje X.
        # set_xlim fija el rango visible del eje X. Si no se llamara, Matplotlib
        # calcularía los límites solo a partir de los datos dibujados ("autoscale").
        # (En la recta vertical el eje Y se fijó antes con set_ylim por la misma razón.)
        ax.set_xlim(x_min, x_max)

        # Dibuja los puntos A y B con sus coordenadas.
        self._marcar_puntos(ax, [(x1, y1), (x2, y2)], ["A", "B"])

        # Dibujar axhline(0) y axvline(0) en negro marca los EJES cartesianos
        # (la recta y = 0 es el eje X y la recta x = 0 es el eje Y). Matplotlib por sí
        # solo solo dibuja el marco de la gráfica, no los ejes que cruzan por el origen.
        ax.axhline(0, color='black', linewidth=1) # Eje X
        ax.axvline(0, color='black', linewidth=1) # Eje Y
        # grid(True) activa la cuadrícula en las marcas de los ejes; linestyle='--' la
        # hace de líneas discontinuas; alpha=0.6 es la opacidad (0 = invisible,
        # 1 = sólida) para que no tape la gráfica.
        ax.grid(True, linestyle='--', alpha=0.6)   # Cuadrícula de fondo
        ax.set_title("Gráfica de la Ecuación Lineal", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        # Leyenda con las "label" de cada elemento dibujado.
        # legend() arma el recuadro de leyenda automáticamente: recorre todo lo
        # dibujado que tenga "label" y muestra su símbolo junto con ese texto.
        ax.legend(fontsize=8)

        # Incrusta la figura en el panel de Tkinter:
        # 1) Se crea el canvas que envuelve la figura.
        # ===== DE MATPLOTLIB A TKINTER =====
        # Hasta aquí "fig" es solo una descripción de la gráfica en memoria. Los pasos:
        #   FigureCanvasTkAgg(fig, master=panel) -> crea el "lienzo" que sabe pintar
        #       la figura y que pertenece al panel (master) de Tkinter.
        #   canvas.draw()                        -> renderiza la figura a píxeles.
        #   canvas.get_tk_widget()               -> obtiene el widget real de Tkinter...
        #   .pack(expand=True, fill="both")      -> ...y lo coloca llenando todo el panel.
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_1ro)
        # 2) draw() renderiza la figura.
        canvas.draw()
        # 3) get_tk_widget() obtiene el widget de Tk y se empaqueta para llenar el panel.
        canvas.get_tk_widget().pack(expand=True, fill="both")

        # Cierra la figura en pyplot para liberar memoria (el canvas sigue
        # mostrándola; solo se evita acumular figuras abiertas).
        # pyplot guarda en una lista global TODAS las figuras que se crean con
        # plt.subplots()/plt.figure(). Si no se cierran, se acumulan en memoria cada
        # vez que se presiona "Graficar" (y Matplotlib avisa después de 20 figuras).
        # plt.close(fig) la saca de esa lista; el canvas ya incrustado sigue mostrándola.
        plt.close(fig)



    # ------------------------------------------------------------------
    # VENTANA: ECUACIÓN DE SEGUNDO GRADO (parábola por 3 puntos)
    # Misma estructura que la de primer grado, pero con 3 puntos.
    # ------------------------------------------------------------------
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
        # Tres filas de entradas (prefijo q_ = "quadratic" para distinguirlas
        # de las de primer grado).
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

        # Etiqueta de resultados de la parábola.
        self.lbl_valores_clave_2do = tk.Label(frame_izquierdo,
                                            text="Valores clave:\n-\n-",
                                            font=("Helvetica", 10),
                                            justify="left",
                                            fg=COLOR_TEXTO_TITULO,
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_2do.pack(anchor="w", pady=10)

        # Panel donde se incrusta la gráfica.
        self.frame_grafica_2do = tk.Frame(ventana_hija,
                                        bg="white",
                                        bd=1,
                                        relief="sunken")
        self.frame_grafica_2do.pack(side="right",
                                    expand=True,
                                    fill="both",
                                    padx=15, pady=15)


    # Calcula la parábola que pasa por 3 puntos y la grafica.
    def procesar_segundo_grado(self):
        # Lectura y validación numérica de los 3 puntos.
        puntos = self._leer_puntos([(self.q_p1_x, self.q_p1_y),
                                    (self.q_p2_x, self.q_p2_y),
                                    (self.q_p3_x, self.q_p3_y)])
        if puntos is None:
            return

        # Se separan las coordenadas en dos listas: xs e ys.
        xs = [p[0] for p in puntos]
        ys = [p[1] for p in puntos]

        # set() elimina repetidos: si hay menos de 3 valores distintos de X,
        # dos puntos comparten X y no se puede formar una función cuadrática.
        if len(set(xs)) < 3:
            messagebox.showerror("Error matemático",
                                "Los 3 puntos deben tener valores de X distintos.\n"
                                "(Si dos puntos comparten X, no se puede formar y = ax² + bx + c)")
            return

        # Cada punto cumple y = a·x² + b·x + c  ->  sistema 3x3 para encontrar a, b, c
        # Matriz A: cada fila es [x², x, 1] de un punto. Resolver A·[a,b,c] = ys
        # da los coeficientes de la parábola (interpolación).
        # ===== MATEMÁTICA: PARÁBOLA QUE PASA POR 3 PUNTOS =====
        # Se busca y = a·x² + b·x + c. Las incógnitas son a, b y c (3 números), y cada
        # punto (xi, yi) aporta UNA ecuación al sustituir en la fórmula:
        #     a·x1² + b·x1 + c = y1
        #     a·x2² + b·x2 + c = y2
        #     a·x3² + b·x3 + c = y3
        # Son 3 ecuaciones LINEALES en a, b, c (los x² son números conocidos). En forma
        # de matriz:   [ x1²  x1  1 ]   [a]   [y1]
        #              [ x2²  x2  1 ] · [b] = [y2]        es decir   A · v = y
        #              [ x3²  x3  1 ]   [c]   [y3]
        # Cada fila de A se arma con la comprensión [x**2, x, 1.0] para cada x de xs.
        # Se usa 1.0 (float) para que toda la matriz sea de decimales.
        # Esta matriz se llama "de Vandermonde": su determinante es distinto de 0
        # solo si los tres x son DIFERENTES (por eso se exige antes x distintos).
        A = np.array([[x**2, x, 1.0] for x in xs])
        # np.linalg.solve(A, y) resuelve A·v = y. Internamente usa eliminación
        # gaussiana (descomposición LU): convierte la matriz en una triangular y
        # despeja de abajo hacia arriba. Es más preciso y rápido que calcular la
        # inversa de A. Devuelve un arreglo [a, b, c] que aquí se desempaqueta.
        # Ejemplo con (-1,0), (0,-3), (3,0):  a=1, b=-2, c=-3  ->  y = x² - 2x - 3.
        a, b, c = np.linalg.solve(A, np.array(ys))

        # Si a ≈ 0 los 3 puntos son colineales: es una recta, no una parábola.
        # Si los tres puntos están sobre una misma recta, la solución del sistema da
        # a = 0 (el término x² desaparece) y la "parábola" es en realidad una recta.
        # atol=1e-9 es la tolerancia absoluta: valores menores a 0.000000001 cuentan
        # como cero (los errores de redondeo pueden dejar a = 1e-16 en vez de 0).
        # Además, a = 0 rompería las fórmulas de abajo (dividen entre 2a).
        if np.isclose(a, 0, atol=1e-9):
            messagebox.showerror("Error matemático",
                                "Los 3 puntos están alineados: forman una recta, no una parábola.\n"
                                "Usa la opción de ecuación de primer grado, o cambia algún punto.")
            return

        n = self._num
        # Discriminante Δ = b² - 4ac: indica cuántas raíces reales hay.
        # ===== MATEMÁTICA: DISCRIMINANTE Y RAÍCES =====
        # Las raíces son los x donde y = 0:  a·x² + b·x + c = 0. Completando el
        # cuadrado se llega a la fórmula general:
        #           x = ( -b ± √(b² - 4ac) ) / (2a)
        # La parte bajo la raíz es el DISCRIMINANTE  Δ = b² - 4ac  y decide cuántas
        # raíces REALES (cruces con el eje X) hay:
        #     Δ > 0 -> dos raíces reales distintas (la parábola cruza el eje X 2 veces)
        #     Δ = 0 -> una raíz real doble (la parábola solo TOCA el eje X en el vértice)
        #     Δ < 0 -> ninguna real (la parábola no toca el eje X); son complejas.
        discriminante = b**2 - 4*a*c

        # Vértice: x = -b/(2a); su y se obtiene evaluando la parábola en ese x.
        # ===== MATEMÁTICA: VÉRTICE =====
        # El vértice es el punto más alto (si a < 0) o más bajo (si a > 0). Como la
        # parábola es simétrica, su eje pasa justo a la mitad entre las dos raíces:
        #     (x1 + x2)/2 = ( (-b+√Δ) + (-b-√Δ) ) / (4a) = -b / (2a)
        # (también sale al derivar y' = 2a·x + b = 0). Esa es la coordenada H del
        # vértice; la K se obtiene evaluando la parábola en ese x (sustituyendo).
        vx = -b / (2 * a)
        vy = a * (vx**2) + b * vx + c

        # Según el signo del discriminante hay tres casos:
        # Se usa isclose y no "== 0" porque Δ sale de operaciones con decimales y casi
        # nunca da exactamente 0 aunque matemáticamente lo sea.
        if np.isclose(discriminante, 0):
            # Δ = 0: una sola raíz (repetida), que coincide con el vértice.
            x1 = -b / (2 * a)
            texto_raices = f"Raíz (Real única / repetida):\n  X = {n(x1)}"
            puntos_raices = [(x1, 0)]
        elif discriminante > 0:
            # Δ > 0: dos raíces reales distintas (fórmula general).
            x1 = (-b + np.sqrt(discriminante)) / (2 * a)
            x2 = (-b - np.sqrt(discriminante)) / (2 * a)
            texto_raices = f"Raíces (Reales distintas):\n  X1 = {n(x1)}\n  X2 = {n(x2)}"
            puntos_raices = [(x1, 0), (x2, 0)]
        else:
            # Δ < 0: raíces complejas conjugadas (parte real ± parte imaginaria).
            # Con Δ < 0 aparece la raíz de un número negativo: √Δ = i·√|Δ|, donde i es la
            # unidad imaginaria (i² = -1). La fórmula general queda:
            #     x = -b/(2a)  ±  i · √|Δ| / (2a)
            # -> parte real = -b/(2a)  (justo la coordenada H del vértice);
            # -> parte imaginaria = √|Δ| / (2|a|). Se usa |a| porque el signo "±" ya
            #    contempla ambos signos, y así el valor mostrado es siempre positivo.
            # Son un par de números complejos conjugados y no se pueden ubicar en el eje
            # X real, por eso en este caso no se dibujan puntos de raíces.
            parte_real = -b / (2 * a)
            parte_imag = np.sqrt(abs(discriminante)) / (2 * abs(a))
            texto_raices = (f"Raíces (Complejas/Imaginarias):\n"
                            f"  X1 = {n(parte_real)} + {n(parte_imag)}i\n"
                            f"  X2 = {n(parte_real)} - {n(parte_imag)}i")
            puntos_raices = [] # No se cruza el eje X real

        # Ecuación en texto, p. ej. "y = x² - 2x - 3".
        ecuacion = self._texto_poli([(a, 'x²'), (b, 'x'), (c, '')])

        # Texto del panel izquierdo con todos los valores clave.
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
        # Limpia la gráfica anterior.
        for widget in self.frame_grafica_2do.winfo_children():
            widget.destroy()

        # Rango de la gráfica: que se vean los puntos, el vértice, el origen y las raíces
        # Se juntan todas las coordenadas X importantes para definir el ancho.
        # Ventana horizontal: debe mostrar los 3 puntos, el vértice, el eje Y (x=0) y
        # las raíces. (Mismo método de margen que en la recta; el eje Y aquí lo calcula
        # Matplotlib solo, según los valores de la curva que se dibuje.)
        refs_x = xs + [vx, 0] + [p[0] for p in puntos_raices]
        pad_x = max(2, 0.3 * (max(refs_x) - min(refs_x)))
        # 300 valores de x para una curva suave; y se calcula con la fórmula
        # (NumPy aplica la operación a todo el arreglo a la vez).
        # Se crean 300 valores de x. La línea siguiente aplica la fórmula a todo el
        # arreglo: x**2 eleva al cuadrado CADA elemento (operación elemento a
        # elemento, no multiplicación de matrices), b * x multiplica cada elemento por
        # b, y c se suma a todos. Resultado: 300 valores de y.
        # Más puntos = curva más suave (con pocos se vería "quebrada" en la punta).
        x = np.linspace(min(refs_x) - pad_x, max(refs_x) + pad_x, 300)
        y = a * (x**2) + b * x + c

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        # Dibuja la parábola.
        # Une los 300 puntos (x_i, y_i) con segmentos muy cortos: a esa escala el ojo
        # ve una curva continua. linewidth = grosor de la línea en puntos.
        ax.plot(x, y, color="#2E7D32", linewidth=2, label=ecuacion)

        # Ejes, cuadrícula, título y etiquetas.
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_title("Gráfica de la Ecuación Cuadrática", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")

        # Puntos ingresados A, B y C.
        self._marcar_puntos(ax, puntos, ["A", "B", "C"])

        # Vértice: rombo morado ('D' = diamante).
        # Marca el vértice. 'D' es el marcador "diamante/rombo"; color="#8E24AA" lo
        # pinta de morado (se puede combinar la forma con un color hexadecimal).
        ax.plot(vx, vy, 'D', color="#8E24AA", label=f"Vértice ({n(vx)}, {n(vy)})")
        # Intersección con el eje Y: punto verde en (0, c).
        # Intersección con el eje Y: ocurre en x = 0, y al sustituir en y = ax² + bx + c
        # todos los términos con x desaparecen y queda y = c. Por eso el punto es (0, c).
        ax.plot(0, c, 'go', label=f"Int. Y (0, {n(c)})")

        # Raíces: puntos rojos sobre el eje X (solo la primera lleva etiqueta).
        # Dibuja cada raíz como punto rojo sobre el eje X (su y es 0). enumerate da el
        # índice i para ponerle etiqueta de leyenda solo a la primera raíz y no repetirla.
        # Si la lista está vacía (Δ < 0) este ciclo simplemente no hace nada.
        for i, (px, py) in enumerate(puntos_raices):
            ax.plot(px, py, 'ro', label="Raíces (Int. X)" if i == 0 else None)

        ax.legend(fontsize=8)

        # Incrustar la gráfica en Tkinter (igual que en primer grado).
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_2do)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        plt.close(fig)



    # ------------------------------------------------------------------
    # VENTANA: SELECTOR DE TIPO DE SISTEMA (2x2 o 3x3)
    # ------------------------------------------------------------------
    def ventana_sistema_ecuaciones(self):
        ventana_sistemas = tk.Toplevel(self.ventana)
        ventana_sistemas.title("Sistemas de Ecuaciones")
        ventana_sistemas.geometry("400x300")
        ventana_sistemas.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_sistemas.iconphoto(False, self.icono)

        # Título de la ventana.
        tk.Label(ventana_sistemas, 
                text="Selecciona el Tipo de Sistema", 
                font=("Impact", 18),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=25)

        # Botón que abre la ventana del sistema 2x2. Aquí el botón se crea y se
        # coloca (pack) en la misma instrucción; "command" va dentro del Button.
        # padx=50 deja margen a los lados y fill="x" lo estira entre esos márgenes.
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

        # Botón que abre la ventana del sistema 3x3.
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

    # ------------------------------------------------------------------
    # VENTANA: SISTEMA 2x2  (a1·x + b1·y = c1  y  a2·x + b2·y = c2)
    # ------------------------------------------------------------------
    def sistema_2x2(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 2x2")
        ventana_hija.geometry("800x550")  # Espacio suficiente para entradas y gráfica
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        # Panel izquierdo con entradas y resultados.
        frame_izquierdo = tk.Frame(ventana_hija, bg=COLOR_FONDO_PRINCIPAL, padx=15, pady=15)
        frame_izquierdo.pack(side="left", fill="y")

        tk.Label(frame_izquierdo, text="Sistema de 2x2", font=("Impact", 16), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=5)
        # Recordatorio del formato que usa el programa.
        tk.Label(frame_izquierdo, text="ax + by = c", font=("Helvetica", 11, "italic"), fg=COLOR_TEXTO_TITULO, bg=COLOR_FONDO_PRINCIPAL).pack(pady=2)

        # Aquí se usa GRID (filas/columnas) en lugar de pack, porque las
        # ecuaciones necesitan alinearse en una tabla:
        #   col 0: etiqueta | col 1: a | col 2: "x +" | col 3: b | col 4: "y =" | col 5: c
        # IMPORTANTE: no se mezcla grid y pack dentro del MISMO contenedor;
        # por eso frame_inputs es un Frame aparte que solo usa grid.
        frame_inputs = tk.Frame(frame_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        frame_inputs.pack(pady=10)

        # ---------- Ecuación 1 (fila 0 de la cuadrícula) ----------
        tk.Label(frame_inputs, 
                text="Ecuación 1: ", 
                font=("Helvetica", 10, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).grid(row=0, column=0, pady=5)
        # Entry de "a1" con valor inicial "1". El ";" permite escribir varias
        # instrucciones en una línea: crear el Entry; colocarlo con grid; insertar valor.
        self.entry_a1 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_a1.grid(row=0, column=1); self.entry_a1.insert(0, "1")
        tk.Label(frame_inputs, text="x + ", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=2)
        # Entry de "b1".
        self.entry_b1 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_b1.grid(row=0, column=3); self.entry_b1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="y = ", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=4)
        # Entry de "c1" (el término independiente).
        self.entry_c1 = tk.Entry(frame_inputs, 
                                width=5, 
                                font=("Helvetica", 11)); self.entry_c1.grid(row=0, column=5); self.entry_c1.insert(0, "5")

        # ---------- Ecuación 2 (fila 1 de la cuadrícula) ----------
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
        # Con los valores por defecto el sistema es x+y=5, x-y=1 → solución (3, 2).

        # Botón que resuelve y grafica.
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

        # Etiqueta de resultados (determinante y solución).
        self.lbl_valores_clave_sist = tk.Label(frame_izquierdo, 
                                            text="Solución del sistema:\n-\n-", 
                                            font=("Helvetica", 10), 
                                            justify="left", 
                                            fg=COLOR_TEXTO_TITULO, 
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_sist.pack(anchor="w", pady=10)

        # Panel de la gráfica.
        self.frame_grafica_sist = tk.Frame(ventana_hija,
                                        bg="white", 
                                        bd=1, 
                                        relief="sunken")
        self.frame_grafica_sist.pack(side="right", 
                                    expand=True, 
                                    fill="both", 
                                    padx=15, 
                                    pady=15)


    # Resuelve el sistema 2x2 con álgebra lineal y grafica las dos rectas.
    def procesar_sistema_2x2(self):
        # Se leen los 6 coeficientes. Si alguno no es número, float() lanza
        # ValueError y se muestra el error. (Aquí NO se acepta coma decimal.)
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

        # Si a y b son ambos 0 la "ecuación" sería 0 = c: no es una recta.
        if (a1 == 0 and b1 == 0) or (a2 == 0 and b2 == 0):
            messagebox.showerror("Error matemático",
                                "En cada ecuación, 'a' y 'b' no pueden ser 0 a la vez (no sería una recta).")
            return

        # Forma matricial A·[x, y] = B:
        # A = matriz de coeficientes, B = vector de términos independientes.
        # ===== MATEMÁTICA: SISTEMA 2x2 EN FORMA MATRICIAL =====
        # Dos rectas:   a1·x + b1·y = c1
        #               a2·x + b2·y = c2
        # Se escribe como  A · [x, y] = B  con
        #     A = [[a1, b1],     (matriz de coeficientes)
        #          [a2, b2]]
        #     B = [c1, c2]       (términos independientes)
        # GEOMÉTRICAMENTE: la solución es el punto donde se cruzan las dos rectas.
        # np.array([[...], [...]]) crea una matriz (arreglo 2D): cada lista interior
        # es una fila.
        A = np.array([[a1, b1], 
                    [a2, b2]])
        B = np.array([c1, c2])

        # Determinante: si es 0, las rectas son paralelas o coincidentes y no
        # hay una solución única. isclose evita errores por decimales.
        # Para 2x2 el determinante es  det = a1·b2 - a2·b1. Vale 0 exactamente cuando
        # las rectas tienen la misma pendiente (a1/b1 = a2/b2), es decir, son
        # PARALELAS (sin solución) o COINCIDENTES (infinitas soluciones). En ambos
        # casos NO hay un único punto de cruce y no se puede resolver con solve.
        determinante = np.linalg.det(A)

        if np.isclose(determinante, 0):
            self.lbl_valores_clave_sist.config(text="--- VALORES CLAVE ---\nEl sistema NO tiene solución única.\n(Rectas paralelas o coincidentes)")
            solucion_existe = False
        else:
            # linalg.solve resuelve el sistema y devuelve [x, y].
            # solve usa eliminación gaussiana y devuelve [x, y]. Equivale a la regla de
            # Cramer:   x = (c1·b2 - c2·b1) / det     y     y = (a1·c2 - a2·c1) / det
            # Con las rectas por defecto (x+y=5 y x-y=1): det = -2, x = 3, y = 2.
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

        # Limpia la gráfica anterior.
        for widget in self.frame_grafica_sist.winfo_children():
            widget.destroy()

        # La gráfica se centra en la solución (±10 unidades en X); si no hay
        # solución se centra en 0. Se generan 100 valores de x.
        # La gráfica se "enfoca" alrededor de la solución: 10 unidades a cada lado en
        # X, para que el cruce quede al centro. x_vals (100 puntos) es el muestreo
        # con el que se evaluarán ambas rectas.
        centro_x = sol_x if solucion_existe else 0
        x_vals = np.linspace(centro_x - 10, centro_x + 10, 100)

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        
        # Recta 1: si b1 ≠ 0 se despeja y = (c1 - a1·x) / b1 y se dibuja.
        # DESPEJE PARA GRAFICAR: Matplotlib necesita pares (x, y). De  a·x + b·y = c  se
        # despeja la y:       b·y = c - a·x      ->      y = (c - a·x) / b
        # y se evalúa en todos los x_vals a la vez (vectorización). Solo se puede
        # dividir entre b si b ≠ 0; si b = 0 queda  a·x = c, una recta VERTICAL en
        # x = c/a (que no tiene "y = ..." y se dibuja con axvline).
        if b1 != 0:
            y_vals1 = (c1 - a1 * x_vals) / b1
            ax.plot(x_vals, y_vals1, color="#1B5E20", linewidth=2, label=f"{self._num(a1)}x + {self._num(b1)}y = {self._num(c1)}")
        else:
            # Si b1 = 0 queda a1·x = c1 → recta vertical en x = c1/a1
            # (a1 ≠ 0 está garantizado por la validación anterior).
            # Línea vertical punteada (linestyle="--") en x = c1/a1. Aquí a1 ≠ 0 siempre,
            # porque antes se validó que a y b no fueran 0 a la vez.
            ax.axvline(c1 / a1, color="#1B5E20", linewidth=2, linestyle="--", label=f"{self._num(a1)}x = {self._num(c1)}")

        # Recta 2: misma lógica, en naranja.
        if b2 != 0:
            y_vals2 = (c2 - a2 * x_vals) / b2
            ax.plot(x_vals, y_vals2, color="#E65100", linewidth=2, label=f"{self._num(a2)}x + {self._num(b2)}y = {self._num(c2)}")
        else:
            ax.axvline(c2 / a2, color="#E65100", linewidth=2, linestyle="--", label=f"{self._num(a2)}x = {self._num(c2)}")

        # Marca el punto de intersección en rojo, si existe.
        if solucion_existe:
            # Punto rojo en la intersección. Se dibuja DESPUÉS de las rectas para que quede
            # encima de ellas.
            ax.plot(sol_x, sol_y, 'ro', markersize=8, label=f"Intersección ({sol_x:.1f}, {sol_y:.1f})")

        # Ejes, cuadrícula, títulos y leyenda.
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_title("Intersección de Rectas (Sistema 2x2)", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        # Aquí la leyenda usa el tamaño de letra por defecto; muestra las 2 ecuaciones
        # y el punto de intersección (cada uno con su label).
        ax.legend()

        # Incrustar en Tkinter.
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_sist)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        plt.close(fig)



    # ------------------------------------------------------------------
    # VENTANA: SISTEMA 3x3  (a·x + b·y + c·z = d, tres ecuaciones = 3 planos)
    # ------------------------------------------------------------------
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

        # Tabla (grid) de entradas. Cada fila es una ecuación con 8 columnas:
        #   0: "Eq N:" | 1: a | 2: "x+" | 3: b | 4: "y+" | 5: c | 6: "z=" | 7: d
        # Los atributos se nombran entry_<letra>3_<número de ecuación>
        # (ej. entry_b3_2 = coeficiente "b" de la ecuación 2 del sistema 3x3).
        frame_inputs = tk.Frame(frame_izquierdo, 
                                bg=COLOR_FONDO_PRINCIPAL)
        frame_inputs.pack(pady=10)

        ## Ecuación 1 ##  (por defecto: x + y + z = 6)
        tk.Label(frame_inputs, 
                text="Eq 1: ", 
                font=("Helvetica", 9, "bold"), 
                fg=COLOR_TEXTO_TITULO, 
                bg=COLOR_FONDO_PRINCIPAL).grid(row=0, column=0, pady=5)
        # a1 (coeficiente de x)
        self.entry_a3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_a3_1.grid(row=0, column=1); self.entry_a3_1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="x+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=2)
        # b1 (coeficiente de y)
        self.entry_b3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_b3_1.grid(row=0, column=3); self.entry_b3_1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="y+", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=4)
        # c1 (coeficiente de z)
        self.entry_c3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_c3_1.grid(row=0, column=5); self.entry_c3_1.insert(0, "1")
        tk.Label(frame_inputs, 
                text="z=", 
                bg=COLOR_FONDO_PRINCIPAL, 
                fg=COLOR_TEXTO_TITULO).grid(row=0, column=6)
        # d1 (término independiente)
        self.entry_d3_1 = tk.Entry(frame_inputs, 
                                width=4, 
                                font=("Helvetica", 10)); self.entry_d3_1.grid(row=0, column=7); self.entry_d3_1.insert(0, "6")

        ## Ecuación 2 ##  (por defecto: 0x + 2y + 5z = -4; misma estructura, fila 1)
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

        ## Ecuación 3 ##  (por defecto: 2x + 5y - z = 27; misma estructura, fila 2)
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

        # Botón que resuelve el sistema y dibuja los 3 planos.
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

        # Etiqueta de resultados (determinante y x, y, z).
        self.lbl_valores_clave_3x3 = tk.Label(frame_izquierdo, 
                                            text="Solución del sistema:\n-\n-", 
                                            font=("Helvetica", 10), 
                                            justify="left", 
                                            fg=COLOR_TEXTO_TITULO, 
                                            bg=COLOR_FONDO_PRINCIPAL)
        self.lbl_valores_clave_3x3.pack(anchor="w", pady=10)

        # Panel de la gráfica 3D.
        self.frame_grafica_3x3 = tk.Frame(ventana_hija, 
                                        bg="white", 
                                        bd=1, 
                                        relief="sunken")
        self.frame_grafica_3x3.pack(side="right", 
                                    expand=True, 
                                    fill="both", 
                                    padx=15, 
                                    pady=15)


    # Dibuja UN plano ax + by + cz = d sobre los ejes 3D "ax".
    # Un plano 3D se dibuja como superficie: hay que calcular una coordenada
    # a partir de las otras dos. Se elige despejar la variable cuyo
    # coeficiente no sea 0 (así nunca se divide entre cero).
    def _dibujar_plano(self, ax, a, b, c, d, x_rango, y_rango, z_rango, color):
        """Dibuja el plano ax + by + cz = d. Si c = 0 es un plano vertical y se despeja y (o x)."""
        if c != 0:
            # Caso normal: se despeja z = (d - a·x - b·y) / c.
            # meshgrid convierte los rangos 1D en dos mallas 2D (todas las
            # combinaciones x,y) para poder calcular Z en cada punto.
            # ===== MATEMÁTICA Y TÉCNICA: CÓMO SE DIBUJA UN PLANO EN 3D =====
            # Un plano  a·x + b·y + c·z = d  es una SUPERFICIE: para cada pareja (x, y)
            # existe un z. Para dibujarlo se calcula z sobre una cuadrícula de parejas.
            # np.meshgrid(x_rango, y_rango) crea las cuadrículas: si
            #     x_rango = [1, 2, 3]   y   y_rango = [10, 20]
            # devuelve dos matrices de 2 filas × 3 columnas:
            #     X = [[1, 2, 3],        Y = [[10, 10, 10],
            #          [1, 2, 3]]             [20, 20, 20]]
            # Así (X[i][j], Y[i][j]) recorre TODAS las combinaciones de x e y. Con 20×20
            # puntos se obtienen 400 parejas por plano.
            # Despejando z de la ecuación del plano:   z = (d - a·x - b·y) / c
            # La operación se aplica a toda la malla a la vez (vectorizada) y da una
            # matriz Z del mismo tamaño que X e Y. Se requiere c ≠ 0 para dividir.
            X, Y = np.meshgrid(x_rango, y_rango)
            Z = (d - a * X - b * Y) / c
        elif b != 0:
            # Si c = 0 (plano "vertical") y b ≠ 0: se despeja y = (d - a·x) / b,
            # y la malla se arma con x y z.
            # Si c = 0 el plano no depende de z (es "vertical", como una pared) y no se
            # puede despejar z. Entonces se despeja y:   a·x + b·y = d  ->  y = (d - a·x)/b
            # y la malla se construye con las variables libres x y z.
            X, Z = np.meshgrid(x_rango, z_rango)
            Y = (d - a * X) / b
        else:
            # Si b = c = 0 solo queda a·x = d → x constante = d/a (a ≠ 0
            # garantizado por la validación). Malla con y y z; full_like crea un
            # arreglo del mismo tamaño que Y relleno con el valor d/a.
            Y, Z = np.meshgrid(y_rango, z_rango)
            # Si b = c = 0 solo queda  a·x = d  ->  x = d/a: un plano donde x es siempre
            # la misma constante. np.full_like(Y, d/a) crea una matriz con la forma de Y
            # pero llena con ese valor; las variables libres son y y z.
            X = np.full_like(Y, d / a)
        # plot_surface dibuja la superficie; alpha=0.5 la hace semitransparente
        # para ver cómo se cruzan los planos.
        # plot_surface(X, Y, Z) recibe tres matrices del mismo tamaño y las interpreta
        # como una malla de puntos 3D; une los vecinos formando pequeños cuadriláteros
        # (parches) y los rellena de color. alpha=0.5 -> 50% transparente, para ver
        # los otros planos a través de éste y notar dónde se intersectan.
        ax.plot_surface(X, Y, Z, alpha=0.5, color=color)


    # Resuelve el sistema 3x3 con álgebra lineal y grafica los tres planos.
    def procesar_sistema_3x3(self):
        try:
            # 1. Recuperar los coeficientes de las 3 ecuaciones
            # Cada línea lee (a, b, c, d) de una ecuación; el desempaquetado
            # múltiple asigna los cuatro valores de una vez.
            a1, b1, c1, d1 = float(self.entry_a3_1.get()), float(self.entry_b3_1.get()), float(self.entry_c3_1.get()), float(self.entry_d3_1.get())
            a2, b2, c2, d2 = float(self.entry_a3_2.get()), float(self.entry_b3_2.get()), float(self.entry_c3_2.get()), float(self.entry_d3_2.get())
            a3, b3, c3, d3 = float(self.entry_a3_3.get()), float(self.entry_b3_3.get()), float(self.entry_c3_3.get()), float(self.entry_d3_3.get())
        except ValueError:
            messagebox.showerror("Error de datos", "Por favor, introduce números válidos en todos los coeficientes.")
            return

        # any(...) es True si ALGUNA ecuación tiene a = b = c = 0 (no sería un
        # plano). Se recorre cada terna (a, b, c) con una expresión generadora.
        if any(a == 0 and b == 0 and c == 0 for a, b, c in ((a1, b1, c1), (a2, b2, c2), (a3, b3, c3))):
            messagebox.showerror("Error matemático",
                                "En cada ecuación, 'a', 'b' y 'c' no pueden ser 0 a la vez (no sería un plano).")
            return

        # 2. Configurar matrices con NumPy
        # A = matriz 3x3 de coeficientes; B = vector de términos independientes.
        # ===== MATEMÁTICA: SISTEMA 3x3 =====
        # Cada ecuación a·x + b·y + c·z = d es un PLANO en el espacio, y el vector
        # (a, b, c) es su "normal" (la dirección perpendicular al plano). El sistema
        # se escribe como  A · [x, y, z] = B  con una fila de A por ecuación.
        # GEOMÉTRICAMENTE: la solución es el punto donde se cortan los 3 planos.
        # El determinante de una matriz 3x3 equivale al producto triple de las tres
        # normales (el volumen del paralelepípedo que forman). Si es 0, las normales
        # son "coplanares" (dependientes), y los planos son paralelos o se cortan en
        # una recta o en nada: no hay un único punto. np.isclose(det, 0) lo detecta.
        A = np.array([[a1, b1, c1],
                    [a2, b2, c2],
                    [a3, b3, c3]])
        B = np.array([d1, d2, d3])

        determinante = np.linalg.det(A)

        # Verificar si hay solución única
        # det ≈ 0 → los planos no se cortan en un único punto.
        if np.isclose(determinante, 0):
            self.lbl_valores_clave_3x3.config(text="--- VALORES CLAVE ---\nEl sistema NO tiene solución única.\n(Planos paralelos o infinitas intersecciones)")
            solucion_existe = False
        else:
            # Solución única: se resuelve A·[x, y, z] = B.
            # Eliminación gaussiana sobre una matriz 3x3. Devuelve [x, y, z].
            # Con los valores por defecto el sistema da (x, y, z) = (5, 3, -2)
            # (se puede verificar sustituyendo esos valores en las 3 ecuaciones).
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
        # La vista se centra en la solución (o en el origen si no hay).
        centro_x = sol_x if solucion_existe else 0
        centro_y = sol_y if solucion_existe else 0
        centro_z = sol_z if solucion_existe else 0

        # Rangos de ±5 unidades alrededor del centro, con 20 puntos por eje
        # (malla de 20x20 por plano).
        # Los 3 rangos (x, y, z) abarcan ±5 unidades alrededor del punto de solución,
        # con 20 muestras cada uno. Con menos muestras los planos se ven "facetados";
        # con más, la gráfica se vuelve lenta de dibujar y de rotar.
        x_rango = np.linspace(centro_x - 5, centro_x + 5, 20)
        y_rango = np.linspace(centro_y - 5, centro_y + 5, 20)
        z_rango = np.linspace(centro_z - 5, centro_z + 5, 20)

        # Inicializamos la figura de Matplotlib indicando explícitamente que es proyección 3D
        # (111 = 1 fila, 1 columna, subgráfica número 1).
        # Aquí se usa plt.figure() (solo el lienzo, sin ejes) en lugar de
        # plt.subplots(), porque el eje 3D se debe crear aparte indicando la proyección.
        fig = plt.figure(figsize=(5, 4), dpi=100)
        # add_subplot(111) agrega un Axes a la figura. "111" significa una cuadrícula
        # de 1 fila × 1 columna y se elige la subgráfica 1 (o sea, la única).
        # projection='3d' hace que el Axes sea un Axes3D: tiene eje Z y permite
        # plot_surface, scatter 3D y rotar la vista con el mouse.
        ax = fig.add_subplot(111, projection='3d')

        # Dibujamos los planos con transparencias (alpha) para que se vea dónde se cruzan
        # Un color distinto por plano: verde, naranja y azul.
        self._dibujar_plano(ax, a1, b1, c1, d1, x_rango, y_rango, z_rango, 'green')
        self._dibujar_plano(ax, a2, b2, c2, d2, x_rango, y_rango, z_rango, 'orange')
        self._dibujar_plano(ax, a3, b3, c3, d3, x_rango, y_rango, z_rango, 'blue')

        # Siempre se enmarca la vista (con o sin solución) para que no se estire la escala
        # Fija los límites de cada eje para que los planos muy inclinados no
        # deformen la escala de la gráfica.
        # Los planos son infinitos y la fórmula puede producir valores enormes de z
        # (por ejemplo si c es muy pequeño). Fijar los límites de X, Y y Z evita que
        # la escala se estire y deje la zona de intersección diminuta.
        ax.set_xlim(centro_x - 5, centro_x + 5)
        ax.set_ylim(centro_y - 5, centro_y + 5)
        ax.set_zlim(centro_z - 5, centro_z + 5)

        # Si hay solución, marcamos el punto exacto de intersección en el espacio con una esfera roja
        if solucion_existe:
            # scatter dibuja un punto en 3D; depthshade=False evita que se
            # atenúe según la profundidad (se vea siempre rojo intenso).
            # scatter dibuja puntos sueltos (aquí uno solo) en el espacio: s=50 es el
            # tamaño del marcador; depthshade=False evita que Matplotlib atenúe el color
            # según qué tan lejos está, y así el punto siempre se ve rojo y visible.
            ax.scatter(sol_x, sol_y, sol_z, color='red', s=50, depthshade=False, label=f"Solución ({sol_x:.1f}, {sol_y:.1f}, {sol_z:.1f})")
            ax.legend(fontsize=8)

        # Configurar etiquetas espaciales
        ax.set_title("Intersección de Planos 3D", fontsize=12, fontweight='bold', color="#1E4620")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.set_zlabel("Eje Z")
        
        # 5. Incrustar en Tkinter
        # Mismo mecanismo que en las gráficas 2D (ver explicación en primer grado).
        # La figura 3D se renderiza una vez; para rotarla de forma interactiva con el
        # mouse haría falta además una barra de herramientas o eventos de ratón.
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica_3x3)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        plt.close(fig)


### Ejecutar la aplicación ###
# Este bloque solo se ejecuta si el archivo se corre directamente
# (python main.py) y NO si otro archivo lo importa como módulo.
if __name__ == "__main__":
    # Crea la ventana raíz de Tkinter.
    raiz = tk.Tk()
    # Crea el menú principal sobre esa ventana (se ejecuta __init__).
    app = MenuPrincipal(raiz)
    # mainloop() inicia el bucle de eventos: mantiene la ventana abierta y
    # atenta a clics y teclas hasta que el usuario la cierre.
    raiz.mainloop()
