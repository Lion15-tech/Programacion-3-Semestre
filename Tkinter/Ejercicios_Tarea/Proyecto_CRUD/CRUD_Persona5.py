# ============================================================
# IMPORTACIONES
# ============================================================

# Importamos el módulo "tkinter", la librería estándar de Python
# para crear ventanas, botones, campos de texto, etc.
# "as tk" le pone un apodo corto: así escribimos tk.Canvas
# en lugar de tkinter.Canvas.
import tkinter as tk

# Importamos "messagebox" desde tkinter. Es el submódulo que
# permite mostrar ventanitas emergentes (avisos, alertas, etc.).
# Hay que importarlo aparte porque "import tkinter" no lo trae.
from tkinter import messagebox


# ============================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# ============================================================

# Una clase es una "plantilla" que agrupa datos (variables) y
# acciones (funciones) relacionados. Aquí toda la aplicación
# vive dentro de una sola clase.
class Persona5CRUDScroll:
    """
    Esta clase representa toda nuestra aplicación gráfica.

    Dentro de ella tenemos:
    - La ventana principal.
    - Los datos de los objetivos.
    - El formulario.
    - Los botones.
    - La lista con scroll.
    - Las operaciones CRUD:
        C = Create  -> Crear
        R = Read    -> Leer/mostrar
        U = Update  -> Actualizar
        D = Delete  -> Eliminar
    """

    # ========================================================
    # CONSTRUCTOR DE LA CLASE
    # ========================================================

    # __init__ es el método especial que Python ejecuta
    # automáticamente al crear un objeto de la clase.
    # "self" es el propio objeto: nos sirve para guardar datos
    # en él (self.algo) y acceder a ellos desde otros métodos.
    # "root" es la ventana principal de Tkinter que recibimos
    # desde fuera (se crea al final del archivo).
    def __init__(self, root):
        """
        __init__ se ejecuta automáticamente cuando creamos
        un objeto de la clase.

        'root' representa la ventana principal de Tkinter.
        """

        # Guardamos la ventana en el objeto. Sin esto, "root"
        # sería una variable local que desaparece al terminar
        # __init__. Con self.root podemos usarla en cualquier
        # otro método de la clase.
        self.root = root

        # Cambia el texto de la barra de título de la ventana.
        self.root.title("Phantom Thieves - Target Database (P5R Style)")

        # Fija el tamaño de la ventana con el formato
        # "ANCHOxALTO" en píxeles: 950 de ancho, 650 de alto.
        self.root.geometry("950x650")

        # Pone el color de fondo de la ventana en negro.
        # Los colores se pueden escribir en hexadecimal
        # "#RRGGBB" (rojo, verde, azul; 00 = nada, FF = máximo).
        # "#000000" es negro.
        self.root.configure(bg="#000000")

        # resizable(ancho, alto): indica si el usuario puede
        # cambiar el tamaño en cada dirección. Con False, False
        # la ventana queda con tamaño fijo.
        self.root.resizable(False, False)


        # ====================================================
        # BASE DE DATOS SIMULADA
        # ====================================================

        # Esta lista funciona como una pequeña "base de datos"
        # en memoria: se pierde cuando cierras el programa.
        # No usamos MySQL, SQLite, PostgreSQL, etc.
        #
        # Cada elemento de la lista es un diccionario
        # (pares clave: valor) y cada diccionario es un objetivo.
        self.targets = [

            # Primer objetivo.
            {
                "id": 1,                      # Identificador único.
                "nombre": "Suguru Kamoshida",  # Nombre del objetivo.
                "crimen": "Abuso de Poder"     # Su "crimen".
            },

            # Segundo objetivo.
            {
                "id": 2,
                "nombre": "Ichiryusai Madarame",
                "crimen": "Plagio de Arte"
            },

            # Tercer objetivo.
            {
                "id": 3,
                "nombre": "Junya Kaneshiro",
                "crimen": "Extorsión Mafiosa"
            },

            # Cuarto objetivo.
            {
                "id": 4,
                "nombre": "Kunikazu Okumura",
                "crimen": "Explotación Laboral"
            },

            # Quinto objetivo.
            {
                "id": 5,
                "nombre": "Sae Niijima",
                "crimen": "Corrupción Judicial"
            },

            # Sexto objetivo.
            {
                "id": 6,
                "nombre": "Masayoshi Shidou",
                "crimen": "Abuso Político Extremo"
            },

            # Séptimo objetivo.
            {
                "id": 7,
                "nombre": "Takuto Maruki",
                "crimen": "Distorsión de la Realidad"
            }
        ]  # Aquí termina la lista de objetivos.


        # ID que tendrá el siguiente objetivo que se cree.
        # Ya existen los IDs del 1 al 7, así que el próximo es 8.
        # Nunca se reutiliza un ID, aunque se borre un objetivo.
        self.next_id = 8

        # Guarda el ID del objetivo que el usuario ha elegido
        # en la lista. None significa "ninguno" (valor vacío
        # de Python), que es como empieza el programa.
        self.selected_target_id = None


        # ====================================================
        # LIENZO PRINCIPAL
        # ====================================================

        # Canvas es un widget de Tkinter sobre el que se puede
        # dibujar líneas, polígonos, texto, imágenes... y también
        # colocar otros widgets encima. Este será el "fondo" de
        # toda la aplicación.
        self.canvas_main = tk.Canvas(
            root,                   # Widget padre: dentro de qué va.
            width=950,              # Ancho en píxeles.
            height=650,             # Alto en píxeles.
            bg="black",             # Color de fondo (por nombre).
            highlightthickness=0    # Quita el borde de "foco" que
                                    # Tkinter dibuja alrededor.
        )

        # pack() coloca el widget en la ventana.
        self.canvas_main.pack(
            fill="both",   # Se estira en horizontal y vertical.
            expand=True    # Aprovecha todo el espacio libre.
        )


        # ====================================================
        # DECORACIONES DEL FONDO
        # ====================================================

        # En el Canvas, el punto (0, 0) es la esquina superior
        # izquierda. La X crece hacia la derecha y la Y crece
        # hacia ABAJO (al revés que en matemáticas).
        #
        # create_polygon(x1, y1, x2, y2, ...) dibuja una figura
        # uniendo los puntos en orden. Imita el estilo de
        # diagonales de Persona 5.

        # Figura 1: gran panel rojo diagonal a la izquierda.
        self.canvas_main.create_polygon(
            0, 0,        # Punto 1: esquina superior izquierda.
            500, 0,      # Punto 2: arriba, en x = 500.
            350, 650,    # Punto 3: abajo, en x = 350 (inclinado).
            0, 650,      # Punto 4: esquina inferior izquierda.
            fill="#DC0000"  # Color de relleno: rojo.
        )

        # Figura 2: franja blanca diagonal que separa el panel
        # rojo del resto de la pantalla.
        self.canvas_main.create_polygon(
            490, 0,      # Arriba, borde izquierdo de la franja.
            515, 0,      # Arriba, borde derecho de la franja.
            365, 650,    # Abajo, borde derecho.
            340, 650,    # Abajo, borde izquierdo.
            fill="#FFFFFF"  # Blanco.
        )

        # Figura 3: triángulo negro en la esquina inferior
        # izquierda (recorta un pedazo del panel rojo).
        self.canvas_main.create_polygon(
            0, 500,      # Punto sobre el borde izquierdo.
            150, 650,    # Punto sobre el borde inferior.
            0, 650,      # Esquina inferior izquierda.
            fill="#000000"  # Negro.
        )

        # Figura 4: triángulo rojo en la esquina superior derecha.
        self.canvas_main.create_polygon(
            800, 0,      # Punto sobre el borde superior.
            950, 0,      # Esquina superior derecha.
            950, 100,    # Punto sobre el borde derecho.
            fill="#DC0000"  # Rojo.
        )


        # ====================================================
        # TÍTULO PRINCIPAL
        # ====================================================

        # create_text() dibuja texto directamente en el Canvas.
        self.canvas_main.create_text(
            40,                       # Posición X.
            35,                       # Posición Y.
            text="PHANTOM TARGETS",   # Texto a mostrar.
            fill="#FFFFFF",           # En un Canvas, "fill" es el
                                      # color del texto (blanco).
            font=("Impact", 38),      # Fuente y tamaño.
            angle=6,                  # Rotación en grados
                                      # (requiere Tk 8.6 o superior).
            anchor="nw"               # El punto (40, 35) es la
                                      # esquina superior izquierda
                                      # del texto (nw = noroeste).
        )

        # Subtítulo en amarillo, justo debajo del título.
        self.canvas_main.create_text(
            43,                            # Posición X.
            85,                            # Posición Y.
            text="DATABASE SYSTEM v2.0",   # Texto.
            fill="#FFF200",                # Amarillo.
            font=("Impact", 16),           # Fuente más pequeña.
            angle=4,                       # Rotación ligera.
            anchor="nw"                    # Ancla: esquina sup. izq.
        )


        # ====================================================
        # ETIQUETAS DEL FORMULARIO
        # ====================================================

        # Rótulo que indica dónde escribir el nombre.
        self.canvas_main.create_text(
            50,                     # Posición X.
            160,                    # Posición Y.
            text="TARGET NAME:",    # Texto del rótulo.
            fill="#000000",         # Negro (se lee sobre el rojo).
            font=("Impact", 16),    # Fuente y tamaño.
            anchor="w"              # El punto es el centro del lado
                                    # izquierdo del texto (w = oeste).
        )

        # Rótulo que indica dónde escribir el crimen.
        self.canvas_main.create_text(
            50,                        # Posición X.
            230,                       # Posición Y.
            text="CRIME / PALACE:",    # Texto del rótulo.
            fill="#000000",            # Negro.
            font=("Impact", 16),       # Fuente y tamaño.
            anchor="w"                 # Ancla: centro izquierdo.
        )


        # ====================================================
        # CAMPOS DE TEXTO
        # ====================================================

        # Entry es una caja de texto de una sola línea donde
        # el usuario puede escribir.

        # Campo para el nombre del objetivo.
        self.entry_name = tk.Entry(
            root,                          # Widget padre: la ventana.
            font=("Arial", 12, "bold"),    # Fuente, tamaño y negrita.
            bg="#FFFFFF",                  # Fondo blanco.
            fg="#000000",                  # Color del texto (negro).
            bd=3,                          # Grosor del borde (píxeles).
            relief="solid"                 # Estilo del borde: línea
                                           # sólida y plana.
        )

        # Campo para el crimen (mismo estilo que el anterior).
        self.entry_crime = tk.Entry(
            root,
            font=("Arial", 12, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            bd=3,
            relief="solid"
        )

        # Los Entry se crearon pero todavía no se ven: hay que
        # colocarlos. Usamos create_window para meterlos dentro
        # del Canvas, en una posición exacta.

        # Colocamos el campo del nombre.
        self.canvas_main.create_window(
            50,                    # Posición X.
            190,                   # Posición Y.
            window=self.entry_name,  # Widget que se coloca.
            anchor="w",            # Ancla: centro del lado izquierdo.
            width=250,             # Ancho del widget en píxeles.
            height=30              # Alto del widget en píxeles.
        )

        # Colocamos el campo del crimen.
        self.canvas_main.create_window(
            50,
            260,
            window=self.entry_crime,
            anchor="w",
            width=250,
            height=30
        )


        # ====================================================
        # BOTONES DE ACCIÓN
        # ====================================================

        # En vez de usar tk.Button, los "botones" son texto
        # dibujado en el Canvas (así pueden ir inclinados y con
        # fuente Impact). Los creamos con el método
        # crear_boton_canvas, definido más abajo.
        #
        # Sus argumentos son:
        #   1) un nombre interno (etiqueta / tag),
        #   2) posición X,
        #   3) posición Y,
        #   4) texto visible,
        #   5) función a ejecutar al hacer clic
        #      (sin paréntesis: se pasa la función, no se llama).

        # Botón para CREAR.
        self.crear_boton_canvas(
            "btn_create",
            50,
            320,
            "> EXECUTE (CREATE)",
            self.ejecutar_crear
        )

        # Botón para ACTUALIZAR.
        self.crear_boton_canvas(
            "btn_update",
            50,
            380,
            "> ALTER (UPDATE)",
            self.ejecutar_actualizar
        )

        # Botón para ELIMINAR.
        self.crear_boton_canvas(
            "btn_delete",
            50,
            440,
            "> PURGE (DELETE)",
            self.ejecutar_borrar
        )

        # Botón para limpiar el formulario.
        self.crear_boton_canvas(
            "btn_clear",
            50,
            500,
            "> RESET FORM",
            self.limpiar_formulario
        )


        # ====================================================
        # TÍTULO DE LA LISTA DERECHA
        # ====================================================

        # Título de la lista de objetivos.
        self.canvas_main.create_text(
            530,                              # Posición X.
            60,                               # Posición Y.
            text="CURRENT TARGETS IN PALACE",  # Texto.
            fill="#FFFFFF",                   # Blanco.
            font=("Impact", 20),              # Fuente y tamaño.
            anchor="nw"                       # Ancla: esq. sup. izq.
        )

        # Pista para el usuario, en gris e itálica.
        self.canvas_main.create_text(
            530,
            90,
            text="(Use mouse wheel to scroll list)",
            fill="#666666",                   # Gris oscuro.
            font=("Arial", 10, "italic"),     # Arial cursiva.
            anchor="nw"
        )


        # ====================================================
        # CONTENEDOR DEL SCROLL
        # ====================================================

        # Frame es un contenedor rectangular vacío donde se
        # pueden agrupar otros widgets.
        self.scroll_frame = tk.Frame(
            root,       # Widget padre.
            bg="black"  # Fondo negro.
        )

        # Metemos el Frame dentro del Canvas principal, en la
        # zona derecha de la pantalla.
        self.canvas_main.create_window(
            520,                      # Posición X.
            120,                      # Posición Y.
            window=self.scroll_frame,  # Widget que se coloca.
            anchor="nw",              # Ancla: esquina sup. izq.
            width=400,                # Ancho del contenedor.
            height=500                # Alto del contenedor.
        )


        # ====================================================
        # CANVAS INTERNO DE LA LISTA
        # ====================================================

        # Segundo Canvas, dentro del Frame. Es el que contiene
        # las "tarjetas" de los objetivos y el que se desplaza
        # (scroll) cuando hay más tarjetas de las que caben.
        self.canvas_list = tk.Canvas(
            self.scroll_frame,       # Widget padre: el Frame.
            bg="black",              # Fondo negro.
            highlightthickness=0,    # Sin borde de foco.
            bd=0                     # Sin borde normal.
        )

        # Lo colocamos dentro del Frame.
        self.canvas_list.pack(
            side="left",   # Pegado al lado izquierdo del Frame.
            fill="both",   # Rellena en ambas direcciones.
            expand=True    # Ocupa el espacio disponible.
        )


        # ====================================================
        # EVENTOS DEL RATÓN
        # ====================================================

        # bind(evento, función) significa: "cuando ocurra este
        # evento sobre este widget, llama a esta función".
        # La rueda del ratón genera eventos distintos según el
        # sistema operativo, por eso registramos tres.

        # <MouseWheel>: rueda en Windows y macOS.
        self.canvas_list.bind(
            "<MouseWheel>",
            self.on_mouse_wheel
        )

        # <Button-4>: rueda hacia arriba en muchos Linux.
        self.canvas_list.bind(
            "<Button-4>",
            self.on_mouse_wheel
        )

        # <Button-5>: rueda hacia abajo en muchos Linux.
        self.canvas_list.bind(
            "<Button-5>",
            self.on_mouse_wheel
        )


        # Dibujamos por primera vez la lista de objetivos.
        self.actualizar_lista_visual()


    # ========================================================
    # CONTROL DEL SCROLL
    # ========================================================

    # Este método lo llama Tkinter cada vez que se mueve la
    # rueda del ratón sobre la lista. Tkinter le pasa "event",
    # un objeto con información de lo ocurrido.
    def on_mouse_wheel(self, event):
        """
        Se ejecuta cuando el usuario mueve la rueda del ratón.
        """

        # event.num: número de botón (4 = rueda arriba en Linux).
        # event.delta: cantidad de giro; positivo = hacia arriba
        # en Windows/macOS (en Linux vale 0).
        # Con "or", basta con que se cumpla una de las dos.
        if event.num == 4 or event.delta > 0:

            # yview_scroll(cantidad, unidad) desplaza la vista
            # verticalmente. -1 = una unidad hacia arriba.
            self.canvas_list.yview_scroll(
                -1,        # Cantidad: negativa = subir.
                "units"    # Unidad: pasos pequeños del Canvas.
            )

        # Si no fue hacia arriba, comprobamos si fue hacia abajo
        # (botón 5 en Linux, o delta negativo en Windows/macOS).
        elif event.num == 5 or event.delta < 0:

            # 1 = una unidad hacia abajo.
            self.canvas_list.yview_scroll(
                1,         # Cantidad: positiva = bajar.
                "units"    # Unidad: pasos pequeños del Canvas.
            )


    # ========================================================
    # CREAR BOTONES PERSONALIZADOS
    # ========================================================

    # Método auxiliar que evita repetir el mismo código para
    # cada botón. Recibe:
    #   tag_base -> nombre interno del botón,
    #   x, y     -> posición,
    #   texto    -> lo que se lee en pantalla,
    #   comando  -> función que se ejecuta al hacer clic.
    def crear_boton_canvas(
        self,
        tag_base,
        x,
        y,
        texto,
        comando
    ):
        """
        Crea un "botón" utilizando texto dentro del Canvas.

        Parámetros:
        - tag_base -> identificador del botón.
        - x, y -> posición.
        - texto -> texto que aparecerá.
        - comando -> función que se ejecutará al hacer clic.
        """

        # Dibujamos el texto del botón. create_text devuelve un
        # número (el ID del elemento dibujado) que guardamos en
        # text_id para poder modificarlo o asociarle eventos.
        text_id = self.canvas_main.create_text(
            x,                   # Posición X recibida.
            y,                   # Posición Y recibida.
            text=texto,          # Texto recibido.
            fill="#FFFFFF",      # Color inicial: blanco.
            font=("Impact", 18), # Fuente y tamaño.
            angle=3,             # Ligera inclinación.
            anchor="nw",         # Ancla: esquina sup. izq.
            tags=tag_base        # Etiqueta para identificarlo.
        )


        # ====================================================
        # EVENTO: EL RATÓN ENTRA
        # ====================================================

        # tag_bind(elemento, evento, función) es como bind(), pero
        # para un elemento concreto dibujado en el Canvas.
        # <Enter> ocurre cuando el cursor entra sobre el elemento.
        # Al entrar, cambiamos el color del texto a amarillo con
        # itemconfig (que modifica propiedades de un elemento).
        self.canvas_main.tag_bind(
            text_id,
            "<Enter>",
            lambda e: self.canvas_main.itemconfig(
                text_id,
                fill="#FFF200"   # Amarillo (efecto "hover").
            )
        )


        # ====================================================
        # EVENTO: EL RATÓN SALE
        # ====================================================

        # <Leave> ocurre cuando el cursor sale del elemento.
        # Devolvemos el texto a blanco.
        self.canvas_main.tag_bind(
            text_id,
            "<Leave>",
            lambda e: self.canvas_main.itemconfig(
                text_id,
                fill="#FFFFFF"   # Vuelve al blanco original.
            )
        )


        # ====================================================
        # EVENTO: CLIC
        # ====================================================

        # <Button-1> es el clic con el botón izquierdo del ratón.
        # Al hacer clic, se ejecuta la función "comando"
        # (por ejemplo, ejecutar_crear).
        self.canvas_main.tag_bind(
            text_id,
            "<Button-1>",
            lambda e: comando()
        )


        # ----------------------------------------------------
        # ¿QUÉ ES lambda?
        # ----------------------------------------------------
        #
        # lambda crea una función pequeña sin nombre, escrita
        # en una sola línea.
        #
        # lambda e: comando()
        #
        # equivale a:
        #
        # def funcion(e):
        #     comando()
        #
        # La "e" es el objeto evento que Tkinter siempre envía
        # a estas funciones. Aquí no lo necesitamos, pero hay que
        # recibirlo igualmente o Python daría error.


    # ========================================================
    # ACTUALIZAR VISUALMENTE LA LISTA
    # ========================================================

    def actualizar_lista_visual(self):
        """
        Borra la lista actual y vuelve a dibujarla
        utilizando los datos existentes en self.targets.

        Esta función representa principalmente la parte
        READ del CRUD.
        """

        # Borramos todo lo dibujado en el Canvas de la lista.
        # Cada vez que algo cambia, se dibuja todo desde cero.
        self.canvas_list.delete("all")

        # Coordenada Y donde empieza la primera tarjeta.
        start_y = 10

        # Altura de cada tarjeta, en píxeles.
        card_height = 65

        # Espacio vertical entre una tarjeta y la siguiente.
        spacing = 15

        # enumerate() recorre la lista entregando dos valores:
        #   i      -> posición: 0, 1, 2, 3...
        #   target -> el diccionario de esa posición.
        # Ejemplo: i = 0, target = {"id": 1, ...}
        #          i = 1, target = {"id": 2, ...}
        for i, target in enumerate(self.targets):

            # Posición vertical de esta tarjeta: cada una se
            # desplaza (altura + espacio) por cada posición.
            y_pos = start_y + (
                i * (card_height + spacing)
            )


            # =================================================
            # COLORES DE LA TARJETA
            # =================================================

            # Sintaxis: valor_A if condición else valor_B.
            # Si el objetivo es el seleccionado, la tarjeta es
            # amarilla; si no, gris muy oscuro.
            bg_color = (
                "#FFF200"
                if target["id"] == self.selected_target_id
                else "#111111"
            )

            # Color del nombre: negro sobre amarillo si está
            # seleccionado, blanco sobre gris si no.
            text_color = (
                "#000000"
                if target["id"] == self.selected_target_id
                else "#FFFFFF"
            )

            # Color del texto del crimen: gris oscuro si está
            # seleccionado, rojo si no.
            subtext_color = (
                "#333333"
                if target["id"] == self.selected_target_id
                else "#DC0000"
            )


            # =================================================
            # DIBUJAR LA TARJETA
            # =================================================

            # Polígono de 4 puntos ligeramente torcido que hace
            # de fondo de la tarjeta. Guardamos su ID en panel_id
            # para poder asociarle el clic más adelante.
            panel_id = self.canvas_list.create_polygon(
                10,                       # Punto 1 X: arriba-izq.
                y_pos,                    # Punto 1 Y.

                370,                      # Punto 2 X: arriba-der.
                y_pos + 5,                # Punto 2 Y (un poco más baja).

                350,                      # Punto 3 X: abajo-der.
                y_pos + card_height,      # Punto 3 Y.

                20,                       # Punto 4 X: abajo-izq.
                y_pos + card_height - 5,  # Punto 4 Y.

                fill=bg_color,            # Color de relleno elegido.

                # outline = color del borde. Blanco si está
                # seleccionado; cadena vacía "" = sin borde.
                outline=(
                    "#FFFFFF"
                    if target["id"] == self.selected_target_id
                    else ""
                ),

                width=2                   # Grosor del borde.
            )


            # =================================================
            # NOMBRE DEL OBJETIVO
            # =================================================

            # Texto con el nombre, dentro de la tarjeta.
            txt_name_id = self.canvas_list.create_text(
                40,                          # Posición X.
                y_pos + 12,                  # Posición Y.

                # f-string: una cadena con f delante permite
                # insertar valores entre llaves {}.
                # .upper() convierte el texto a MAYÚSCULAS.
                # Se usan comillas simples dentro ('nombre')
                # porque la cadena exterior usa dobles.
                text=f"{target['nombre'].upper()}",

                fill=text_color,             # Color según selección.
                font=("Impact", 16),         # Fuente y tamaño.
                anchor="nw"                  # Ancla: esq. sup. izq.
            )


            # =================================================
            # CRIMEN
            # =================================================

            # Texto con el crimen, debajo del nombre.
            txt_crime_id = self.canvas_list.create_text(
                40,                          # Posición X.
                y_pos + 38,                  # Posición Y (más abajo).

                # f-string que une la palabra "CRIME: " con el
                # crimen guardado en el diccionario.
                text=f"CRIME: {target['crimen']}",

                fill=subtext_color,          # Color según selección.
                font=("Arial", 10, "bold"),  # Arial negrita.
                anchor="nw"                  # Ancla: esq. sup. izq.
            )


            # =================================================
            # HACER LA TARJETA INTERACTIVA
            # =================================================

            # Función interna que selecciona un objetivo.
            # "t=target" es un parámetro con valor por defecto:
            # guarda el objetivo de ESTA vuelta del bucle.
            def registrar_click(t=target):
                return self.seleccionar_target(t)

            # Recorremos los tres elementos que forman la
            # tarjeta: el fondo, el nombre y el crimen. Así el
            # clic funciona sin importar en qué parte se haga.
            for element_id in (
                panel_id,
                txt_name_id,
                txt_crime_id
            ):

                # Al hacer clic izquierdo (<Button-1>) sobre ese
                # elemento, se selecciona el objetivo.
                #
                # "lambda e, t=target: ..." fija el objetivo de
                # esta vuelta con un valor por defecto. Sin el
                # "t=target", todas las tarjetas acabarían
                # usando el ÚLTIMO objetivo del bucle, porque la
                # lambda leería "target" cuando ya cambió.
                self.canvas_list.tag_bind(
                    element_id,
                    "<Button-1>",
                    lambda e, t=target: registrar_click(t)
                )


        # =====================================================
        # REGIÓN DE SCROLL
        # =====================================================

        # Calculamos la altura total que ocupan todas las
        # tarjetas: margen inicial + (tarjetas x su espacio)
        # + 20 píxeles extra al final.
        total_height = (
            start_y
            + len(self.targets) * (card_height + spacing)
            + 20
        )

        # scrollregion es el área total por la que se puede
        # desplazar el Canvas: (x_min, y_min, x_max, y_max).
        # Si es más alta que el Canvas visible, se puede hacer
        # scroll con la rueda.
        self.canvas_list.configure(
            scrollregion=(
                0,              # X mínima.
                0,              # Y mínima.
                400,            # X máxima (ancho).
                total_height    # Y máxima (alto calculado).
            )
        )


    # ========================================================
    # SELECCIONAR UN OBJETIVO
    # ========================================================

    # Se ejecuta al hacer clic en una tarjeta. Recibe el
    # diccionario del objetivo elegido.
    def seleccionar_target(self, target):
        """
        Selecciona un objetivo de la lista y coloca sus datos
        dentro del formulario.
        """

        # Recordamos cuál es el objetivo seleccionado guardando
        # su ID. Los métodos de actualizar y borrar lo usan.
        self.selected_target_id = target["id"]


        # ====================================================
        # RELLENAR CAMPO NOMBRE
        # ====================================================

        # delete(inicio, fin) borra texto del Entry.
        # 0 = primer carácter, tk.END = hasta el final.
        # Es decir, deja el campo vacío.
        self.entry_name.delete(
            0,
            tk.END
        )

        # insert(posición, texto) escribe texto en el Entry.
        # En la posición 0 (al inicio) ponemos el nombre.
        self.entry_name.insert(
            0,
            target["nombre"]
        )


        # ====================================================
        # RELLENAR CAMPO CRIMEN
        # ====================================================

        # Igual que arriba: primero vaciamos el campo...
        self.entry_crime.delete(
            0,
            tk.END
        )

        # ...y luego escribimos el crimen del objetivo.
        self.entry_crime.insert(
            0,
            target["crimen"]
        )


        # Redibujamos la lista para que la tarjeta elegida
        # se vea en amarillo.
        self.actualizar_lista_visual()


    # ========================================================
    # CREATE - CREAR
    # ========================================================

    def ejecutar_crear(self):
        """
        Crea un nuevo objetivo utilizando la información
        introducida en el formulario.
        """

        # .get() lee lo que hay escrito en el Entry.
        # .strip() elimina los espacios del principio y del
        # final (así "   " cuenta como vacío).
        nombre = self.entry_name.get().strip()

        # Leemos y limpiamos también el crimen.
        crimen = self.entry_crime.get().strip()


        # ====================================================
        # VALIDACIÓN
        # ====================================================

        # Una cadena vacía es "falsa" en Python, por eso
        # "not nombre" es verdadero cuando está vacía.
        # Si el nombre O el crimen están vacíos...
        if not nombre or not crimen:

            # ...mostramos una ventana emergente de advertencia:
            # primero el título, después el mensaje.
            messagebox.showwarning(
                "ALERT",
                "¡No puedes dejar campos vacíos, Ladrón Fantasma!"
            )

            # return termina la función aquí: no se crea nada.
            return


        # ====================================================
        # CREAR NUEVO REGISTRO
        # ====================================================

        # append() añade un elemento al final de la lista.
        # Aquí añadimos un diccionario nuevo con el ID
        # disponible y los datos del formulario.
        self.targets.append({
            "id": self.next_id,
            "nombre": nombre,
            "crimen": crimen
        })

        # Subimos el contador (+= 1 significa "suma 1") para
        # que el próximo objetivo tenga un ID distinto.
        self.next_id += 1

        # Vaciamos el formulario. Ese método también
        # redibuja la lista, así que el nuevo objetivo aparece.
        self.limpiar_formulario()


    # ========================================================
    # UPDATE - ACTUALIZAR
    # ========================================================

    def ejecutar_actualizar(self):
        """
        Modifica un objetivo existente.
        """

        # Si no hay ningún objetivo seleccionado, no hay nada
        # que actualizar.
        if self.selected_target_id is None:

            # Avisamos al usuario con una ventana.
            messagebox.showwarning(
                "ALERT",
                "Selecciona primero un objetivo de la lista."
            )

            # Salimos de la función.
            return

        # Leemos los nuevos datos escritos en el formulario.
        nombre = self.entry_name.get().strip()

        crimen = self.entry_crime.get().strip()

        # Comprobamos que ninguno esté vacío.
        if not nombre or not crimen:

            messagebox.showwarning(
                "ALERT",
                "Los campos modificados no pueden estar vacíos."
            )

            # Salimos sin modificar nada.
            return


        # ====================================================
        # BUSCAR EL OBJETIVO
        # ====================================================

        # Recorremos la lista buscando el objetivo cuyo ID
        # coincida con el seleccionado.
        for target in self.targets:

            # "==" compara igualdad (un solo "=" asignaría).
            if target["id"] == self.selected_target_id:

                # Lo encontramos: reemplazamos su nombre...
                target["nombre"] = nombre

                # ...y su crimen.
                target["crimen"] = crimen

                # break termina el bucle: ya no hace falta seguir
                # buscando porque los IDs son únicos.
                break

        # Vaciamos el formulario y redibujamos la lista con los
        # datos ya modificados.
        self.limpiar_formulario()


    # ========================================================
    # DELETE - ELIMINAR
    # ========================================================

    def ejecutar_borrar(self):
        """
        Elimina el objetivo actualmente seleccionado.
        """

        # Sin objetivo seleccionado no hay nada que borrar.
        if self.selected_target_id is None:

            messagebox.showwarning(
                "ALERT",
                "Selecciona el objetivo que deseas eliminar."
            )

            return


        # ====================================================
        # ELIMINAR OBJETIVO
        # ====================================================

        # Construimos una lista nueva con una "list
        # comprehension":
        #
        # [t for t in self.targets if t["id"] != self.selected_target_id]
        #
        # Se lee así: "para cada t en self.targets, quédate con
        # t solo si su ID es DISTINTO (!=) al seleccionado".
        # El objetivo seleccionado se queda fuera y desaparece.
        self.targets = [
            t                                  # Qué se guarda.
            for t in self.targets              # De dónde sale.
            if t["id"] != self.selected_target_id  # Condición.
        ]

        # Vaciamos el formulario y redibujamos la lista.
        self.limpiar_formulario()


    # ========================================================
    # LIMPIAR FORMULARIO
    # ========================================================

    def limpiar_formulario(self):
        """
        Deselecciona cualquier objetivo y limpia los campos
        del formulario.
        """

        # Ya no hay ningún objetivo seleccionado.
        self.selected_target_id = None

        # Vaciamos el campo del nombre (del carácter 0 al final).
        self.entry_name.delete(
            0,
            tk.END
        )

        # Vaciamos el campo del crimen.
        self.entry_crime.delete(
            0,
            tk.END
        )

        # Redibujamos la lista para reflejar los cambios
        # (nuevos, modificados, borrados o sin selección).
        self.actualizar_lista_visual()


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

# __name__ es una variable especial que Python crea solo.
# Si ejecutas este archivo directamente (python archivo.py),
# vale "__main__". Si otro archivo lo importa, vale otra cosa.
# Esta condición significa: "haz lo siguiente solo si este
# archivo se ejecuta directamente".
if __name__ == "__main__":

    # Creamos la ventana principal de Tkinter.
    root = tk.Tk()

    # Creamos la aplicación (un objeto de nuestra clase) y le
    # pasamos la ventana. Esto ejecuta __init__ y dibuja todo.
    app = Persona5CRUDScroll(root)

    # mainloop() arranca el bucle de eventos: mantiene la
    # ventana abierta y queda escuchando clics, teclas, rueda
    # del ratón, etc. El programa termina al cerrar la ventana.
    # Sin esta línea, la ventana se cerraría al instante.
    root.mainloop()