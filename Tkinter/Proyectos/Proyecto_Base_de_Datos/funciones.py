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
    ventana.title("Clientes")
    ventana.geometry("1100x600")
    ventana.configure(bg=est.COLOR_FONDO)
    ventana.protocol("WM_DELETE_WINDOW",
                     lambda: (ventana_padre.deiconify(), ventana.destroy()))

    id_cliente_seleccionado = tk.StringVar()

    # ---- Panel de la tabla (derecha) ----
    panel_tabla = tk.Frame(ventana, bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

    # ---- Panel del formulario (izquierda) ----
    panel_form = tk.Frame(ventana, bg=est.COLOR_FONDO, padx=15, pady=15)
    panel_form.pack(side="left", fill="y")

    tk.Label(panel_form, text="CLIENTES",
             font=est.FUENTE_SUBTITULO, bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO, pady=20).pack(padx=15)

    # Helper etiqueta + entry
    def campo(etiqueta):
        tk.Label(panel_form, text=etiqueta,
                 font=est.FUENTE_TEXTO, bg=est.COLOR_FONDO,
                 fg=est.COLOR_TEXTO, pady=5).pack(padx=5)
        e = tk.Entry(panel_form, justify="center")
        e.pack(padx=15, pady=8)
        return e

    entrada_nombre    = campo("Nombre:")
    entrada_apellido  = campo("Apellido:")
    entrada_telefono  = campo("Teléfono:")
    entrada_membresia = campo("Tipo de membresía:")
    entrada_fecha     = campo("Fecha nacimiento (DDMMAAAA):")

    # ---- Treeview con 6 columnas ----
    columnas = ("ID", "Nombre", "Apellido", "Teléfono", "Membresía", "Fecha Nac.")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=130)

    scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(expand=True, fill="both")

    # ---- Auxiliares ----
    def cargar_datos_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for cliente in bd.ver_clientes():
            tabla.insert("", "end", values=cliente)

    def limpiar_campos():
        for e in (entrada_nombre, entrada_apellido, entrada_telefono,
                  entrada_membresia, entrada_fecha):
            e.delete(0, tk.END)
        id_cliente_seleccionado.set("")

    def al_seleccionar_registro(event):
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        if not valores:
            return
        id_cliente_seleccionado.set(valores[0])
        for entry, valor in zip(
            (entrada_nombre, entrada_apellido, entrada_telefono,
             entrada_membresia, entrada_fecha),
            valores[1:]
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)

    # ---- Acciones ----
    def accion_agregar():
        n  = entrada_nombre.get().strip()
        a  = entrada_apellido.get().strip()
        t  = entrada_telefono.get().strip()
        tm = entrada_membresia.get().strip()
        f  = entrada_fecha.get().strip()

        if not (n and a and t and tm and f):
            messagebox.showwarning("Advertencia", "Completa todos los campos.")
            return
        try:
            nuevo_id = bd.agregar_cliente(n, a, t, tm, f)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Cliente agregado", f"ID asignado: {nuevo_id}")
        cargar_datos_tabla()
        limpiar_campos()

    def accion_actualizar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero.")
            return
        try:
            ok = bd.modificar_cliente(
                c_id,
                nombre=entrada_nombre.get().strip(),
                apellido=entrada_apellido.get().strip(),
                telefono=entrada_telefono.get().strip(),
                tipo_membresia=entrada_membresia.get().strip(),
                fecha_nacimiento=entrada_fecha.get().strip()
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        if not ok:
            messagebox.showerror("Error", "El ID no existe en la base de datos.")
            return
        cargar_datos_tabla()
        limpiar_campos()

    def accion_eliminar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al cliente {c_id}?"):
            return
        bd.eliminar_cliente(c_id)
        cargar_datos_tabla()
        limpiar_campos()

    # ---- Botones ----
    crear_boton(panel_form, "AGREGAR", accion_agregar,
                est.FUENTE_BOTONES, est.COLOR_BOTON, est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8)
    crear_boton(panel_form, "ACTUALIZAR", accion_actualizar,
                est.FUENTE_BOTONES, est.COLOR_BOTON, est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8)
    crear_boton(panel_form, "ELIMINAR", accion_eliminar,
                est.FUENTE_BOTONES, est.COLOR_BOTON, est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8)

    cargar_datos_tabla()

def Crear_Ventana_Estado_Membresia(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Estado de Membresía")
    ventana.geometry("1000x600")
    ventana.configure(bg=est.COLOR_FONDO)
    # Si el usuario cierra la ventana regresa al menu inicial
    ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy())) 

    # -- Variable para rastrear el id del cliente -- #
    id_cliente_seleccionado = tk.StringVar()
    
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
    ## --- Botones --- ##
    # Agregar
    crear_boton(panel_para_modificar,
                "AGREGAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Actualizar 
    crear_boton(panel_para_modificar,
                "ACTUALIZAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Eliminar
    crear_boton(panel_para_modificar,
                "ELIMINAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
             
    # --- Widget Treeview (Tabla) ---
    columnas = ("ID", "Tipo de Membresía", "Vigencia", "Fecha de próximo pago")
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
        tipo_membresia.delete(0, tk.END)
        vigencia.delete(0, tk.END)
        fecha_prox_pago.delete(0, tk.END)
        id_cliente_seleccionado.set("")
    
    def al_seleccionar_registro(event):
        item_seleccionado = tabla.focus()
        if not item_seleccionado:
            return
        valores = tabla.item(item_seleccionado, "values")
        if valores:
            id_cliente_seleccionado.set(valores[0])
            
            tipo_membresia.delete(0, tk.END)
            tipo_membresia.insert(0, valores[1])
            
            vigencia.delete(0, tk.END)
            vigencia.insert(0, valores[2])
            
            fecha_prox_pago.delete(0, tk.END)
            fecha_prox_pago.insert(0, valores[3])
    
    # Enlazar la selección en la tabla con la función de autollenado
    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)
    
    # --- Acciones de Botones ---
    def accion_agregar():
        n, a, t = tipo_membresia.get(), vigencia.get(), fecha_prox_pago.get()
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
        n, a, t = tipo_membresia.get(), vigencia.get(), fecha_prox_pago.get()
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


def Crear_Ventana_Tipo_Membresia(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Tipos de Membresía")
    ventana.geometry("1000x600")
    ventana.configure(bg=est.COLOR_FONDO)
    # Si el usuario cierra la ventana regresa al menu inicial
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana_padre.deiconify(), ventana.destroy()))

    # -- Variable para rastrear el id del cliente -- #
    id_cliente_seleccionado = tk.StringVar()

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
    
    # --- ComboBox para el menú desplegable ---
    # Lista para el combobox
    opciones = ["Beneficios", "Planes"]
    menu_seleccion = ttk.Combobox(panel_para_modificar,
                 values=opciones,
                 state="readonly")
    menu_seleccion.pack(pady=10)
    # Esto para usar Combobox y así que la base de datos te permita modificar ya sea el precio
    # el acceso a instalaciones o modificar los planes (básico, estandar y ultra)
    # Frames donde se guardan los Entrys
    entrys_beneficios = tk.Frame(panel_para_modificar,
                            bg=est.COLOR_FONDO,
                            padx=15,
                            pady=5)
    entrys_planes = tk.Frame(panel_para_modificar,
                             bg=est.COLOR_FONDO,
                            padx=15,
                            pady=5)
    # Entrys
    ## -- Beneficios -- ##
    tk.Label(entrys_beneficios,
             text="Precio:",
             font=est.FUENTE_TEXTO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=5).pack(padx=5)
    precio = tk.Entry(entrys_beneficios,
                    justify="center")
    precio.pack(padx=15, pady=15)
    tk.Label(entrys_beneficios,
             text="Acceso a Instalaciones:",
             font=est.FUENTE_TEXTO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=5).pack(padx=5)
    acceso_instalaciones = tk.Entry(entrys_beneficios,
                                    justify="center")
    acceso_instalaciones.pack(padx=15, pady=15)
    tk.Label(entrys_beneficios,
             text="Entrenamiento Personalizado:",
             font=est.FUENTE_TEXTO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=5).pack(padx=5)
    entrenamiento_personalizado = tk.Entry(entrys_beneficios,
                                    justify="center")
    entrenamiento_personalizado.pack(padx=15, pady=15)
    ## --- Botones --- ##
    # Agregar
    crear_boton(entrys_beneficios,
                "AGREGAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Actualizar 
    crear_boton(entrys_beneficios,
                "ACTUALIZAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Eliminar
    crear_boton(entrys_beneficios,
                "ELIMINAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    ## -- Planes -- #
    tk.Label(entrys_planes,
             text="Nombre:",
             font=est.FUENTE_TEXTO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=5).pack(padx=5)
    nombre = tk.Entry(entrys_planes,
                    justify="center")
    nombre.pack(padx=15, pady=15)
    ## --- Botones --- ##
    # Agregar
    crear_boton(entrys_planes,
                "AGREGAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Actualizar 
    crear_boton(entrys_planes,
                "ACTUALIZAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)
    # Eliminar
    crear_boton(entrys_planes,
                "ELIMINAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10)

    def cambiar_vista(event):
        # Primero ocultamos los dos
        entrys_beneficios.pack_forget()
        entrys_planes.pack_forget()

        # Mostramos según lo que eligió el usuario en el combobox
        if menu_seleccion.get() == "Beneficios":
            entrys_beneficios.pack(fill="x", pady=10)
        elif menu_seleccion.get() == "Planes":
            entrys_planes.pack(fill="x", pady=10)

    # Detectar cuándo se cambia el menú desplegable
    menu_seleccion.bind("<<ComboboxSelected>>", cambiar_vista)
    
    # Valor por defecto al abrir la ventana
    menu_seleccion.set("Beneficios")
    cambiar_vista(None)

    # --- Widget Treeview (Tabla) ---
    columnas = ("ID", "Tipo de Membresía", "Vigencia", "Fecha de próximo pago")
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
        precio.delete(0, tk.END)
        acceso_instalaciones.delete(0, tk.END)
        entrenamiento_personalizado.delete(0, tk.END)
        id_cliente_seleccionado.set("")
    def al_seleccionar_registro(event):
        item_seleccionado = tabla.focus()
        if not item_seleccionado:
            return
        valores = tabla.item(item_seleccionado, "values")
        if valores:
            id_cliente_seleccionado.set(valores[0])
            precio.delete(0, tk.END)
            precio.insert(0, valores[1])
            acceso_instalaciones.delete(0, tk.END)
            acceso_instalaciones.insert(0, valores[2])
            entrenamiento_personalizado.delete(0, tk.END)
            entrenamiento_personalizado.insert(0, valores[3])
    # Enlazar la selección en la tabla con la función de autollenado
    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)
    # --- Acciones de Botones ---
    def accion_agregar():
        n, a, t = precio.get(), acceso_instalaciones.get(), entrenamiento_personalizado.get()
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
        n, a, t = precio.get(), acceso_instalaciones.get(), entrenamiento_personalizado.get()
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
        opciones = ["Costos", "Zonas"]
        menu_seleccion = ttk.Combobox(panel_para_modificar,
                     values=opciones,
                     state="readonly")
        menu_seleccion.pack(pady=10)
        
        # Frames donde se guardan los Entrys
        entrys_Zonas = tk.Frame(panel_para_modificar,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=5)
        tk.Label(entrys_Zonas,
                 text="Precio:",
                 font=est.FUENTE_TEXTO,
                 bg=est.COLOR_FONDO,
                 fg=est.COLOR_TEXTO,
                 pady=5).pack(padx=5)
        nombre_zona = tk.Entry(entrys_Zonas,
                        justify="center")
        nombre_zona.pack(padx=15, pady=15)

        entrys_Costos = tk.Frame(panel_para_modificar,
                                 bg=est.COLOR_FONDO,
                                 padx=15,
                                 pady=5)
        tk.Label(entrys_Costos,
                 text="Precio:",
                 font=est.FUENTE_TEXTO,
                 bg=est.COLOR_FONDO,
                 fg=est.COLOR_TEXTO,
                 pady=5).pack(padx=5)
        costo_unico = tk.Entry(entrys_Zonas,
                        justify="center")
        costo_unico.pack(padx=15, pady=15)



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

