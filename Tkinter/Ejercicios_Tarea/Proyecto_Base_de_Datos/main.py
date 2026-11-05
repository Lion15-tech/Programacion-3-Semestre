import tkinter as tk
import estilos as est  
import funciones as func
import os
#From estilos import *

#import base datos
#import funciones


ventana_principal = tk.Tk()
ventana_principal.title("Base de Datos")
ventana_principal.resizable(False, False)
ventana_principal.geometry("500x600")
ventana_principal.config(bg=est.COLOR_FONDO)
## CONFIGURACIÓN DEL ICONO ##
carpeta_proyecto = os.path.dirname(__file__)
ruta_icono = os.path.join(carpeta_proyecto, "logo_cecyteq.png")
try:
    icono = tk.PhotoImage(file=ruta_icono)
    ventana_principal.iconphoto(True, icono)
except Exception as e:
    print(f"Error al cargar el icono: {e}")

#----- TITULO ----

tk.Label(
    ventana_principal,
    text="BASE DE DATOS",
    font=est.FUENTE_TITULO,
    bg=est.COLOR_FONDO,
    fg=est.COLOR_TEXTO,
    pady=20
).pack()


# ====== BOTONES ======

# ----- Clientes -----
func.crear_boton(
    ventana_principal, 
    "Clientes", 
    lambda: func.Crear_Ventana_Clientes(ventana_principal), 
    est.FUENTE_TEXTO,
    est.COLOR_BOTON, 
    est.COLOR_TEXTO, 
    est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

# ---- Estado de Membresía ----
func.crear_boton(
    ventana_principal, 
    "Estado de membresía", 
    lambda: func.Crear_Ventana_Estado_Membresia(ventana_principal), 
    est.FUENTE_TEXTO,
    est.COLOR_BOTON, 
    est.COLOR_TEXTO, 
    est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

# ---- Tipo de Membresía ----
func.crear_boton(
    ventana_principal, 
    "Tipo de Membresía", 
    lambda: func.Crear_Ventana_Tipo_Membresia(ventana_principal), 
    est.FUENTE_TEXTO,
    est.COLOR_BOTON, 
    est.COLOR_TEXTO, 
    est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

# ---- Inversión ----
func.crear_boton(
    ventana_principal, 
    "Inversión", 
    lambda: func.Crear_Ventana_Inversion(ventana_principal), 
    est.FUENTE_TEXTO,
    est.COLOR_BOTON, 
    est.COLOR_TEXTO, 
    est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

# ----- Instalaciones ----
func.crear_boton(
    ventana_principal, 
    "Instalaciones", 
    lambda: func.Crear_Ventana_Instalaciones(ventana_principal), 
    est.FUENTE_TEXTO,
    est.COLOR_BOTON, 
    est.COLOR_TEXTO, 
    est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

ventana_principal.mainloop()

