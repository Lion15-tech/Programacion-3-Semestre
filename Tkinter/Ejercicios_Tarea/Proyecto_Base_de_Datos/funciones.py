import tkinter as tk
from tkinter import ttk, messagebox
import estilos as est
import base_datos as bd

def crear_boton(padre, texto, comando, fuente_texto,color_fondo, color_texto, color_boton_presionado):
    boton = tk.Button(padre, 
                    text=texto, 
                    command=comando,
                    font=fuente_texto,
                    bg=color_fondo, 
                    fg=color_texto,
                    activebackground=color_boton_presionado)
    return boton


def Crear_Ventana_Clientes(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Usuarios")
    ventana.geometry("1000x600")
    ventana.configure(bg=est.COLOR_FONDO)
    # Si el usuario cierra la ventana regresa al menu inicial
    ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy()))        
    # -- Variable para rastrear el id del cliente -- #
    id_cliente_seleccionado = tk.StringVar()
    
    # Creamos el Frame para la tabla
    panel_tabla = tk.Frame(ventana,
                            bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)
    # Creamos el Frame donde ingresar los datos
    panel_para_modificar = tk.Frame(ventana,
                            bg=est.COLOR_FONDO,
                            padx=15,
                            pady=15)
    panel_para_modificar.pack(side="left", fill="y")           
    # ------ Titulo ----- #
    tk.Label(panel_para_modificar,
            text="CLIENTES",
            font=est.FUENTE_SUBTITULO,
            bg=est.COLOR_FONDO,
            fg=est.COLOR_TEXTO,
            pady=20
            ).pack(padx=15)
    # Entrys
    tk.Label(panel_para_modificar,
             text="Nombre:",
             font=est.FUENTE_TEXTO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=5).pack(padx=5)
    nombre = tk.Entry(panel_para_modificar,
                    justify="center")
    nombre.pack(padx=15, pady=10)      
    tk.Label(panel_para_modificar,
                     text="Apellido:",
                     font=est.FUENTE_TEXTO,
                     bg=est.COLOR_FONDO,
                     fg=est.COLOR_TEXTO,
                     pady=5).pack(padx=5)
    apellido = tk.Entry(panel_para_modificar,
                    justify="center")
    apellido.pack(padx=15, pady=10)    
    tk.Label(panel_para_modificar,
                     text="Tipo de membresía:",
                     font=est.FUENTE_TEXTO,
                     bg=est.COLOR_FONDO,
                     fg=est.COLOR_TEXTO,
                     pady=5).pack(padx=5)
    tipo_membresia = tk.Entry(panel_para_modificar,
                    justify="center")
    tipo_membresia.pack(padx=15, pady=10)      
    tk.Label(panel_para_modificar,
                     text="Teléfono:",
                     font=est.FUENTE_TEXTO,
                     bg=est.COLOR_FONDO,
                     fg=est.COLOR_TEXTO,
                     pady=5).pack(padx=5)
    telefono = tk.Entry(panel_para_modificar,
                    justify="center")
    telefono.pack(padx=15, pady=10)    
    ## --- Botones --- ##
    # Agregar
    crear_boton(panel_para_modificar,
                "AGREGAR",
                accion_agregar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Actualizar 
    crear_boton(panel_para_modificar,
                "ACTUALIZAR",
                accion_actualizar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Eliminar
    crear_boton(panel_para_modificar,
                "ELIMINAR",
                accion_eliminar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
             
    # --- Widget Treeview (Tabla) ---
    columnas = ("ID", "Nombre", "Apellido", "Teléfono")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")
    
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    
    # Agregar Scrollbar a la tabla
    scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(expand=True, fill="both")
    
    # --- Funciones Auxiliares para la Interfaz ---
    def cargar_datos_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for cliente in bd.obtener_clientes():
            tabla.insert("", "end", values=cliente)
    
    def limpiar_campos():
        nombre.delete(0, tk.END)
        apellido.delete(0, tk.END)
        telefono.delete(0, tk.END)
        id_cliente_seleccionado.set("")
    
    def al_seleccionar_registro(event):
        item_seleccionado = tabla.focus()
        if not item_seleccionado:
            return
        valores = tabla.item(item_seleccionado, "values")
        if valores:
            id_cliente_seleccionado.set(valores[0])
            
            nombre.delete(0, tk.END)
            nombre.insert(0, valores[1])
            
            apellido.delete(0, tk.END)
            apellido.insert(0, valores[2])
            
            telefono.delete(0, tk.END)
            telefono.insert(0, valores[3])
    
    # Enlazar la selección en la tabla con la función de autollenado
    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)
    
    # --- Acciones de Botones ---
    def accion_agregar():
        n, a, t = nombre.get(), apellido.get(), telefono.get()
        if n and a and t:
            bd.agregar_cliente(n, a, t)
            cargar_datos_tabla()
            limpiar_campos()
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos.")
    
    def accion_actualizar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la tabla para modificar.")
            return
        n, a, t = nombre.get(), apellido.get(), telefono.get()
        bd.actualizar_cliente(c_id, n, a, t)
        cargar_datos_tabla()
        limpiar_campos()
    
    def accion_eliminar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la tabla para eliminar.")
            return
        bd.eliminar_cliente(c_id)
        cargar_datos_tabla()
        limpiar_campos()
    # Carga inicial de registros
    cargar_datos_tabla()

def Crear_Ventana_Estado_Membresia(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Estado de Membresía")
    ventana.geometry("1000x600")
    ventana.configure(bg=est.COLOR_FONDO)
    # Si el usuario cierra la ventana regresa al menu inicial
    ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy())) 
    
    # Creamos el Frame donde ingresar los datos
    panel_para_modificar = tk.Frame(ventana,
                            bg=est.COLOR_FONDO,
                            padx=15,
                            pady=15)
    panel_para_modificar.pack(side="left", fill="y")
    # Creamos el Frame para la tabla
    panel_tabla = tk.Frame(ventana,
                            bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)
    # ------ Titulo ------
    tk.Label(panel_para_modificar,
            text="ESTADO DE \nMEMBRESÍA",
            font=est.FUENTE_SUBTITULO,
            bg=est.COLOR_FONDO,
            fg=est.COLOR_TEXTO,
            pady=20
            ).pack(padx=15)
    # Entrys
    tk.Label(panel_para_modificar,
                     text="Tipo de Membresía:",
                     font=est.FUENTE_TEXTO,
                     bg=est.COLOR_FONDO,
                     fg=est.COLOR_TEXTO,
                     pady=5).pack(padx=5)
    tipo_membresia = tk.Entry(panel_para_modificar,
                    justify="center")
    tipo_membresia.pack(padx=15, pady=15)
    tk.Label(panel_para_modificar,
                             text="Vigencia:",
                             font=est.FUENTE_TEXTO,
                             bg=est.COLOR_FONDO,
                             fg=est.COLOR_TEXTO,
                             pady=5).pack(padx=5)
    vigencia = tk.Entry(panel_para_modificar,
                    justify="center")
    vigencia.pack(padx=15, pady=15)
    tk.Label(panel_para_modificar,
                             text="Fecha de Pago:",
                             font=est.FUENTE_TEXTO,
                             bg=est.COLOR_FONDO,
                             fg=est.COLOR_TEXTO,
                             pady=5).pack(padx=5)
    fecha_prox_pago = tk.Entry(panel_para_modificar,
                    justify="center")
    fecha_prox_pago.pack(padx=15, pady=15)


def Crear_Ventana_Tipo_Membresia(ventana_padre):
        ventana_padre.withdraw()
        ventana = tk.Toplevel(ventana_padre)
        ventana.title("Tipos de Membresía")
        ventana.geometry("1000x600")
        ventana.configure(bg=est.COLOR_FONDO)
        # Si el usuario cierra la ventana regresa al menu inicial
        ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana_padre.deiconify(), ventana.destroy())) 
        
        # Creamos el Frame donde ingresar los datos
        panel_para_modificar = tk.Frame(ventana,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=15)
        panel_para_modificar.pack(side="left", fill="y")
        # Creamos el Frame para la tabla
        panel_tabla = tk.Frame(ventana,
                                bg=est.FONDO_TABLA)
        panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        # ----- Titulo ------
        tk.Label(panel_para_modificar,
                text="TIPOS DE \nMEMBRESÍA",
                font=est.FUENTE_SUBTITULO,
                bg=est.COLOR_FONDO,
                fg=est.COLOR_TEXTO,
                pady=20
                ).pack(padx=15)
        # Entrys
        tk.Label(panel_para_modificar,
                                 text="Precio:",
                                 font=est.FUENTE_TEXTO,
                                 bg=est.COLOR_FONDO,
                                 fg=est.COLOR_TEXTO,
                                 pady=5).pack(padx=5)
        precio = tk.Entry(panel_para_modificar,
                        justify="center")
        precio.pack(padx=15, pady=15)

        tk.Label(panel_para_modificar,
                                 text="Acceso a Instalaciones:",
                                 font=est.FUENTE_TEXTO,
                                 bg=est.COLOR_FONDO,
                                 fg=est.COLOR_TEXTO,
                                 pady=5).pack(padx=5)
        acceso_instalaciones = tk.Entry(panel_para_modificar,
                                        justify="center")
        acceso_instalaciones.pack(padx=15, pady=15)

        tk.Label(panel_para_modificar,
                                 text="Entrenamiento Personalizado:",
                                 font=est.FUENTE_TEXTO,
                                 bg=est.COLOR_FONDO,
                                 fg=est.COLOR_TEXTO,
                                 pady=5).pack(padx=5)
        entrenamiento_personalizado = tk.Entry(panel_para_modificar,
                                        justify="center")
        entrenamiento_personalizado.pack(padx=15, pady=15)


def Crear_Ventana_Inversion(ventana_padre):
        ventana_padre.withdraw()
        ventana = tk.Toplevel(ventana_padre)
        ventana.title("Inversión")
        ventana.geometry("1000x600")
        ventana.configure(bg=est.COLOR_FONDO)
        # Si el usuario cierra la ventana regresa al menu inicial
        ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy())) 
        
        # Creamos el Frame donde ingresar los datos
        panel_para_modificar = tk.Frame(ventana,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=15)
        panel_para_modificar.pack(side="left", fill="y")
        # Creamos el Frame para la tabla
        panel_tabla = tk.Frame(ventana,
                                bg=est.FONDO_TABLA)
        panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        # ------ Titulo -----
        tk.Label(panel_para_modificar,
                text="INVERSIÓN",
                font=est.FUENTE_SUBTITULO,
                bg=est.COLOR_FONDO,
                fg=est.COLOR_TEXTO,
                pady=20
                ).pack(padx=15)
        # --- ComboBox para el menú desplegable ---
        # Lista para el combobox
        opciones = ["Pagos", "Zonas"]
        menu_seleccion = ttk.Combobox(panel_para_modificar,
                     values=opciones,
                     state="readonly")
        menu_seleccion.pack(pady=10)
        # Frames donde se guardan los Entrys
        entrys_Pagos = tk.Frame(panel_para_modificar,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=5)
        nombre = tk.Entry(entrys_Pagos,
                        justify="center")
        nombre.pack(padx=15, pady=15)
        # V


def Crear_Ventana_Instalaciones(ventana_padre):
        ventana_padre.withdraw()
        ventana = tk.Toplevel(ventana_padre)
        ventana.title("Instalaciones")
        ventana.geometry("1000x600")
        ventana.configure(bg=est.COLOR_FONDO)
        # Si el usuario cierra la ventana regresa al menu inicial
        ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy())) 
        
        # Creamos el Frame donde ingresar los datos
        panel_para_modificar = tk.Frame(ventana,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=15)
        panel_para_modificar.pack(side="left", fill="y")
        # Creamos el Frame para la tabla
        panel_tabla = tk.Frame(ventana,
                                bg=est.FONDO_TABLA)
        panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        tk.Label(panel_para_modificar,
                text="INSTALACIONES",
                font=est.FUENTE_SUBTITULO,
                bg=est.COLOR_FONDO,
                fg=est.COLOR_TEXTO,
                pady=20
                ).pack(padx=15)
        # Entrys
        nombre = tk.Entry(panel_para_modificar,
                        justify="center")
        nombre.pack(padx=15, pady=15)

        apellido = tk.Entry(panel_para_modificar,
                        justify="center")
        apellido.pack(padx=15, pady=15)
        
        tipo_membresia = tk.Entry(panel_para_modificar,
                        justify="center")
        tipo_membresia.pack(padx=15, pady=15)

        telefono = tk.Entry(panel_para_modificar,
                        justify="center")
        telefono.pack(padx=15, pady=15)

