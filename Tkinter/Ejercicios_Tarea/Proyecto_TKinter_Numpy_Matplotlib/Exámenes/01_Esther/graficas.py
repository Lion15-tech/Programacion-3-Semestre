import tkinter as tk
from tkinter import messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
icono = "cecyteq.ico"
#ESTE ES DE LA OPCION 1
def grafica_linea(valor1, valor2, valor3, valor4, ventana_mayor):
    try:
        x1 =float(valor1)
        y1 = float(valor2)
        x2= float(valor3)
        y2 = float(valor4)
    except ValueError:
        messagebox.showerror("ERROR JAJAJ", "Ingrese numeros validos")
        return
    if x1 == x2:
        messagebox.showerror("Error", "x1 y x2 no pueden ser iguales")
        return
    m =  (y2 - y1) / (x2-x1) #aqui es para el calculo de la pendiente
#Aqui es donde numpy generara los rango de X para graficar desde x1 hasta x2
    x_min = min(x1, x2) - 10
    x_max = max(x1, x2) + 10
    x = np.linspace(x_min, x_max, 400)
 #Este es para ecuacion punto-pendiente: y-y1 = m(x-x1)      
    y = m * (x - x1) + y1
#Esta es la ventana para la grafica
    ventana_grafica = tk.Toplevel(ventana_mayor)
    ventana_grafica.title(f"Graficar dos puntos ")
    ventana_grafica.geometry("500x400")
    ventana_grafica.config(bg= "#A47148")
   
    try:
        ventana_grafica.iconbitmap(icono)
    except Exception:
            pass
    
#Aqui se usa el matplotlib para crear la figura y ejes 
    fig, ax = plt.subplots(figsize = (5,4), dpi = 100) # el plt.subplots sirve para crear una fgra y una cuadricula
#EL fig es la ventana contenedora, el ax es el grafico en donde van a ir las lineas, puntos y numeros
#el figsize es para definir  el tamaño de la iamgen en pulgadas 5 de ancho por 4 de alto
#el dpi = 100 significa puntos por pulgada
    etiqueta = f"pendiente de la recta {m} \npar1: ({x1:.0f}, {y1:.0f}) par 2: ({x2:.0f}, {y2:.0f})"
    ax.plot(x,y,  label=etiqueta, color= "#AC9DF1", linewidth=1.2, marker= 'o', markersize=3)#el x, y,  se le pasa la lista con puntos numericos
    #Aqui dibuja SOLO los 2 puntos especificos introducidos
    ax.scatter([x1,x2], [y1, y2], color= "#B9FFD4", s=40, zorder=5)
    #el color es para la linea, y el linewidht para grosor de linea
    ax.axhline(0, color= 'black', linewidth = 0.8, linestyle = '--') #ES PARA HOPRIZONTAL en el eje x
#el 0 la posicion en el eje Y, y el linestyle estilo de linea
    ax.axvline(0, color = 'black', linewidth= 0.8, linestyle= '--') #Lo mismo pero para la linea VERTICAL eje 
    ax.grid(True, linestyle = ':', alpha=0.6)#El agrid es para activar la cuadricula y personalizar en el fondo grafico
    ax.legend(loc= 'upper left')
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill= tk.BOTH, expand = True, padx=10, pady=10)
#el canvas.get_tk_widget es para convertir el canava en en widget para que la interfaz pueda manipualrlo
#el master le especifica en que ventana se va a colocar el canva


#AQUI ES PARA LA OPCION DE RAIZ CUADRATICA(DE SEGUNDO GRADO)
def grafica_linea2(valor3, valor4, valor5, ventana_may2):
    try:
        a1 = float(valor3)
        b2 = float(valor4)
        c = float(valor5)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese Numeros Validos")
        return
    if a1 == 0:
        messagebox.showerror("Error", "El valor de 'a' no puede ser 0 en una ecuacion cuadratica")
        return
    x = np.linspace(-10, 10, 400)
    y = a1 * (x**2) + b2 * x + c
    
    ventana_grafica2 = tk.Toplevel(ventana_may2)
    ventana_grafica2.title(f"Grafica: Y = {a1}X² + {b2}X + {c}")
    ventana_grafica2.geometry("500x400")
    ventana_grafica2.configure(bg="#A47148")
    try:
        ventana_grafica2.iconbitmap(icono)
    except Exception:
            pass
    fig, ax = plt.subplots(figsize = (5,4), dpi = 100)
    ax.plot(x,y, label = f"Y = {a1}X² + {b2}X + {c}", color= "#BEA7F3", linewidth = 2)
    ax.axhline(0, color= 'black', linewidth = 0.8, linestyle = '--')
    ax.axvline(0, color = 'black', linewidth = 0.8, linestyle = '--')
    ax.grid(True, linestyle = ':', alpha=0.6)
    ax.grid(True, linestyle = ":", alpha = 0.6)
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafica2)
    canvas.draw()
    canvas.get_tk_widget().pack(fill= tk.BOTH, expand = True, padx=10, pady=10)
    #aqui es la forumula general 
    discriminante = b2 ** 2 - 4 * a1 * c
    if discriminante >= 0:
        raiz = np.sqrt(discriminante) # aqui se extrae la raiz
        raiz1 = (-b2 + raiz) / (2 * a1)
        raiz2 = (-b2 - raiz) / (2 * a1)
        messagebox.showinfo("Resultados", f"x1 = {round(raiz1, 2)} \n x2= {round(raiz2, 2)}")
    else:
        messagebox.showinfo("Resultados", "Sin soluciones reales (Osea que la raiz es negativa)")

#AQUI ES PARA LA ECUACIONES DE 2X2
def resolver_2x2(e_a1, e_b1, e_c1, e_a2, e_b2, e_c2, ventana_mayor):
    try:
        a1 = float(e_a1)
        b1 = float(e_b1)
        c1 = float(e_c1)
        a2 = float(e_a2)
        b2 = float(e_b2)
        c2 = float(e_c2)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese solo numeros")
        return
    determinante = a1 * b2 - b1 * a2 #es para hallar el determinante
    if determinante == 0:
        messagebox.showwarning("AVISO", "El sistema no tiene una solucion unica, es decir las dos lineas no se cruzan en un solo punto")
        return
    #se hace la resoluciond del sistema: 
    x_solucion = (c1 * b2 - c2 * b1)/ determinante #para hallar el valor de x
    y_solucion = (a1 * c2 - c1 * a2)/ determinante
    messagebox.showinfo("Solucion del sistema 2x2", f"Punto de Interseccion:\nX ={round(x_solucion, 2)} \nY ={round(y_solucion, 2)}")
    x_vals = np.linspace(x_solucion - 10, x_solucion + 10, 300) #crea una lista de parametros de 300  a lo largo del eje x
    ventana_grafica = tk.Toplevel(ventana_mayor)
    ventana_grafica.title("Ecuaciones de 2x2 con el Metodo Cramer")
    ventana_grafica.geometry("350x350")
    ventana_grafica.configure(bg="#A47148")
    try : 
        ventana_grafica.iconbitmap(icono)
    except Exception:
        pass
    fig, ax = plt.subplots(figsize = (5, 4), dpi = 100)
    #----ESTA ES PARA LA RECTA 1 : a1*x + b1*y = c1 => y = (c1 - a1*x) / b1 --
    #Para graficar cada ecuacion (ax - by = c), despejamos la variable Y = 
    # bY = c - aX ----> y = c - aX / b
    if b1 != 0:
        y1_vals = (c1 - a1 * x_vals) /b1
        ax.plot(x_vals, y1_vals, label = f"{a1}x + {b1}y = {c1}", color="#E010A5", linewidth= 3) #se aplica la primera formula y se traza la siguiente linea
    else:
        ax.axvline(c1/a1, label=f"{a1} X = {c1}", color="#B603FD", linewidth = 3) #Esto es siginifca que si b1 == 0 es una linea completamente vertical
    #Para la recta 2 = a2*x + b2*y = c2 => y = (c2 - a2*x) /b2 => 
    if b2 != 0:
        y2_vals = (c2 - a2 * x_vals) / b2
        ax.plot(x_vals, y2_vals, label = f"{a2}x + {b2}y = {c2}", color = "#08FAB1", linewidth= 3)      
    else:
        ax.axvline(c2/a2, label=f"{a2} X = {c2}", color="#0F93F1", linewidth = 3)
    #punto de interseccion (solucion)
    ax.scatter([x_solucion], [y_solucion], color = "#490746CC", s= 60, zorder = 5, label= f"Solucion: ({round(x_solucion, 2)}, {round(y_solucion, 2)})") 
    ax.axhline(0, color='pink', linewidth = 0.8, linestyle = '--')
    ax.axvline(0, color = 'pink', linewidth = 0.8, linestyle = '--')
    ax.grid(True, linestyle = ':', alpha = 0.6)
    ax.legend(loc = 'upper left')
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#AQUI ES PARA EL SISTEMA DE 3X3
def resolver_3x3(e_a1, e_b1, e_c1, e_d1, e_a2, e_b2, e_c2, e_d2, e_a3, e_b3, e_c3, e_d3, ventana_mayor):
    try:
        a1 = float(e_a1)
        b1 = float(e_b1)
        c1 = float(e_c1)
        d1 = float(e_d1)
        a2 = float(e_a2)
        b2 = float(e_b2)
        c2 = float(e_c2)
        d2 = float(e_d2)
        a3 = float(e_a3)
        b3 = float(e_b3)
        c3 = float(e_c3)
        d3 = float(e_d3)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese solo numeros")
        return
    A = np.array([      #es para la matriz de los coeficientes, osea que guarda solo los numeros que acompañan las letras
        [a1, b1, c1],
        [a2, b2, c2], 
        [a3, b3, c3]
    ])
    B = np.array([d1, d2, d3]) #guardan las constantes independientes que estan del lado derecho del signo = 
    #se comprrueba si el sistema tien solucion
    determinante = np.linalg.det(A) #el linalg.det se utiliza para calcular la determinante de una matriz
    if abs(determinante) < 1e-9: #el abs(determinante) calcula su valor ignorando si el signo es negativo o positivo
        # el <1e-9 es la notacion cientifica pa 1x10 elevado a 9, cantidad peque
        messagebox.showwarning("EROR JAJA", "El sistema no tiene solucion unica")
        return
    solucion = np.linalg.solve(A, B) #es la funcion de numpy que aplica cualquier metodo para despejar X, Y, Z de forma instantanea
    x, y, z = solucion[0], solucion[1], solucion[2] # solucion 0 para X, solucion Y para 1, y la 2 para Z
    messagebox.showinfo(
        "Solucion del Sistema 3x3", 
        f"Punto de Interseccion = \n\n X ={round(x, 2)}\n Y = {round(y, 2)}\nZ = {round(z, 2)}"
    )
    #AQUI ES PARA LA GRAFICA DIMENSIONAL EN 3D
    ventana_grafica = tk.Toplevel(ventana_mayor)
    ventana_grafica.title("Grafica 3d -Sistema de Ecuaciones 3x3")
    ventana_grafica.geometry("520x450")
    ventana_grafica.configure(bg ="#694312")
    try:
        ventana_grafica.iconbitmap(icono)
    except Exception:
        pass
    #para crear figura y  eje con proyeccion al 3d
    fig = plt.figure(figsize=(5,4), dpi=100)
    ax = fig.add_subplot(111, projection = '3d')
    #Se crea la malla sobre el eje XY alrededor de la solucion
    X_vals = np.linspace(x - 5, x+5, 20)
    Y_vals = np.linspace(y - 5, y+ 5, 20)
    X_grid, Y_grid = np.meshgrid(X_vals, Y_vals) #Es para trasformar dos o mas vectores de coordenadas dimensionale
    if c1 != 0:
        Z1 = (d1 - a1 * X_grid - b1 * Y_grid) / c1
        ax.plot_surface(X_grid, Y_grid, Z1, alpha = 0.5, color = "#FC84E2FF")#sirve para crear graficos de superficies tridimensionales
    #dibujar plano 2
    if c2 != 0:
        Z2 = (d2 - a2 * X_grid - b2 * Y_grid)/ c2
        ax.plot_surface(X_grid, Y_grid, Z2, alpha = 0.5, color= "#01FFF2")
    #Dibujar plano 3
    if c3 != 0:
        Z3 = (d3- a3 * X_grid - b3 * Y_grid)/c3
        ax.plot_surface(X_grid, Y_grid, Z3, alpha= 0.5, color ="#7C2378")
    #Grafica la solucion como una esfera redonda en 3d
    ax.scatter([x], [y], [z],color = "#FA259A", s=80, label=f"Solución ({round(x,2)}, {round(y, 2)}, {round(z, 2)})")
    #etiqueta de los 3 ejes
    ax.set_xlabel = ('EJE X')
    ax.set_ylabel = ('EJE Y')
    ax.set_zlabel = ('EJE Z')
    ax.legend(loc='upper left')
    canvas = FigureCanvasTkAgg(fig, master= ventana_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill = tk.BOTH, expand=True, padx=10, pady=10)




    #PARA EL TRIANGULO RECTANGULO
def resolver_trig_rectangulo(modo, v1, v2):
    try:
        val1, val2 = float(v1), float(v2)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese valores numéricos válidos.")
        return

    if val1 <= 0 or val2 <= 0:
        messagebox.showerror("ERROR", "Los datos deben ser mayores que cero.")
        return

    if modo == 1:  # Dos catetos (a, b)
        a, b = val1, val2
        c = math.sqrt(a**2 + b**2)
        alpha = math.degrees(math.atan(a / b)) # el degrees es para convertir el angulo de radianes a grdos
        beta = 90.0 - alpha
    elif modo == 2:  #Cateto e hipotenusa
        a, c = val1, val2
        if c <= a:
            messagebox.showerror("ERROR", "La hipotenusa (c) debe ser estrictamente mayor que el cateto (a).")
            return
        b = math.sqrt(c**2 - a**2)
        alpha = math.degrees(math.asin(a / c)) #el asin es para calcular el arcoseno(seno nverso) de un numero 
        beta = 90.0 - alpha
    elif modo == 3:  # Cateto (a) y Ángulo agudo A (grados)
        a, alpha = val1, val2
        if alpha >= 90.0:
            messagebox.showerror("ERROR", "El ángulo agudo debe ser menor a 90°.")
            return
        beta = 90.0 - alpha
        c = a / math.sin(math.radians(alpha)) 
        b = math.sqrt(c**2 - a**2) #aqui calcula a raiz cuadrada

  

    msg = f"--- RESULTADOS TRIÁNGULO RECTÁNGULO ---\n\n" \
          f"Cateto a = {a:.2f}\nCateto b = {b:.2f}\nHipotenusa c = {c:.2f}\n" \
          f"Ángulo A = {alpha:.2f}°\nÁngulo B = {beta:.2f}°\nÁngulo C = 90.00°\n\n" \
          
    messagebox.showinfo("Solución Triángulo Rectángulo", msg)


def resolver_trig_oblicuangulo(modo, v1, v2, v3):
    try:
        val1, val2, val3 = float(v1), float(v2), float(v3)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese valores numéricos válidos en los tres campos.")
        return

    if val1 <= 0 or val2 <= 0 or val3 <= 0:
        messagebox.showerror("ERROR", "Todos los valores deben ser obligatoriamente positivos.")
        return

    if modo == 1:  # Tres lados (a, b, c)
        a, b, c = val1, val2, val3
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            messagebox.showerror("ERROR", "Desigualdad triangular: La suma de 2 lados debe ser mayor al 3ro.")
            return
        cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
        cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
        alpha = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
        beta = math.degrees(math.acos(max(-1.0, min(1.0, cos_B))))
        gamma = 180.0 - alpha - beta

    elif modo == 2:  # LAL (a, b y Ángulo C en grados)
        a, b, gamma = val1, val2, val3
        if gamma >= 180.0:
            messagebox.showerror("ERROR", "El ángulo C debe ser menor a 180°.")
            return
        c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(math.radians(gamma)))
        cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
        alpha = math.degrees(math.acos(max(-1.0, min(1.0, cos_A)))) # el acos es para calcular el arcoseno de un numero y devolver el angulo correspondiente de un numero
        beta = 180.0 - alpha - gamma

    elif modo == 3:  # ALA (Ángulo A, Ángulo B, Lado c)
        alpha, beta, c = val1, val2, val3
        if alpha + beta >= 180.0:
            messagebox.showerror("ERROR", "La suma de los dos ángulos A + B debe ser menor a 180°.")
            return
        gamma = 180.0 - alpha - beta
        a = c * (math.sin(math.radians(alpha)) / math.sin(math.radians(gamma))) #el radians es para cnvertir un angulo de grados a radianes

        b = c * (math.sin(math.radians(beta)) / math.sin(math.radians(gamma)))#EL sin se utiliza para calcular el seno de un angulo

        s = (a + b + c) / 2.0
   

    msg = f"--- RESULTADOS TRIÁNGULO OBLICUÁNGULO ---\n\n" \
          f"Lado a = {a:.2f}\nLado b = {b:.2f}\nLado c = {c:.2f}\n" \
          f"Ángulo A = {alpha:.2f}°\nÁngulo B = {beta:.2f}°\nÁngulo C = {gamma:.2f}°\n\n" \
         
    messagebox.showinfo("Solución Triángulo Oblicuángulo", msg)