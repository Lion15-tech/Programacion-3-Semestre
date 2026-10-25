import tkinter as tk
from tkinter import messagebox
from graficas import grafica_linea, grafica_linea2, resolver_2x2, resolver_3x3, resolver_trig_rectangulo, resolver_trig_oblicuangulo
icono = "cecyteq.ico"
def tecla_enter(event):
    #Obtiene el siguiente widget e el orden de tabulacion y le da el foco
    event.widget.tk_focusNext().focus()
    return "break" #Evita que el evento se propague o haga ruido por defecto

def abrir_ventana_opcion1():#VENTANA PARA LA OPCION 1
    root.withdraw()
    ventana_op1 = tk.Toplevel(root)
    ventana_op1.title("Opcion 1- Ecuacion Lineal")
    ventana_op1.geometry("350x350")
    ventana_op1.configure(bg="#A47148")
    def volver_menu():
        ventana_op1.destroy()
        root.deiconify() #Muestra nuevamente el menu
        #este es por s el usuario cierra con X en la ventana 
    ventana_op1.protocol("WM_DELETE_WINDOW", volver_menu)
    try:
        ventana_op1.iconbitmap(icono)
    except Exception:
        pass
    tk.Label(ventana_op1, text="Introduzca dos pares ordenados:", font=("Lucida Calligraphy", 14), bg= "#F7B7C4").pack()
    tk.Label(ventana_op1, text="Par ordenado 1", font=("Footlight MT Light", 12), bg="#F7B7C4").pack()
    e_x1 = tk.Entry(ventana_op1, width=20, bg="#FCEDB7")# es para el valor de (x)
    e_x1.pack(pady=5)
    e_y1 = tk.Entry(ventana_op1, width=20, bg="#FFF3C9")#es para el valor de (y)
    e_y1.pack(pady=5)
    tk.Label(ventana_op1, text=" Par Ordenado 2", font=("Footlight MT Light", 12), bg="#F7B7C4").pack()
    e_x2 = tk.Entry(ventana_op1,width=20, bg="#FFF3C9")
    e_x2.pack(pady=5)
    e_y2 = tk.Entry(ventana_op1, width=20, bg="#FFF3C9")
    e_y2.pack(pady=5)
    boton = tk.Button(
        ventana_op1, 
        text="Graficar", 
        font=("Arial", 11, "bold"), 
        bg="#FFF3C9", 
        fg="black",
        command=lambda: grafica_linea(e_x1.get(), e_y1.get(),e_x2.get(), e_y2.get(), ventana_op1)
    )
    boton.pack(pady=15)
   

    e_x1.bind("<Return>", tecla_enter)
    e_y1.bind("<Return>", tecla_enter)
    e_x2.bind("<Return>", tecla_enter)
    e_y2.bind("<Return>", tecla_enter)
    boton.bind("<Return>", lambda event: boton.invoke())
    e_x1.focus()
#VENTANA PARA LA OPCION 2
def abrir_ventana_opcion2():
    root.withdraw()
    ventana_op2 = tk.Toplevel(root)
    ventana_op2.title("Opcion 2.- Ecuaciones de Segundo Grado")
    ventana_op2.geometry("350x350")
    ventana_op2.configure(bg= "#A47148")
    def volver_menu1():
        ventana_op2.destroy()
        root.deiconify() #Muestra nuevamente el menu
            #este es por s el usuario cierra con X en la ventana 
    ventana_op2.protocol("WM_DELETE_WINDOW", volver_menu1)
    try:
        ventana_op2.iconbitmap(icono)
    except Exception:
        pass
    tk.Label(ventana_op2, text="Ecuacion de Segundo Grado: aX² + bX + c", font=("Footlight MT Light", 12), bg="#F7B7C4").pack(pady=15)
    tk.Label(ventana_op2, text="Valor de la constante -- a --", font=("Arial", 12), bg= "#F7B7C4").pack()
    entrada3 = tk.Entry(ventana_op2, width=12, bg="#FFF3C9")
    entrada3.pack(pady=5)
    tk.Label(ventana_op2, text="Valor de la Constante -- b --", font=("Arial", 12), bg="#F7B7C4").pack()
    entrada4 = tk.Entry(ventana_op2, width=12, bg="#FFF3C9")
    entrada4.pack(pady=5)
    tk.Label(ventana_op2, text="Valor de la Constante -- c--", font=("Arial", 12), bg= "#F7B7C4").pack()
    entrada5 = tk.Entry(ventana_op2, width=12, bg="#FFF3C9")
    entrada5.pack(pady=5)
    boton1 = tk.Button(
        ventana_op2, 
        text="Graficar", 
        font=("Arial", 14, "bold"), 
        bg="#FFF3C9", 
        fg="black",
        command=lambda: grafica_linea2(entrada3.get(), entrada4.get(),entrada5.get(),ventana_op2)
    )
    boton1.pack(pady=15)
    
    entrada3.bind("<Return>", tecla_enter)
    entrada4.bind("<Return>", tecla_enter)
    entrada5.bind("<Return>", tecla_enter)
    boton1.bind("<Return>",lambda event: boton1.invoke())
    #AQI ES PARA LA OPCION 3 
#Este es para las subventaas de cada opcion 2x2 y 3x3
def ventana_2x2(ventana_anterior): #Ventana para la opcion de 2x2
    ventana_anterior.withdraw()
    v_2x2 = tk.Toplevel(root)
    v_2x2.title("Sistema de 2x2")
    v_2x2.geometry("350x400")
    v_2x2.configure(bg="#A47148")
    try: 
        v_2x2.iconbitmap(icono)
    except Exception:
        pass
    def volver():
        v_2x2.destroy()
        ventana_anterior.deiconify()
    v_2x2.protocol("WM_DELETE_WINDOW", volver)
        
    tk.Label(v_2x2, text="Ecucaciones de 2x2",font=("Footlight MT Light", 25), bg="#F7B7C4").pack(pady=15)
    frame_input = tk.Frame(v_2x2, bg="#FFF3C9")
    frame_input.pack(pady=10)
     #Ecuacion 1:
    tk.Label(frame_input, text="Ecuacion 1:",font=("Footlight MT Light", 16), bg="#F7B7C4").grid(row=0, columnspan=6, sticky="w", pady=(5,2))
    e_a1 = tk.Entry(frame_input, width=7, bg= "#FFF3C9"); e_a1.grid(row=1, column=0)
    tk.Label(frame_input, text="X +", bg="#F7B7C4").grid(row=1, column=1)
    e_b1 = tk.Entry(frame_input, width=7, bg="#FFF3C9"); e_b1.grid(row=1, column=2)
    tk.Label(frame_input, text="Y = ", bg="#F7B7C4").grid(row=1, column=3)
    e_c1 = tk.Entry(frame_input, width=7, bg="#FFF3C9"); e_c1.grid(row = 1, column=4)
    #Para la ecuacion 2
    tk.Label(frame_input, text="Ecuacion 2:", font=("Footlight MT Light", 16), bg="#F7B7C4").grid(row=2, columnspan=6, sticky="w", pady=(10, 5))
    e_a2 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_a2.grid(row=3, column=0)
    tk.Label(frame_input, text="X +", bg="#F7B7C4").grid(row=3, column=1)
    e_b2 = tk.Entry(frame_input, width=7, bg="#FFF3C9"); e_b2.grid(row=3, column=2)
    tk.Label(frame_input, text= "Y =", bg="#F7B7C4").grid(row=3, column=3)
    e_c2 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_c2.grid(row=3, column=4)
    boton = tk.Button(
        v_2x2, 
        text="Graficar y Resolver", 
        font=("Arial", 13, "bold"),
        bg= "#FFF3C9", 
        fg="black", 
        command=lambda: resolver_2x2(e_a1.get(), e_b1.get(), e_c1.get(), e_a2.get(), e_b2.get(), e_c2.get(), v_2x2)
    )
    boton.pack(pady = 15)
 
    e_a1.bind("<Return>", tecla_enter)
    e_b1.bind("<Return>", tecla_enter)
    e_c1.bind("<Return>", tecla_enter)
    e_a2.bind("<Return>", tecla_enter)
    e_b2.bind("<Return>", tecla_enter)
    e_c2.bind("<Return>", tecla_enter)
    boton.bind("<Return>", lambda event: boton.invoke())
#Esta es para la ventan 3x3
def ventana_3x3(ventana_anterior):
    ventana_anterior.withdraw()
    v_3x3 = tk.Toplevel(root)
    v_3x3.title("Sistema de Ecuaciones 3x3")
    v_3x3.geometry("350x400")
    v_3x3.configure(bg="#A47148")
    def volver():
        v_3x3.destroy()
        ventana_anterior.deiconify()

    v_3x3.protocol("WM_DELETE_WINDOW", volver)
    try:
        v_3x3.iconbitmap(icono)
    except Exception:
        pass
   
    tk.Label(v_3x3, text="Ecuaciones de 3x3", font=("Arial", 16), bg="#F7B7C4").pack(pady=15)
    frame_input = tk.Frame(v_3x3, bg="#FFF3C9")
    frame_input.pack(pady=10)
    #Aqui es para la ecuacion 1
    tk.Label(frame_input, text="Ecuacion 1:", font=("Arial", 15)).grid(row=0, columnspan=6, sticky="w", pady=(5,2))
    e_a1 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_a1.grid(row=1, column=0)
    tk.Label(frame_input, text="X +", bg="#F7B7C4").grid(row=1, column=1)
    e_b1 = tk.Entry(frame_input, width=7, bg="#FFF3C9"); e_b1.grid(row=1, column=2)
    tk.Label(frame_input, text=" Y +", bg="#F7B7C4").grid(row=1, column=3)
    e_c1 = tk.Entry(frame_input, width=7, bg="#FFF3C9"); e_c1.grid(row=1, column=4)
    tk.Label(frame_input, text= " Z =", bg="#F7B7C4").grid(row=1, column=5)
    e_d1 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_d1.grid(row=1, column=6)
    #Para la ecuacion 2
    tk.Label(frame_input, text="Ecuacion 2:", font = ("Arial", 15)).grid(row=2, columnspan=7, sticky="w", pady=(8, 2))
    e_a2 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_a2.grid(row=3, column= 0)
    tk.Label(frame_input, text="X  +", bg="#F7B7C4").grid(row= 3, column=1)
    e_b2 = tk.Entry(frame_input, width=7,bg = "#FFF3C9") ; e_b2.grid(row= 3, column=2)
    tk.Label(frame_input, text=" Y + ",  bg="#F7B7C4").grid(row=3 , column=3 )
    e_c2 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_c2.grid(row=3 , column=4 )
    tk.Label(frame_input, text="Z = ",bg="#F7B7C4").grid(row =3, column= 5)
    e_d2= tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_d2.grid(row= 3, column=6)
    #PARA LA ECUACION 3
    tk.Label(frame_input, text="Ecuacion 3:", font=("Arial", 15)).grid(row= 4, columnspan=7, sticky="w", pady=(8, 2))
    e_a3 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_a3.grid(row=5, column=0)
    tk.Label(frame_input, text="X +", bg= "#F7B7C4").grid(row=5, column=1)
    e_b3 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_b3.grid(row=5, column=2)
    tk.Label(frame_input, text= " Y + ", bg="#F7B7C4").grid(row=5, column=1)
    e_c3 = tk.Entry(frame_input, width=7, bg="#FFF3C9"); e_c3.grid(row=5, column=4)
    tk.Label(frame_input, text=" Z = ",bg="#F7B7C4").grid(row=5, column=5)
    e_d3 = tk.Entry(frame_input, width=7, bg="#FFF3C9") ; e_d3.grid(row=5, column=6)
    boton1 = tk.Button(
        v_3x3, 
        text= "Graficar y resolver", 
        font=("Arial", 12 ,"bold"),
        bg="#F7B7C4",
        fg="black", 
        command=lambda : resolver_3x3
        ( e_a1.get(), e_b1.get(), e_c1.get(), e_d1.get(), 
        e_a2.get(), e_b2.get(), e_c2.get(), e_d2.get(),
        e_a3.get(), e_b3.get(), e_c3.get(), e_d3.get(), 
        v_3x3
        )
    )
    boton1.pack(pady=7)
    tk.Button(v_3x3, text="Volver al menu", command=volver, font=("Arial", 13), bg="#F7B7C4").pack()
    e_a1.bind("<Return>", tecla_enter)
    e_b1.bind("<Return>", tecla_enter)
    e_c1.bind("<Return>", tecla_enter)
    e_d1.bind("<Return>", tecla_enter)
    e_a2.bind("<Return>", tecla_enter)
    e_b2.bind("<Return>", tecla_enter)
    e_c2.bind("<Return>", tecla_enter)
    e_d2.bind("<Return>", tecla_enter)
    e_a3.bind("<Return>", tecla_enter)
    e_b3.bind("<Return>", tecla_enter)
    e_c3.bind("<Return>", tecla_enter)
    e_d3.bind("<Return>", tecla_enter)
    boton1.bind("<Return>", lambda event : boton1.invoke())
#SUBMENU DE SISTEMA DE ECUACIONES
def abrir_submenu():
    root.withdraw()
    submenu1= tk.Toplevel(root)
    submenu1.title("sistema de ecuaciones")
    submenu1.geometry("350x350")
    submenu1.configure(bg="#A47148")
    def volver_menu2():
        submenu1.destroy()
        root.deiconify() #Muestra nuevamente el menu
            #este es por s el usuario cierra con X en la ventana 
    submenu1.protocol("WM_DELETE_WINDOW", volver_menu2)
    try:
        submenu1.iconbitmap(icono)
    except Exception:
        pass
    tk.Label(submenu1, text="Submenu de Ecuaciones", font=("Footlight MT Light", 14), width=30 ,bg="#F7B7C4").pack(pady=10)
    tk.Button(submenu1, text="Ecuaciones de 2x2", width=28, font=("Arial", 13), bg= "#FFF3C9", command=lambda : ventana_2x2(submenu1)).pack(pady=8)
    tk.Button(submenu1, text="Ecuaciones de 3x3", width=28, font=("Arial", 13), background= "#FFF3C9", command= lambda : ventana_3x3(submenu1)).pack(pady=8)
    tk.Button(submenu1, text= "Volver", command=volver_menu2, font=("Arial", 13), bg="#F7B7C4" ).pack()
   




def form_trig_rectangulo(modo, ventana_anterior):
    ventana_anterior.withdraw()
    v_form = tk.Toplevel(root)
    v_form.geometry("380x360")
    v_form.configure(bg="#A47148")

    def volver5():
        v_form.destroy()
        ventana_anterior.deiconify()
    v_form.protocol("WM_DELETE_WINDOW", volver5)
    try:
        v_form.iconbitmap(icono)
    except Exception:
        pass

    titulos = {1: "Caso 1: Dos Catetos (a y b)", 2: "Caso 2: Cateto (a) e Hipotenusa (c)", 3: "Caso 3: Cateto (a) y Ángulo A"}
    lbl_v1 = {1: "Cateto a:", 2: "Cateto a:", 3: "Cateto a:"}
    lbl_v2 = {1: "Cateto b:", 2: "Hipotenusa c:", 3: "Ángulo A (°):"}

    v_form.title(titulos[modo])
    tk.Label(v_form, text=titulos[modo], font=("Footlight MT Light", 14, "bold"), bg="#F7B7C4").pack(pady=15)

    f_in = tk.Frame(v_form, bg="#A47148")
    f_in.pack(pady=10)

    tk.Label(f_in, text=lbl_v1[modo], font=("Arial", 11, "bold"), bg="#A47148", fg="white").grid(row=0, column=0, pady=5, sticky="e")
    e_val1 = tk.Entry(f_in, width=12, bg="#FFF3C9"); e_val1.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(f_in, text=lbl_v2[modo], font=("Arial", 11, "bold"), bg="#A47148", fg="white").grid(row=1, column=0, pady=5, sticky="e")
    e_val2 = tk.Entry(f_in, width=12, bg="#FFF3C9"); e_val2.grid(row=1, column=1, pady=5, padx=5)

    boton = tk.Button(
        v_form, text="Calcular", font=("Arial", 12, "bold"), bg="#FFF3C9", fg="black",
        command=lambda: resolver_trig_rectangulo(modo, e_val1.get(), e_val2.get())
    )
    boton.pack(pady=20)

    tk.Button(v_form, text="Volver", command=volver5, font=("Arial", 11), bg="#F7B7C4").pack()
    e_val1.bind("<Return>", tecla_enter)
    e_val2.bind("<Return>", tecla_enter)
    boton.bind("<Return>", lambda event : boton.invoke() )



def ventana_triangulo_rectangulo(ventana_anterior):
    ventana_anterior.withdraw()
    v_rect = tk.Toplevel(root)
    v_rect.title("Triángulo Rectángulo")
    v_rect.geometry("380x360")
    v_rect.configure(bg="#A47148")

    def volver():
        v_rect.destroy()
        ventana_anterior.deiconify()

    v_rect.protocol("WM_DELETE_WINDOW", volver)
    try:
        v_rect.iconbitmap(icono)
    except Exception:
        pass

    tk.Label(v_rect, text="Triángulo Rectángulo", font=("Footlight MT Light", 16, "bold"), bg="#F7B7C4").pack(pady=15)
    tk.Label(v_rect, text="Seleccione los datos que posee:", font=("Arial", 11), bg="#A47148", fg="white").pack(pady=5)

    tk.Button(v_rect, text="1. Dos Catetos (a y b)", width=30, font=("Arial", 11), bg="#FFF3C9", command=lambda: form_trig_rectangulo(1, v_rect)).pack(pady=8)
    tk.Button(v_rect, text="2. Cateto (a) e Hipotenusa (c)", width=30, font=("Arial", 11), bg="#FFF3C9", command=lambda: form_trig_rectangulo(2, v_rect)).pack(pady=8)
    tk.Button(v_rect, text="3. Cateto (a) y Ángulo Agudo (A)", width=30, font=("Arial", 11), bg="#FFF3C9", command=lambda: form_trig_rectangulo(3, v_rect)).pack(pady=8)
    tk.Button(v_rect, text="Volver", command=volver, width=30, font=("Arial", 11), bg="#F7B7C4").pack(pady=12)


# VENTANA DE TRAINGULO OBLICUANGULO
def form_trig_oblicuangulo(modo, ventana_anterior):
    ventana_anterior.withdraw()
    v_form = tk.Toplevel(root)
    v_form.geometry("380x380")
    v_form.configure(bg="#A47148")

    def volver():
        v_form.destroy()
        ventana_anterior.deiconify()

    v_form.protocol("WM_DELETE_WINDOW", volver)
    try:
        v_form.iconbitmap(icono)
    except Exception:
        pass
    titulos = {1: "Caso 1: Tres Lados (a, b, c)", 2: "Caso 2: LAL (a, b y Ángulo C)", 3: "Caso 3: ALA (Ángulo A, B y Lado c)"}
    lbl_v1 = {1: "Lado a:", 2: "Lado a:", 3: "Ángulo A (°):"}
    lbl_v2 = {1: "Lado b:", 2: "Lado b:", 3: "Ángulo B (°):"}
    lbl_v3 = {1: "Lado c:", 2: "Ángulo C (°):", 3: "Lado c:"}

    v_form.title(titulos[modo])
    tk.Label(v_form, text=titulos[modo], font=("Footlight MT Light", 14, "bold"), bg="#F7B7C4").pack(pady=15)

    f_in = tk.Frame(v_form, bg="#A47148")
    f_in.pack(pady=10)

    tk.Label(f_in, text=lbl_v1[modo], font=("Arial", 11, "bold"), bg="#A47148", fg="white").grid(row=0, column=0, pady=5, sticky="e")
    e_val1 = tk.Entry(f_in, width=12, bg="#FFF3C9"); e_val1.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(f_in, text=lbl_v2[modo], font=("Arial", 11, "bold"), bg="#A47148", fg="white").grid(row=1, column=0, pady=5, sticky="e")
    e_val2 = tk.Entry(f_in, width=12, bg="#FFF3C9"); e_val2.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(f_in, text=lbl_v3[modo], font=("Arial", 11, "bold"), bg="#A47148", fg="white").grid(row=2, column=0, pady=5, sticky="e")
    e_val3 = tk.Entry(f_in, width=12, bg="#FFF3C9"); e_val3.grid(row=2, column=1, pady=5, padx=5)

    boton = tk.Button(
        v_form, text="Calcular", font=("Arial", 12, "bold"), bg="#FFF3C9", fg="black",
        command=lambda: resolver_trig_oblicuangulo(modo, e_val1.get(), e_val2.get(), e_val3.get())
    )
    boton.pack(pady=20)

    tk.Button(v_form, text="Volver", command=volver, font=("Arial", 11), bg="#F7B7C4").pack()
    e_val1.bind("<Return>", tecla_enter)
    e_val2.bind("<Return>", tecla_enter)
    e_val3.bind("<Return>", tecla_enter)
    boton.bind("<Return>", lambda event : boton.invoke())


def ventana_triangulo_oblicuangulo(ventana_anterior):
    ventana_anterior.withdraw()
    v_oblic = tk.Toplevel(root)
    v_oblic.title("Triángulo Oblicuángulo")
    v_oblic.geometry("380x360")
    v_oblic.configure(bg="#A47148")

    def volver():
        v_oblic.destroy()
        ventana_anterior.deiconify()

    v_oblic.protocol("WM_DELETE_WINDOW", volver)
    try:
        v_oblic.iconbitmap(icono)
    except Exception:
        pass

    tk.Label(v_oblic, text="Triángulo Oblicuángulo", font=("Footlight MT Light", 16, "bold"), bg="#F7B7C4").pack(pady=15)
    tk.Label(v_oblic, text="Seleccione los datos que posee:", font=("Arial", 11), bg="#A47148", fg="white").pack(pady=5)

    tk.Button(v_oblic, text="1. Tres Lados (a, b, c)", width=30, font=("Arial", 11), bg="#FFF3C9", command=lambda: form_trig_oblicuangulo(1, v_oblic)).pack(pady=8)
    tk.Button(v_oblic, text="2. LAL (a, b y Ángulo C)", width=30, font=("Arial", 11), bg="#FFF3C9", command=lambda: form_trig_oblicuangulo(2, v_oblic)).pack(pady=8)
    tk.Button(v_oblic, text="3. ALA (Ángulo A, B y Lado c)", width=30, font=("Arial", 11), bg="#FFF3C9", command=lambda: form_trig_oblicuangulo(3, v_oblic)).pack(pady=8)
    tk.Button(v_oblic, text="Volver", command=volver, width=30, font=("Arial", 11), bg="#F7B7C4").pack(pady=12)
#SUBMENU DE TRIGONOMETRIA
def trigonometria_submenu():
    root.withdraw()
    sub_trig = tk.Toplevel(root)
    sub_trig.title("Trigonometría")
    sub_trig.geometry("350x350")
    sub_trig.configure(bg="#A47148")

    def volver_menu_principal():
        sub_trig.destroy()
        root.deiconify()

    sub_trig.protocol("WM_DELETE_WINDOW", volver_menu_principal)
    try:
        sub_trig.iconbitmap(icono)
    except Exception:
        pass

    tk.Label(sub_trig, text="Menú de Trigonometría", font=("Footlight MT Light", 15, "bold"), width=28, bg="#F7B7C4").pack(pady=15)
    tk.Button(sub_trig, text="Triángulo rectángulo", width=28, font=("Arial", 13), bg="#FFF3C9", command=lambda: ventana_triangulo_rectangulo(sub_trig)).pack(pady=10)
    tk.Button(sub_trig, text="Triángulo oblicuángulo", width=28, font=("Arial", 13), bg="#FFF3C9", command=lambda: ventana_triangulo_oblicuangulo(sub_trig)).pack(pady=10)
    tk.Button(sub_trig, text="Volver al Menú Principal", width=28, font=("Arial", 12), bg="#F7B7C4", command=volver_menu_principal).pack(pady=15)






root = tk.Tk()
root.title("Menu de Ecuaciones")
root.geometry("350x350")
root.configure(background= "#A47148")
try:
    root.iconbitmap(icono)
except Exception:
    pass
tk.Label(root, text="MENU DE OPCIONES", width=30, font=("Footlight MT Light", 15), background="#F7B7C4").pack(pady=10)
tk.Button(root,text="1.-Ecuaciones de Primer Grado", width=28, font=("Arial",13),command=abrir_ventana_opcion1, bg="#FFF3C9").pack(pady=8)
tk.Button(root, text="2.- Ecuaciones de Segundo grado", width=28, font=("Arial", 13),command= abrir_ventana_opcion2,bg="#FFF3C9").pack(pady=8)
tk.Button(root, text="3.- Sistema de ecuaciones", width=28, font=("Arial", 13), command=abrir_submenu,bg="#FFF3C9").pack(pady=8)
tk.Button(root, text="4 .- Trigonometria", width=28,font=("Arial", 13), bg="#FFF3C9", command= trigonometria_submenu).pack(pady=8)
tk.Button(root, text="5.- Salir ", width=28,font=("Arial", 13), bg="#FFF3C9", command=root.destroy).pack(pady=8)
root.mainloop()
