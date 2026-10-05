import tkinter as tk
from tkinter import messagebox
import os

### Fuentes ###
fuente_titulo = ("Impact", 20)

### Paleta de Colores (Estilo Verde Institucional) ###
COLOR_FONDO_PRINCIPAL = "#F4F9F4"  # Verde menta muy claro para el fondo
COLOR_FONDO_LATERAL   = "#E1EFE1"  # Verde claro pastel para resaltar el título lateral
COLOR_TEXTO_TITULO    = "#1E4620"  # Verde bosque oscuro para los títulos
COLOR_BOTON_NORMAL    = "#2E7D32"  # Verde estándar para los botones
COLOR_BOTON_HOVER     = "#1B5E20"  # Verde más oscuro cuando pasas el mouse
COLOR_TEXTO_BOTON     = "#FFFFFF"  # Texto blanco para que contraste con los botones



class MenuPrincipal:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gráficas y Ecuaciones - CECYTEQ")
        self.ventana.geometry("450x450")

        #### CONFIGURACIÓN DEL ICONO ####
        carpeta_proyecto = os.path.dirname(__file__)
        ruta_icono = os.path.join(carpeta_proyecto, "logo_cecyteq.png")

        try:
            self.icono = tk.PhotoImage(file=ruta_icono)
            self.ventana.iconphoto(False, self.icono)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")


        self.ventana.rowconfigure(0, weight=1)
        self.ventana.rowconfigure(1, weight=1)
        self.ventana.rowconfigure(2, weight=1)
        
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)
        
        tk.Label(self.ventana,
                text="Gráficas \ny \nEcuaciones", 
                font=fuente_titulo).grid(row=0, column=0, rowspan=3, padx=20, pady=10, sticky="w") 

        tk.Button(self.ventana,
                text="Gráfica una ecuación \nde primer grado",
                command=self.grafica_primer_grado).grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        tk.Button(self.ventana,
                text="Gráfica una ecuación \nde segundo grado",
                command=self.grafica_segundo_grado).grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        tk.Button(self.ventana,
                text="Sistemas de ecuaciones",
                command=self.ventana_sistema_ecuaciones).grid(row=2, column=1, padx=20, pady=10, sticky="ew")


    # Métodos para crear ventanas hijas con Toplevel
    def grafica_primer_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Primer Grado")
        ventana_hija.geometry("300x200")
        tk.Label(ventana_hija, text="Interfaz de Primer Grado aquí").pack(pady=50)

    def grafica_segundo_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Segundo Grado")
        ventana_hija.geometry("300x200")
        tk.Label(ventana_hija, text="Interfaz de Segundo Grado aquí").pack(pady=50)

    def ventana_sistema_ecuaciones(self):
        ventana_sistemas = tk.Toplevel(self.ventana)
        ventana_sistemas.title("Sistemas de Ecuaciones")
        ventana_sistemas.geometry("400x300")
        if hasattr(self, 'icono'): 
            ventana_sistemas.iconphoto(False, self.icono)

        tk.Label(ventana_sistemas, 
                text="Selecciona el Tipo de Sistema", 
                font=("Impact", 16)).pack(pady=20)
        tk.Button(ventana_sistemas,
                text="Sistemas de 2x2",
                font=("Arial", 11),
                command=self.sistema_2x2).pack(pady=15, fill="x", padx=40)
        tk.Button(ventana_sistemas,
                text="Sistemas de 3x3",
                font=("Arial", 11),
                command=self.sistema_3x3).pack(pady=15, fill="x", padx=40)
        
    def sistema_2x2(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 2x2")
        ventana_hija.geometry("300x200")
        tk.Label(ventana_hija, text="Interfaz de Sistema 2x2 aquí").pack(pady=50)

    def sistema_3x3(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 3x3")
        ventana_hija.geometry("300x200")
        tk.Label(ventana_hija, text="Interfaz de Sistema 3x3 aquí").pack(pady=50)



### Ejecutar la aplicación ###
if __name__ == "__main__":
    raiz = tk.Tk()
    app = MenuPrincipal(raiz)
    raiz.mainloop()
