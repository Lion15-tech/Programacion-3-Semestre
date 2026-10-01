import tkinter as tk
from tkinter import messagebox


class Menu:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Graficas y Ecuaciones")
        self.ventana.geometry("400x450")
        self.ventana.configure(bg="#000000")
        #Para que el usuario no pueda cambiar el tamaño de la ventana
        self.ventana.resizable(False, False) 

        #### Esto le dará la estetica de Persona 5 ####
        self.canvas_main = tk.Canvas(
            ventana,               
            width=400,              
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
'''
        ## Botones ##
        self.crear_boton_canvas(
                    "ecu. primer grado",
                    50,
                    320,
                    "> Gráfica de una ecuación\nde primer grado",
                    self.ejecutar_crear
                )

    ## Método de la clase para crear los botones a base de texto ##
    def crear_boton_canvas(self, tag_base, x, y, texto, comando):
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
        self.canvas_main.tag_bind(
            text_id,
            "<Enter>",
            lambda e: self.canvas_main.itemconfig(
                text_id,
                fill="#FFF200"   # Amarillo (efecto "hover").
            )
        )
        self.canvas_main.tag_bind(
            text_id,
            "<Leave>",
            lambda e: self.canvas_main.itemconfig(
                text_id,
                fill="#FFFFFF"   # Vuelve al blanco original.
            )
        )
        self.canvas_main.tag_bind(
                    text_id,
                    "<Button-1>",
                    lambda e: comando()
                )

'''

### Ejecutar la aplicación ###
if __name__ == "__main__":
    raiz = tk.Tk()
    app = Menu(raiz)
    raiz.mainloop()