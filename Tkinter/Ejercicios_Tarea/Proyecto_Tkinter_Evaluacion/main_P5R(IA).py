import tkinter as tk
from tkinter import messagebox
import preguntas

# ============================================================
# PALETA DE COLORES "PERSONA 5 ROYAL"
# ============================================================
# Guardamos los colores en variables para no repetir el mismo
# código hexadecimal por todo el archivo y para poder cambiar
# el estilo completo desde un solo lugar si hace falta.

COLOR_FONDO   = "#000000"     # Negro: fondo general de las ventanas.
COLOR_ROJO    = "#DC0000"     # Rojo característico de P5R.
COLOR_BLANCO  = "#FFFFFF"     # Blanco: texto principal, franjas.
COLOR_AMARILLO = "#FFF200"    # Amarillo: acentos, texto al pasar
                                # el mouse por encima (hover).
COLOR_GRIS    = "#666666"     # Gris: texto secundario / pistas.

FUENTE_TITULO  = ("Impact", 30)          # Fuente grande de título.
FUENTE_SUB     = ("Impact", 14)          # Subtítulos / botones.
FUENTE_TEXTO   = ("Arial", 11, "bold")   # Texto normal (preguntas).
FUENTE_ENTRY   = ("Arial", 12, "bold")   # Texto dentro de los Entry.


# ============================================================
# FUNCIÓN AUXILIAR: FONDO CON EL ESTILO DE PERSONA 5
# ============================================================

def dibujar_fondo_p5r(canvas, ancho, alto, titulo, subtitulo=""):
    """
    Dibuja, sobre el Canvas recibido, las franjas diagonales
    rojas/blancas típicas de Persona 5 Royal y, encima, un
    título (y opcionalmente un subtítulo).

    Recibimos el Canvas ya creado (en vez de crearlo aquí)
    porque cada ventana necesita el suyo propio, pero todas
    quieren el mismo estilo de fondo: así evitamos copiar y
    pegar el mismo dibujo en cada ventana.
    """

    # Franja diagonal roja grande, del lado izquierdo.
    # create_polygon(x1,y1, x2,y2, ...) une los puntos en el
    # orden en que se dan y rellena la figura resultante.
    canvas.create_polygon(
        0, 0,
        ancho * 0.65, 0,
        ancho * 0.45, alto,
        0, alto,
        fill=COLOR_ROJO
    )

    # Franja blanca delgada que separa el rojo del fondo negro,
    # dando el efecto de "corte" diagonal.
    canvas.create_polygon(
        ancho * 0.64, 0,
        ancho * 0.67, 0,
        ancho * 0.47, alto,
        ancho * 0.44, alto,
        fill=COLOR_BLANCO
    )

    # Triángulo rojo pequeño en la esquina inferior derecha,
    # para que el fondo no se vea vacío de ese lado.
    canvas.create_polygon(
        ancho, alto * 0.85,
        ancho, alto,
        ancho * 0.8, alto,
        fill=COLOR_ROJO
    )

    # Título principal, en la esquina superior izquierda, con
    # una leve inclinación (angle) para dar dinamismo.
    canvas.create_text(
        20,
        20,
        text=titulo,
        fill=COLOR_BLANCO,
        font=FUENTE_TITULO,
        angle=4,
        anchor="nw"
    )

    # El subtítulo es opcional: solo lo dibujamos si se recibió
    # un texto distinto de cadena vacía.
    if subtitulo:
        canvas.create_text(
            23,
            58,
            text=subtitulo,
            fill=COLOR_AMARILLO,
            font=("Impact", 12),
            angle=3,
            anchor="nw"
        )


# ============================================================
# FUNCIÓN AUXILIAR: "BOTÓN" ESTILO PERSONA 5 SOBRE UN CANVAS
# ============================================================

def crear_boton_p5r(canvas, x, y, texto, comando):
    """
    Dibuja un texto en el Canvas que se comporta como un botón:
    cambia de color cuando el mouse pasa por encima y ejecuta
    'comando' cuando se hace clic.

    No usamos tk.Button para mantener el look "texto sobre
    fondo negro" característico del juego, igual que se hizo
    en la base de datos de objetivos (Prueba_P5R.py).
    """

    # Dibujamos el texto del botón y guardamos su ID: lo
    # necesitamos para poder cambiarle el color después.
    texto_id = canvas.create_text(
        x,
        y,
        text=f"> {texto}",
        fill=COLOR_BLANCO,
        font=FUENTE_SUB,
        anchor="w"
    )

    # Cuando el mouse entra en el texto, lo pintamos de amarillo.
    canvas.tag_bind(
        texto_id,
        "<Enter>",
        lambda e: canvas.itemconfig(texto_id, fill=COLOR_AMARILLO)
    )

    # Cuando el mouse sale, lo devolvemos a blanco.
    canvas.tag_bind(
        texto_id,
        "<Leave>",
        lambda e: canvas.itemconfig(texto_id, fill=COLOR_BLANCO)
    )

    # Con el clic izquierdo, ejecutamos la función recibida.
    canvas.tag_bind(
        texto_id,
        "<Button-1>",
        lambda e: comando()
    )

    # Devolvemos el ID por si quien llama a esta función quiere
    # hacer algo más con el botón (aquí no se usa, pero es una
    # buena práctica dejarlo disponible).
    return texto_id


# ============================================================
# LÓGICA DEL PROGRAMA
# ============================================================
# A partir de aquí, la lógica es la misma que tenía tu archivo
# original: seguimos usando el diccionario preguntas.alumnos_resultados
# y la lista preguntas.preguntas_evaluacion definidos en preguntas.py.
# Lo único que cambia es la apariencia (colores, fuentes, Canvas).

def iniciar_evaluacion():
    """
    Se ejecuta al presionar el botón "Continuar" de la ventana
    de registro. Valida el nombre y abre la ventana de examen.
    """

    # .get() obtiene lo escrito en el campo de texto.
    nombre = entrada_nombre.get()

    # Validar que no se dejen campos vacíos.
    # .strip() quita espacios sueltos, así " " también
    # cuenta como vacío.
    if nombre.strip() == "":
        messagebox.showwarning("Cuidado", "Debes ingresar tu nombre para continuar")
        return

    # Guardar el nombre en el diccionario y dejar la
    # calificación en 0 por ahora (se actualizará al terminar).
    preguntas.alumnos_resultados[nombre] = 0

    # Ocultar la ventana de registro (no la cerramos, solo se
    # esconde; withdraw() permite volver a mostrarla luego con
    # deiconify() sin perder lo que tenía dentro).
    ventana_registro.withdraw()

    # Llamar a la siguiente ventana, pasándole el nombre.
    abrir_ventana_evaluacion(nombre)


def abrir_ventana_evaluacion(nombre):
    """
    Crea y muestra la ventana del examen para el alumno
    indicado, con todas sus preguntas y opciones.
    """

    # Toplevel crea una ventana secundaria, distinta de la
    # ventana principal, pero que sigue perteneciendo al mismo
    # programa (por eso recibe 'ventana_registro' como padre).
    ventana_evaluacion = tk.Toplevel(ventana_registro)
    ventana_evaluacion.title("Evaluación de Python")
    ventana_evaluacion.geometry("420x750")

    # Fondo negro para toda la ventana (detrás del Canvas
    # puede asomar un borde si la ventana se redimensiona).
    ventana_evaluacion.configure(bg=COLOR_FONDO)

    # Si cierran esta ventana desde la 'X', cerramos todo el
    # programa: protocol() intercepta ese evento de cierre y,
    # en vez de dejar que solo esta ventana se cierre, llama a
    # ventana_registro.destroy(), que termina el programa entero.
    ventana_evaluacion.protocol("WM_DELETE_WINDOW", ventana_registro.destroy)


    # ========================================================
    # CANVAS DE FONDO (ENCABEZADO CON EL ESTILO P5R)
    # ========================================================

    # Un Canvas fijo arriba con las franjas rojas y el título.
    # No ocupa toda la ventana porque abajo necesitamos una
    # zona con scroll para las preguntas (ver más abajo).
    canvas_encabezado = tk.Canvas(
        ventana_evaluacion,
        width=420,
        height=110,
        bg=COLOR_FONDO,
        highlightthickness=0
    )
    canvas_encabezado.pack(fill="x")

    # Usamos la función auxiliar para pintar el fondo con el
    # nombre del alumno como subtítulo.
    dibujar_fondo_p5r(
        canvas_encabezado,
        420,
        110,
        "EXAM RAID",
        f"Evaluando a: {nombre}"
    )


    # ========================================================
    # ZONA CON SCROLL PARA LAS PREGUNTAS
    # ========================================================
    # Como el número de preguntas puede ser grande, ponemos un
    # Canvas con scrollbar para que todas quepan aunque no
    # entren en la pantalla de una vez.

    # Frame contenedor del Canvas con scroll y su barra.
    contenedor = tk.Frame(ventana_evaluacion, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True)

    # Canvas donde en realidad se dibujan/colocan las preguntas.
    canvas_preguntas = tk.Canvas(
        contenedor,
        bg=COLOR_FONDO,
        highlightthickness=0
    )
    canvas_preguntas.pack(side="left", fill="both", expand=True)

    # Barra de scroll vertical, ligada al Canvas de preguntas.
    scrollbar = tk.Scrollbar(
        contenedor,
        orient="vertical",
        command=canvas_preguntas.yview
    )
    scrollbar.pack(side="right", fill="y")

    # Conectamos el Canvas con la Scrollbar en ambos sentidos:
    # cuando el Canvas se desplaza, la barra debe moverse, y
    # viceversa. yscrollcommand hace la primera parte.
    canvas_preguntas.configure(yscrollcommand=scrollbar.set)

    # Dentro del Canvas metemos un Frame: es más fácil colocar
    # Labels y Radiobuttons en un Frame normal (con pack) que
    # dibujarlos directamente en el Canvas.
    frame_preguntas = tk.Frame(canvas_preguntas, bg=COLOR_FONDO)

    # create_window mete ese Frame dentro del Canvas para que
    # el Canvas pueda desplazarlo como si fuera una imagen.
    canvas_preguntas.create_window(
        (0, 0),
        window=frame_preguntas,
        anchor="nw"
    )

    # Permitimos hacer scroll con la rueda del mouse (Windows/
    # macOS mandan <MouseWheel>; delta positivo = hacia arriba).
    def on_mouse_wheel(event):
        canvas_preguntas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas_preguntas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Cada vez que el contenido del Frame cambia de tamaño,
    # actualizamos la scrollregion para que el scroll cubra
    # exactamente el alto real de las preguntas.
    def actualizar_scrollregion(event):
        canvas_preguntas.configure(
            scrollregion=canvas_preguntas.bbox("all")
        )

    frame_preguntas.bind("<Configure>", actualizar_scrollregion)


    # ========================================================
    # LISTA PARA GUARDAR LAS RESPUESTAS SELECCIONADAS
    # ========================================================

    # Aquí guardaremos una variable de Tkinter por cada
    # pregunta, para poder leer después qué opción se marcó.
    variables_respuestas = []

    # Recorremos la lista de preguntas para mostrarlas en
    # pantalla. enumerate() nos da el índice (pregunta) y el
    # diccionario de esa pregunta (respuesta) en cada vuelta.
    for pregunta, respuesta in enumerate(preguntas.preguntas_evaluacion):

        # Texto de la pregunta, en blanco y con la fuente P5R.
        tk.Label(
            frame_preguntas,
            text=f"{pregunta + 1}. {respuesta['pregunta']}",
            bg=COLOR_FONDO,
            fg=COLOR_AMARILLO,
            font=FUENTE_TEXTO,
            wraplength=380,     # Corta el texto largo en varias
                                # líneas en vez de salirse de la
                                # ventana.
            justify="left"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # Variable de Tkinter que va a rastrear cuál opción
        # eligió el usuario para ESTA pregunta. Empieza vacía
        # ("" = ninguna opción marcada todavía).
        var_respuesta = tk.StringVar(value="")
        variables_respuestas.append(var_respuesta)

        # Mostramos cada opción como un Radiobutton. Todos los
        # de una misma pregunta comparten "variable=var_respuesta",
        # así que marcar uno desmarca automáticamente los demás.
        for opcion in respuesta["opciones"]:
            tk.Radiobutton(
                frame_preguntas,
                text=opcion,
                variable=var_respuesta,
                value=opcion,
                bg=COLOR_FONDO,          # Fondo negro, igual que
                                          # el resto de la ventana.
                fg=COLOR_BLANCO,         # Texto de la opción.
                selectcolor=COLOR_ROJO,  # Color del círculo
                                          # cuando está marcado.
                activebackground=COLOR_FONDO,  # Fondo al hacer
                                                # clic (se queda
                                                # negro, no gris).
                activeforeground=COLOR_AMARILLO,  # Texto al
                                                    # hacer clic.
                highlightthickness=0,
                font=("Arial", 10)
            ).pack(anchor="w", padx=40)


    # ========================================================
    # FUNCIÓN: CALIFICAR Y ENVIAR RESPUESTAS
    # ========================================================

    def enviar_respuestas():
        """
        Revisa que todas las preguntas estén contestadas,
        calcula el porcentaje de aciertos, lo guarda y pregunta
        si se desea evaluar a otro alumno.
        """

        # Revisamos si alguna variable sigue en blanco, es
        # decir, si el usuario dejó alguna pregunta sin marcar.
        for var in variables_respuestas:
            if var.get() == "":
                messagebox.showwarning(
                    "Incompleto",
                    "No puedes terminar sin contestar todas las preguntas."
                )
                return

        # Calculamos los aciertos comparando cada respuesta
        # marcada con la respuesta correcta guardada en
        # preguntas.py.
        aciertos = 0
        total = len(preguntas.preguntas_evaluacion)

        for i, var in enumerate(variables_respuestas):
            respuesta_usuario = var.get()
            respuesta_correcta = preguntas.preguntas_evaluacion[i]["respuesta"]
            if respuesta_usuario == respuesta_correcta:
                aciertos += 1

        # Calculamos el promedio en base a 100.
        promedio = (aciertos / total) * 100

        # Guardamos el resultado final en el diccionario,
        # reemplazando el 0 inicial.
        preguntas.alumnos_resultados[nombre] = promedio

        # Armamos el texto que se mostrará en el mensaje final.
        texto_resultado = (
            f"Obtuviste {aciertos} de {total} aciertos.\n"
            f"Tu promedio es: {promedio}\n\n"
            f"Diccionario actual:\n{preguntas.alumnos_resultados}"
        )

        # askyesno muestra un mensaje con botones "Sí"/"No" y
        # devuelve True o False según lo que elija el usuario.
        otro_alumno = messagebox.askyesno(
            "Evaluación Terminada",
            f"{texto_resultado}\n\n¿Deseas evaluar a otro alumno?"
        )

        if otro_alumno:
            # Cerramos la ventana de evaluación, limpiamos la
            # caja de texto del nombre y volvemos a mostrar el
            # registro (deiconify es lo opuesto de withdraw).
            ventana_evaluacion.destroy()
            entrada_nombre.delete(0, tk.END)
            ventana_registro.deiconify()
        else:
            # Terminamos el programa cerrando la ventana
            # principal (esto también cierra todo lo demás).
            ventana_registro.destroy()


    # ========================================================
    # PIE DE VENTANA CON EL BOTÓN DE ENVIAR
    # ========================================================

    # Franja negra al fondo de la ventana donde va el botón
    # de "Terminar Evaluación", con estilo de botón P5R.
    canvas_pie = tk.Canvas(
        ventana_evaluacion,
        width=420,
        height=60,
        bg=COLOR_FONDO,
        highlightthickness=0
    )
    canvas_pie.pack(fill="x")

    # Pequeña línea roja decorativa encima del botón.
    canvas_pie.create_line(
        0, 0, 420, 0,
        fill=COLOR_ROJO,
        width=3
    )

    # Botón (texto clicable) para enviar las respuestas.
    crear_boton_p5r(
        canvas_pie,
        150,
        30,
        "TERMINAR EVALUACIÓN",
        enviar_respuestas
    )


# ============================================================
# VENTANA DE REGISTRO (PANTALLA INICIAL)
# ============================================================

# Configuración básica de la ventana de registro.
ventana_registro = tk.Tk()
ventana_registro.title("Registro")
ventana_registro.geometry("340x260")
ventana_registro.configure(bg=COLOR_FONDO)

# Canvas que cubre toda la ventana de registro: aquí dibujamos
# el fondo con las franjas rojas y colocamos encima el campo
# de texto y el botón.
canvas_registro = tk.Canvas(
    ventana_registro,
    width=340,
    height=260,
    bg=COLOR_FONDO,
    highlightthickness=0
)
canvas_registro.pack(fill="both", expand=True)

# Dibujamos el fondo típico de Persona 5 con el título del
# programa.
dibujar_fondo_p5r(
    canvas_registro,
    340,
    260,
    "PYTHON EXAM",
    "REGISTRO DE ALUMNO"
)

# Etiqueta que indica qué escribir en el campo de texto.
canvas_registro.create_text(
    20,
    140,
    text="Ingresa tu nombre:",
    fill=COLOR_BLANCO,
    font=("Impact", 14),
    anchor="w"
)

# Campo de texto donde el alumno escribe su nombre. Se crea
# como Entry normal y luego se "incrusta" en el Canvas con
# create_window, igual que se hizo en Prueba_P5R.py.
entrada_nombre = tk.Entry(
    ventana_registro,
    font=FUENTE_ENTRY,
    bg=COLOR_BLANCO,
    fg="#000000",
    bd=2,
    relief="solid"
)

canvas_registro.create_window(
    20,
    175,
    window=entrada_nombre,
    anchor="nw",
    width=290,
    height=30
)

# Botón para continuar hacia la evaluación, con el mismo
# estilo "texto que cambia de color" que el resto del programa.
crear_boton_p5r(
    canvas_registro,
    20,
    225,
    "CONTINUAR",
    iniciar_evaluacion
)

# Mantener la ventana abierta: inicia el bucle de eventos y
# escucha clics, teclas, etc. hasta que se cierre la ventana.
ventana_registro.mainloop()