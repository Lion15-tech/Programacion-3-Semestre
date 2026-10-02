import tkinter as tk
from tkinter import messagebox


class Menu:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Graficas y Ecuaciones")
        self.ventana.geometry("450x450")
        self.ventana.configure(bg="#000000")
        #Para que el usuario no pueda cambiar el tamaño de la ventana
        self.ventana.resizable(False, False) 

        #### Esto le dará la estetica de Persona 5 ####
        self.canvas_main = tk.Canvas(
            ventana,               
            width=450,              
            height=450,             
            bg="#000000",
            highlightthickness=0
            )
        self.canvas_main.pack(
            fill="both",   #Se estira en horizontal y vertical.
            expand=True    #Aprovecha todo el espacio libre.
        )

        #El create_polygon se usa poniendo puntos en donde quieres que vaya la linea
        #Es como esos dibujos de unir lineas que haciamos de chiquitos
        self.canvas_main.create_polygon( ## Figura roja mitad pantalla ##
                    0, 0,        # Punto 1: esquina superior izquierda.
                    100, 0,      # Punto 2: arriba, en X = 100 y Y = 0.
                    250, 350,    # Punto 3: en X se va a mover hacia la derecha y en Y bajará
                    120, 450,
                    0, 450,      
                    fill="#DC0000"  # Color de relleno: rojo.
                )
        self.canvas_main.create_polygon( ## Linea blanca divisoria ##
                    100, 0,      
                    115, 0,     
                    265, 350,
                    140, 450,
                    115, 450,
                    245, 345,
                    fill="#FFFFFF"  # Blanco.
                )
        self.canvas_main.create_polygon( ## Triangulo negro en lo rojo ##
                    0, 300,      
                    50, 450,    
                    0, 450,      
                    fill="#000000"  # Negro.
                )
        self.canvas_main.create_polygon( ## Triangulo rojo en lo negro ##
            250, 0,      
            450, 0,      
            450, 50,   
            fill="#DC0000"  # Rojo.
        )
        ## Titulo ##
        self.canvas_main.create_text(
                    40,   # Posición X.
                    250,   # Posición Y.
                    text="Gráficas y \nEcuaciones",  
                    fill="#FFFFFF",         
                    font=("Impact", 26),     
                    angle=-6,                 
                    anchor="nw"               
                )

        ## Botones ##
        self.crear_boton_canvas(
                    "ecu. primer grado",
                    160,
                    50,
                    "> Gráfica de una ecuación\n    de primer grado",
                    nueva_ventana
                )
        self.crear_boton_canvas(
                    "ecu. segundo grado",
                    190,
                    120,
                    "> Gráfica de una ecuación\n    de segundo grado",
                    nueva_ventana
                )
        self.crear_boton_canvas(
                    "ecu. tercer grado",
                    220,
                    190,
                    "> Sistema de\n    ecuaciones",
                    nueva_ventana
                )
        self.crear_boton_canvas(
            "boton salir",
            300,
            400,
            "> SALIR",
            lambda: None
        )

    ## Método de la clase para crear los botones a base de texto ##
    def crear_boton_canvas(self, tag_base, x, y, texto, comando):
        ## Esto crea el texto que tendrá el botón
        ## AL crear el texto se le asigna un id que guardamos
        text_id = self.canvas_main.create_text( x,                   # Posición X recibida.
                                                y,                   # Posición Y recibida.
                                                text=texto,          # Texto recibido.
                                                fill="#FFFFFF",      # Color inicial: blanco.
                                                font=("Impact", 15), # Fuente y tamaño.
                                                angle=4,             # Ligera inclinación.
                                                anchor="nw",         # Ancla: esquina sup. izq.
                                                tags=tag_base        # Etiqueta para identificarlo.
                                            )
        ## el tag_bind() sirve para decirle que vigile en el canvas_main 
        # al texto con el texto_id y revise si ocurre un evento, para después 
        # realizar una acción
        self.canvas_main.tag_bind( #TE PIDE: que vigilo, que condicion vigilo y que hago si sucede
            text_id,
            "<Enter>",             # Esto detecta cuando el mouse toca el texto
            ### El lambda sirve como "reemplazo" de crear una función completa para 
            # solo cambiar el color, tipo:              def función(e):
            lambda e: self.entrar_estilo_cursor_texto(text_id)
        )
        self.canvas_main.tag_bind(
            text_id,
            "<Leave>",               # El itemconfig sirve para del objeto con el text_id 
            lambda e: self.desactivar_efecto_boton(text_id)
        )
        self.canvas_main.tag_bind(
                    text_id,
                    "<Button-1>",
                    lambda e: comando()
                )

    def entrar_estilo_cursor_texto(self, text_id):
        ## Esto crea los 2 trapecios que se ponen detras del texto
        ## Así como cuando seleccionas el texto en Persona 5
        self.canvas_main.itemconfig(
                    text_id,
                    fill="#000000",   # Negro (efecto "hover").
                    font=("Impact", 16), # Más grande la letra 
                    )
        x1, y1, x2, y2 = self.canvas_main.bbox(text_id)

        tag_fondo = f"fondo_{text_id}"

        margen_celeste = 4
        poligono1_id = self.canvas_main.create_polygon(
                                x1 - margen_celeste,      y1 - margen_celeste - 3,
                                x2 + margen_celeste + 20, y1 - margen_celeste - 3,
                                x2 + margen_celeste,      y2 + margen_celeste - 3,
                                x1 - margen_celeste - 20, y2 + margen_celeste - 3,
                                fill="#00CCFF",
                                tag=tag_fondo
                            )
        poligono2_id = self.canvas_main.create_polygon(
                                x1 - 15, y1,
                                x2,      y1,
                                x2 + 15, y2,
                                x1,      y2,
                                fill="#FF0000",
                                tag=tag_fondo
                            )
        self.canvas_main.tag_lower(poligono1_id, text_id)
        self.canvas_main.tag_lower(poligono2_id, text_id)

    def desactivar_efecto_boton(self, text_id):
        self.canvas_main.itemconfig(
                    text_id,
                    fill="#FFFFFF",
                    font=("Impact", 15)
                    )
        tag_fondo = f"fondo_{text_id}"
        self.canvas_main.delete(tag_fondo)


def nueva_ventana():
    mensajito = tk.Toplevel()

### Ejecutar la aplicación ###
if __name__ == "__main__":
    raiz = tk.Tk()
    app = Menu(raiz)
    raiz.mainloop()