import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Menu:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Graficas y Ecuaciones")
        self.ventana.geometry("450x450")
        self.ventana.configure(bg="#000000")
        #Para que el usuario no pueda cambiar el tamaño de la ventana
        self.ventana.resizable(False, False) 


        #### CONFIGURACIÓN DEL ICONO ####
        self.carpeta_proyecto = os.path.dirname(__file__)
        self.ruta_icono = os.path.join(self.carpeta_proyecto, "logo_cecyteq.png")

        try:
            self.icono = tk.PhotoImage(file=self.ruta_icono)
            self.ventana.iconphoto(False, self.icono)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        #### Esto permitirá la estetica de Persona 5 ####
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
                    "ecu._primer_grado",
                    160,
                    50,
                    "> Gráfica de una ecuación\n    de primer grado",
                    self.ventana_primer_grado
                )
        self.crear_boton_canvas(
                    "ecu._segundo_grado",
                    190,
                    120,
                    "> Gráfica de una ecuación\n    de segundo grado",
                    self.ventana_segundo_grado
                )
        self.crear_boton_canvas(
                    "ecu._tercer_grado",
                    220,
                    190,
                    "> Sistema de\n    ecuaciones",
                    self.ventana_sistemas_ecuaciones
                )
        self.crear_boton_canvas(
            "boton_salir",
            300,
            400,
            "> SALIR",
            self.cerrar_app
        )
    
    def cerrar_app(self):
        self.ventana.after(10, self.ventana.destroy)



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
            tag_base,
            "<Enter>",             # Esto detecta cuando el mouse toca el texto
            ### El lambda sirve como "reemplazo" de crear una función completa para 
            # solo cambiar el color, tipo:              def función(e):
            lambda e: self.entrar_estilo_cursor_texto(text_id)
        )
        self.canvas_main.tag_bind(
            tag_base,
            "<Leave>",               # El itemconfig sirve para del objeto con el text_id 
            lambda e: self.desactivar_efecto_boton(text_id)
        )
        self.canvas_main.tag_bind(
                    tag_base,
                    "<Button-1>",
                    lambda e: comando()
                )

    def entrar_estilo_cursor_texto(self, text_id):
        ## Esto crea los 2 trapecios que se ponen detras del texto
        ## Así como cuando seleccionas el texto en Persona 5
        self.canvas_main.itemconfig(
                    text_id,
                    fill="#FFFFFF",   # Negro (efecto "hover").
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
        # Revisamos si la ventana todavía existe
        if self.canvas_main.winfo_exists():
            self.canvas_main.itemconfig(
                        text_id,
                        fill="#FFFFFF",
                        font=("Impact", 15)
                        )
            tag_fondo = f"fondo_{text_id}"
            self.canvas_main.delete(tag_fondo)



    #### ---------------------------------- ####
    ####            Gráficas                ####
    #### ---------------------------------- ####
    def ventana_primer_grado(self):
        new_ventana = tk.Toplevel()
        new_ventana.title("Gráfica Ecuación Primer Grado")
        new_ventana.geometry("600x400")
        new_ventana.resizable(False, False)
        if hasattr(self, 'icono'):
            new_ventana.iconphoto(False, self.icono)

        canvas = tk.Canvas(new_ventana, 
                        width=600, 
                        height=400, 
                        bg="#000000",
                        highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Mitad izquierda: Dibujo en Canvas
        canvas.create_polygon(
                    300, 50,
                    120, 350,
                    260, 400,
                    300, 400,
                    fill="#DC0000")
        canvas.create_polygon( ## Linea blanca divisoria ##
                    300, 50,      
                    110, 350,     
                    240, 400,
                    270, 400,
                    130, 345,
                    300, 70,
                    fill="#FFFFFF"  # Blanco.
                )
        canvas.create_polygon(
                    0, 0,
                    150, 0,
                    0, 60,
                    fill="#DC0000")
        
        canvas.create_text(
                            140, 15, 
                            text="Ecuación de\n1er Grado", 
                            fill="#FFFFFF", 
                            font=("Impact", 17), 
                            anchor="nw",
                            angle=-4)
        canvas.create_text(
                                    10, 100, 
                                    text="Par ordenado 1:", 
                                    fill="#FFFFFF", 
                                    font=("Impact", 14), 
                                    anchor="nw",
                                    angle=4)
        canvas.create_text(
                                    10, 170, 
                                    text="Par orenado 2:", 
                                    fill="#FFFFFF", 
                                    font=("Impact", 14), 
                                    anchor="nw",
                                    angle=-4)

        # Mitad derecha: Frame incrustado
        self.frame_1ro = tk.Frame(canvas, 
                                bg="#FFFFFF", 
                                padx=15, 
                                pady=15)
        self.frame_1ro.pack_propagate(False)
        canvas.create_window(270, 0, 
                            window=self.frame_1ro, 
                            anchor="nw", 
                            width=330, 
                            height=400)


    def ventana_segundo_grado(self):
        new_ventana = tk.Toplevel()
        new_ventana.title("Gráfica Ecuación Segundo Grado")
        new_ventana.geometry("600x400")
        new_ventana.resizable(False, False)
        if hasattr(self, 'icono'):
            new_ventana.iconphoto(False, self.icono)

        canvas = tk.Canvas(new_ventana, 
                        width=600, 
                        height=400, 
                        bg="#000000",
                        highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Mitad izquierda: Dibujo en Canvas
        canvas.create_polygon(
                    300, 50,
                    120, 350,
                    260, 400,
                    300, 400,
                    fill="#DC0000")
        canvas.create_polygon( ## Linea blanca divisoria ##
                    300, 50,      
                    110, 350,     
                    240, 400,
                    270, 400,
                    130, 345,
                    300, 70,
                    fill="#FFFFFF"  # Blanco.
                )
        canvas.create_polygon(
                    0, 0,
                    150, 0,
                    0, 60,
                    fill="#DC0000")
        canvas.create_text(
                            20, 160, 
                            text="Ecuación de\n2do Grado", 
                            fill="#FFFFFF", 
                            font=("Impact", 22), 
                            anchor="nw")

        # Mitad derecha: Frame incrustado
        self.frame_2do = tk.Frame(canvas, 
                                bg="#FFFFFF", 
                                padx=15, 
                                pady=15)
        self.frame_2do.pack_propagate(False)
        canvas.create_window(270, 0, 
                            window=self.frame_2do, 
                            anchor="nw", 
                            width=330, 
                            height=400)

        
    def ventana_sistemas_ecuaciones(self):
        new_ventana = tk.Toplevel()
        new_ventana.title("Gráfica Ecuación Primer Grado")
        new_ventana.geometry("600x400")
        new_ventana.resizable(False, False)
        if hasattr(self, 'icono'):
            new_ventana.iconphoto(False, self.icono)

        canvas = tk.Canvas(new_ventana, 
                        width=600, 
                        height=400, 
                        bg="#000000",
                        highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Mitad izquierda: Dibujo en Canvas
        canvas.create_polygon(
                    300, 50,
                    120, 350,
                    260, 400,
                    300, 400,
                    fill="#DC0000")
        canvas.create_polygon( ## Linea blanca divisoria ##
                    300, 50,      
                    110, 350,     
                    240, 400,
                    270, 400,
                    130, 345,
                    300, 70,
                    fill="#FFFFFF"  # Blanco.
                )
        canvas.create_polygon(
                    0, 0,
                    150, 0,
                    0, 60,
                    fill="#DC0000")
        canvas.create_text(
                            20, 160, 
                            text="Sistemas de \necuaciones", 
                            fill="#FFFFFF", 
                            font=("Impact", 22), 
                            anchor="nw")

        # Mitad derecha: Frame incrustado
        self.frame_sistemas_ecuaciones = tk.Frame(canvas, 
                                bg="#FFFFFF", 
                                padx=15, 
                                pady=15)
        self.frame_sistemas_ecuaciones.pack_propagate(False)
        canvas.create_window(270, 0, 
                            window=self.frame_sistemas_ecuaciones, 
                            anchor="nw", 
                            width=330, 
                            height=400)



    def procesar_ecuacion_primer_grado(self):
        pass


    def procesar_ecuacion_primer_grado(self):
        pass


    def procesar_ecuacion_primer_grado(self):
        pass
    

### Ejecutar la aplicación ###
if __name__ == "__main__":
    raiz = tk.Tk()
    app = Menu(raiz)
    raiz.mainloop()