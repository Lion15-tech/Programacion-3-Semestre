import tkinter as tk
from tkinter import ttk

def actualizar_interfaz(event):
    seleccion = combo_pago.get()
    
    # Primero ocultamos todos los contenedores para "limpiar" la pantalla
    frame_tarjeta.pack_forget()
    frame_paypal.pack_forget()
    frame_efectivo.pack_forget()
    
    # Mostramos solo el contenedor que corresponde a la selección
    if seleccion == "Tarjeta de Crédito":
        frame_tarjeta.pack(pady=10, fill="x", padx=20)
    elif seleccion == "PayPal":
        frame_paypal.pack(pady=10, fill="x", padx=20)
    elif seleccion == "Efectivo (Oxxo/7-Eleven)":
        frame_efectivo.pack(pady=10, fill="x", padx=20)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Formulario Dinámico")
ventana.geometry("400x250")

# --- SECCIÓN DEL COMBOBOX ---
lbl_instruccion = tk.Label(ventana, text="Seleccione su método de pago:", font=("Arial", 10, "bold"))
lbl_instruccion.pack(pady=5)

opciones_pago = ["Tarjeta de Crédito", "PayPal", "Efectivo (Oxxo/7-Eleven)"]
combo_pago = ttk.Combobox(ventana, values=opciones_pago, state="readonly", width=25)
combo_pago.pack(pady=5)
# Asociar el evento de selección a nuestra función
combo_pago.bind("<<ComboboxSelected>>", actualizar_interfaz)


# --- CONTENEDOR 1: TARJETA (Oculto al inicio) ---
frame_tarjeta = tk.LabelFrame(ventana, text="Datos de la Tarjeta")
tk.Label(frame_tarjeta, text="Número de Tarjeta:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
tk.Entry(frame_tarjeta, width=20).grid(row=0, column=1, padx=5, pady=2)
tk.Label(frame_tarjeta, text="CVV:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
tk.Entry(frame_tarjeta, width=5).grid(row=1, column=1, sticky="w", padx=5, pady=2)


# --- CONTENEDOR 2: PAYPAY (Oculto al inicio) ---
frame_paypal = tk.LabelFrame(ventana, text="Cuenta de PayPal")
tk.Label(frame_paypal, text="Correo Electrónico:").pack(side="left", padx=5, pady=5)
tk.Entry(frame_paypal, width=25).pack(side="left", padx=5, pady=5)


# --- CONTENEDOR 3: EFECTIVO (Oculto al inicio) ---
frame_efectivo = tk.LabelFrame(ventana, text="Pago en Efectivo")
tk.Label(frame_efectivo, text="Se generará un código de barras.\nAcuda a su sucursal más cercana.", 
         justify="left", fg="darkgreen").pack(padx=5, pady=5)


ventana.mainloop()
