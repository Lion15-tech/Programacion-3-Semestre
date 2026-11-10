import tkinter as tk
from tkinter import messagebox

class Agenda_CRUD:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("CRUD Básico con Diccionario")
        self.ventana.geometry("400x450")
        #Diccionario principal para almacenar los datos
        self.contactos = {}
        #Nombre y Telefono

        tk.Label(ventana, 
                text="Nombre:").pack(pady=5)
        self.entry_nombre = tk.Entry(ventana)
        self.entry_nombre.pack()

        tk.Label(ventana, 
                text="Teléfono:").pack(pady=5)
        self.entry_telefono = tk.Entry(ventana)
        self.entry_telefono.pack()

        self.btn_crear = tk.Button(ventana, 
                                text="1. Crear / Agregar", 
                                command=self.crear_contacto)
        self.btn_crear.pack(pady=5)

        #Seleccionar de la lista
        self.btn_seleccionar = tk.Button(ventana, 
                                        text="2. Cargar Seleccionado", 
                                        command=self.cargar_contacto)
        self.btn_seleccionar.pack(pady=5)

        #Actualizar
        self.btn_actualizar = tk.Button(ventana, 
                                    text="3. Actualizar", 
                                    command=self.actualizar_contacto)
        self.btn_actualizar.pack(pady=5)

        #Eliminar
        self.btn_eliminar = tk.Button(ventana, 
                                    text="4. Eliminar", 
                                    command=self.eliminar_contacto)
        self.btn_eliminar.pack(pady=5)

        #Ver lista de contactos
        tk.Label(ventana, 
                text="Lista de Contactos:").pack(pady=5)
        self.lista = tk.Listbox(ventana, width=40, height=8)
        self.lista.pack()


    #FUNCIONES CRUD
    #Limpiar las cajas de texto
    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)

    #Actualizar la lista visual en la interfaz a partir del diccionario
    def actualizar_lista_visual(self):
        self.lista.delete(0, tk.END)
        for nombre, telefono in self.contactos.items():
            self.lista.insert(tk.END, f"{nombre} - {telefono}")

    #Crear
    def crear_contacto(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()

        if nombre and telefono:
            if nombre in self.contactos:
                messagebox.showwarning("Atención", "El contacto ya existe. Usa 'Actualizar'.")
            else:
                self.contactos[nombre] = telefono # Guardar en el diccionario
                self.actualizar_lista_visual()
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Contacto agregado correctamente.")
        else:
            messagebox.showwarning("Error", "Por favor llena ambos campos.")

    #Cargar contacto seleccionado de la lista
    def cargar_contacto(self):
        try:
            seleccion = self.lista.get(self.lista.curselection())
            nombre = seleccion.split(" - ")[0]
            #Colocar los datos de nuevo en las cajas de texto
            self.limpiar_campos()
            self.entry_nombre.insert(0, nombre)
            self.entry_telefono.insert(0, self.contactos[nombre])
        except:
            messagebox.showwarning("Atención", "Selecciona un contacto de la lista primero.")

    #Actualizar contacto
    def actualizar_contacto(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()

        if nombre in self.contactos:
            self.contactos[nombre] = telefono # Modifica el valor en el diccionario
            self.actualizar_lista_visual()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Contacto actualizado correctamente.")
        else:
            messagebox.showerror("Error", "El contacto no existe para actualizar.")

    #Eliminar contacto
    def eliminar_contacto(self):
        nombre = self.entry_nombre.get().strip()

        if nombre in self.contactos:
            del self.contactos[nombre] #Elimina del diccionario
            self.actualizar_lista_visual()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Contacto eliminado correctamente.")
        else:
            messagebox.showerror("Error", "Escribe el nombre del contacto a eliminar.")

#Ejecutar la aplicación
if __name__ == "__main__":
    raiz = tk.Tk()
    app = Agenda_CRUD(raiz)
    raiz.mainloop()