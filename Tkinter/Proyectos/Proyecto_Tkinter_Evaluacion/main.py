import tkinter as tk
from tkinter import messagebox
import preguntas

def iniciar_evaluacion():
    nombre = entrada_nombre.get()
    
    # Validar que no se dejen campos vacíos
    if nombre.strip() == "":
        messagebox.showwarning("Cuidado", "Debes ingresar tu nombre para continuar")
        return
        
    # Guardar el nombre en el diccionario y dejar la calificación en 0 por ahora
    preguntas.alumnos_resultados[nombre] = 0
    
    # Ocultar la ventana de registro
    ventana_registro.withdraw()
    
    # Llamar a la siguiente ventana
    abrir_ventana_evaluacion(nombre)

def abrir_ventana_evaluacion(nombre):
    # Creamos una ventana secundaria sobre la principal
    ventana_evaluacion = tk.Toplevel(ventana_registro)
    ventana_evaluacion.title("Evaluación de Python")
    ventana_evaluacion.geometry("400x700")

    # Si cierran esta ventana desde la 'X', cerramos todo el programa
    ventana_evaluacion.protocol("WM_DELETE_WINDOW", ventana_registro.destroy)

    tk.Label(ventana_evaluacion, text=f"Evaluación de: {nombre}").pack(pady=10)

    # Lista para guardar las opciones que el usuario seleccione
    variables_respuestas = []

    # Recorremos la lista de preguntas para mostrarlas en pantalla
    for pregunta, respuesta in enumerate(preguntas.preguntas_evaluacion):
        tk.Label(ventana_evaluacion, text=f"{pregunta+1}. {respuesta['pregunta']}").pack(anchor="w", padx=20, pady=5)
        
        # Creamos una variable de tkinter para rastrear la respuesta de cada pregunta
        var_respuesta = tk.StringVar(value="")
        variables_respuestas.append(var_respuesta)
        
        # Mostramos los botones de opción (radiobuttons)
        for opcion in respuesta["opciones"]:
            tk.Radiobutton(
                ventana_evaluacion, 
                text=opcion, 
                variable=var_respuesta, 
                value=opcion
            ).pack(anchor="w", padx=40)

    def enviar_respuestas():
        # Revisamos si alguna variable sigue en blanco
        for var in variables_respuestas:
            if var.get() == "":
                messagebox.showwarning("Incompleto", "No puedes terminar sin contestar todas las preguntas.")
                return
        
        # Calculamos los aciertos
        aciertos = 0
        total = len(preguntas.preguntas_evaluacion)
        
        for i, var in enumerate(variables_respuestas):
            respuesta_usuario = var.get()
            respuesta_correcta = preguntas.preguntas_evaluacion[i]["respuesta"]
            if respuesta_usuario == respuesta_correcta:
                aciertos += 1
                
        # Calculamos el promedio en base a 100
        promedio = (aciertos / total) * 100
        
        # Guardamos el resultado en el diccionario
        preguntas.alumnos_resultados[nombre] = promedio
        
        # Mostramos los resultados y preguntamos si se evalúa a alguien más
        texto_resultado = f"Obtuviste {aciertos} de {total} aciertos.\nTu promedio es: {promedio}\n\nDiccionario actual:\n{preguntas.alumnos_resultados}"
        
        otro_alumno = messagebox.askyesno("Evaluación Terminada", f"{texto_resultado}\n\n¿Deseas evaluar a otro alumno?")
        
        if otro_alumno:
            # Cerramos la evaluación, limpiamos la caja de texto y mostramos el registro
            ventana_evaluacion.destroy()
            entrada_nombre.delete(0, tk.END)
            ventana_registro.deiconify()
        else:
            # Terminamos el programa cerrando la ventana principal
            ventana_registro.destroy()
        
    tk.Button(ventana_evaluacion, text="Terminar Evaluación", command=enviar_respuestas).pack(pady=20)

# Configuración básica de la ventana de registro
ventana_registro = tk.Tk()
ventana_registro.title("Registro")
ventana_registro.geometry("300x150")

# Textos y campos de texto
etiqueta = tk.Label(ventana_registro, text="Ingresa tu nombre para iniciar:")
etiqueta.pack(pady=10)

entrada_nombre = tk.Entry(ventana_registro)
entrada_nombre.pack(pady=5)

boton_iniciar = tk.Button(ventana_registro, text="Continuar", command=iniciar_evaluacion)
boton_iniciar.pack(pady=10)

# Mantener la ventana abierta
ventana_registro.mainloop()