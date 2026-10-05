import tkinter as tk
from tkinter import messagebox
import os

### Paleta de Colores (Estilo Verde Institucional) ###
COLOR_FONDO_PRINCIPAL = "#BCF6BC"  # Verde menta muy claro para el fondo
COLOR_TEXTO_TITULO    = "#1E4620"  # Verde bosque oscuro para los títulos
COLOR_BOTON_NORMAL    = "#2E7D32"  # Verde estándar para los botones
COLOR_BOTON_HOVER     = "#1B5E20"  # Verde más oscuro cuando clckeas con el mouse
COLOR_TEXTO_BOTON     = "#FFFFFF"  # Texto blanco para que contraste con los botones

### Fuentes ###s
fuente_titulo = ("Impact", 22)
fuente_botones = ("Helvetica", 11, "bold")

class MenuPrincipal:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gráficas y Ecuaciones - CECYTEQ")
        self.ventana.geometry("480x450")
        self.ventana.config(bg=COLOR_FONDO_PRINCIPAL)

        #### CONFIGURACIÓN DEL ICONO ####
        self.carpeta_proyecto = os.path.dirname(__file__)
        self.ruta_icono = os.path.join(self.carpeta_proyecto, "logo_cecyteq.png")

        try:
            self.icono = tk.PhotoImage(file=self.ruta_icono)
            self.ventana.iconphoto(False, self.icono)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        # Configuración de cuadrícula (Grid)
        self.ventana.rowconfigure(0, weight=1)
        self.ventana.rowconfigure(1, weight=1)
        self.ventana.rowconfigure(2, weight=1)

        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)

        
        tk.Label(self.ventana,
                text="Gráficas \ny \nEcuaciones", 
                font=fuente_titulo,
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL,
                relief="flat",
                padx=20).grid(row=0, column=0, rowspan=3, sticky="nsew") 

        btn_primer = tk.Button(self.ventana,
                text="Gráfica una ecuación \nde primer grado",
                font=fuente_botones,
                bg=COLOR_BOTON_NORMAL,
                fg=COLOR_TEXTO_BOTON,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_TEXTO_BOTON,
                cursor="hand2",
                bd=0,
                pady=10)
        btn_primer.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        btn_primer.config(command=self.grafica_primer_grado)

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


    #### VENTANAS HIJAS ####
    def grafica_primer_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Primer Grado")
        ventana_hija.geometry("350x250")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        tk.Label(ventana_hija, 
                text="Interfaz de Primer Grado aquí", 
                font=("Arial", 12, "bold"),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=50)

    def grafica_segundo_grado(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Ecuación de Segundo Grado")
        ventana_hija.geometry("350x250")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        tk.Label(ventana_hija, 
                text="Interfaz de Segundo Grado aquí", 
                font=("Arial", 12, "bold"),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=50)

    def ventana_sistema_ecuaciones(self):
        ventana_sistemas = tk.Toplevel(self.ventana)
        ventana_sistemas.title("Sistemas de Ecuaciones")
        ventana_sistemas.geometry("400x300")
        ventana_sistemas.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_sistemas.iconphoto(False, self.icono)

        tk.Label(ventana_sistemas, 
                text="Selecciona el Tipo de Sistema", 
                font=("Impact", 18),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=25)

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

    def sistema_2x2(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 2x2")
        ventana_hija.geometry("350x250")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        tk.Label(ventana_hija, 
                text="Campos para resolver Sistema 2x2", 
                font=("Arial", 12, "bold"),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=50)

    def sistema_3x3(self):
        ventana_hija = tk.Toplevel(self.ventana)
        ventana_hija.title("Sistema de Ecuaciones 3x3")
        ventana_hija.geometry("350x250")
        ventana_hija.config(bg=COLOR_FONDO_PRINCIPAL)
        if hasattr(self, 'icono'): ventana_hija.iconphoto(False, self.icono)
        
        tk.Label(ventana_hija, 
                text="Campos para resolver Sistema 3x3", 
                font=("Arial", 12, "bold"),
                fg=COLOR_TEXTO_TITULO,
                bg=COLOR_FONDO_PRINCIPAL).pack(pady=50)

### Ejecutar la aplicación ###
if __name__ == "__main__":
    raiz = tk.Tk()
    app = MenuPrincipal(raiz)
    raiz.mainloop()
