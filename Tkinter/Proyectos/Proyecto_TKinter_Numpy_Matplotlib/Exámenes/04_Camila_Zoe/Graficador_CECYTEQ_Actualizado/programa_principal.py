import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from grafica_primer_grado import calcular_primer_grado
from grafica_segundo_grado import calcular_segundo_grado
from sistema_2x2 import calcular_2x2
from sistema_3x3 import calcular_3x3

ventana = tk.Tk()
ventana.title("Graficador de ecuaciones - CECYTEQ")
ventana.geometry("1100x700")
ventana.minsize(900, 600)
try:
    ventana.iconbitmap("cecyteq.ico")
except Exception:
    pass

contenedor = tk.Frame(ventana, padx=10, pady=10)
contenedor.pack(fill="both", expand=True)
campos = []
grafica = canvas = etiqueta_resultado = panel_entradas = panel_grafica = None

def limpiar():
    global campos, grafica, canvas, etiqueta_resultado, panel_entradas, panel_grafica
    for widget in contenedor.winfo_children(): widget.destroy()
    campos = []; grafica = canvas = etiqueta_resultado = panel_entradas = panel_grafica = None

def preparar(titulo, formula):
    global grafica, canvas, panel_entradas, panel_grafica, etiqueta_resultado
    limpiar()
    panel_entradas = tk.Frame(contenedor, padx=10, pady=10); panel_entradas.pack(side="left", fill="y")
    panel_grafica = tk.Frame(contenedor); panel_grafica.pack(side="right", fill="both", expand=True)
    tk.Label(panel_entradas, text=titulo, font=("Arial",15,"bold"), wraplength=300).pack(pady=(0,8))
    tk.Label(panel_entradas, text=formula, font=("Arial",11)).pack(pady=(0,10))
    grafica = Figure(figsize=(6.5,5.3), dpi=100)
    canvas = FigureCanvasTkAgg(grafica, master=panel_grafica); canvas.get_tk_widget().pack(fill="both", expand=True)
    etiqueta_resultado = tk.Label(panel_entradas, text="", justify="left", anchor="w", wraplength=300, font=("Arial",10))
    etiqueta_resultado.pack(fill="x", pady=10)

def mover_siguiente(event, caja):
    """Enter mueve al siguiente Entry; en el último campo activa el botón de cálculo."""
    try:
        posicion = campos.index(caja)
        if posicion + 1 < len(campos):
            campos[posicion + 1].focus_set()
        else:
            for widget in panel_entradas.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.invoke()
                    break
    except (ValueError, AttributeError):
        pass
    return "break"

def entrada(nombre, valor=""):
    fila = tk.Frame(panel_entradas); fila.pack(fill="x", pady=3)
    tk.Label(fila, text=nombre, width=8, anchor="w").pack(side="left")
    caja = tk.Entry(fila, width=12); 
    if valor != "":
        caja.insert(0, str(valor))
    caja.pack(side="left"); campos.append(caja)
    caja.bind("<Return>", lambda evento, c=caja: mover_siguiente(evento, c))
    caja.bind("<KP_Enter>", lambda evento, c=caja: mover_siguiente(evento, c))

def boton_graficar(funcion):
    tk.Button(panel_entradas, text="Graficar y calcular valores", command=funcion, bg="#167447", fg="white", padx=8, pady=5).pack(pady=8, fill="x")

def numeros():
    try: return [float(c.get()) for c in campos]
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Escribe números válidos en todos los campos."); return None

def dibujar_ejes(ax, titulo):
    ax.axhline(0, color="black", linewidth=.8); ax.axvline(0, color="black", linewidth=.8)
    ax.grid(True, linestyle="--", alpha=.45); ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_title(titulo); ax.legend(loc="best")

def primer_grado():
    preparar("Ecuación de primer grado", "y = ax + b"); entrada("a =",2); entrada("b =",-4); boton_graficar(calcular_p1); calcular_p1()

def calcular_p1():
    v=numeros()
    if v is None:return
    a,b=v; x,y,d=calcular_primer_grado(a,b); grafica.clear(); ax=grafica.add_subplot(111); ax.plot(x,y,label=f"y = {a:g}x + {b:g}"); ax.scatter([0],[b],label="Corte con Y")
    texto=f"Pendiente (a): {a:g}\nCorte con eje Y: (0, {b:g})"
    if d["raiz"] is not None: ax.scatter([d["raiz"]],[0],label="Raíz"); texto+=f"\nRaíz / corte con X: ({d['raiz']:.3g}, 0)"
    else: texto+="\nLa recta es horizontal."
    dibujar_ejes(ax,"Gráfica de primer grado"); canvas.draw(); etiqueta_resultado.config(text=texto)

def segundo_grado():
    preparar("Ecuación de segundo grado", "y = ax² + bx + c"); entrada("a =",1); entrada("b =",-2); entrada("c =",-3); boton_graficar(calcular_p2); calcular_p2()

def calcular_p2():
    v=numeros()
    if v is None:return
    try:x,y,d=calcular_segundo_grado(*v)
    except ValueError as e: messagebox.showerror("Error",str(e)); return
    a,b,c=v; grafica.clear(); ax=grafica.add_subplot(111); ax.plot(x,y,label=f"y = {a:g}x² + {b:g}x + {c:g}"); xv,yv=d["vertice"]; ax.scatter([xv],[yv],label="Vértice"); ax.scatter([0],[c],label="Corte con Y")
    texto=f"Vértice: ({xv:.3g}, {yv:.3g})\nEje de simetría: x = {xv:.3g}\nCorte con Y: (0, {c:g})\nDiscriminante: {d['discriminante']:.3g}"
    if len(d["raices"])==2: ax.scatter(d["raices"],[0],label="Raíces"); texto+=f"\nRaíces: x₁ = {d['raices'][0]:.3g}, x₂ = {d['raices'][1]:.3g}"
    elif len(d["raices"])==1: ax.scatter(d["raices"],[0],label="Raíz doble"); texto+=f"\nRaíz doble: x = {d['raices'][0]:.3g}"
    else: texto+="\nNo tiene raíces reales."
    texto+="\nApertura: "+("hacia arriba" if a>0 else "hacia abajo"); dibujar_ejes(ax,"Gráfica de segundo grado"); canvas.draw(); etiqueta_resultado.config(text=texto)

def sistema_2x2():
    preparar("Sistema de ecuaciones 2x2", "a₁x + b₁y = c₁\na₂x + b₂y = c₂")
    for n,val in [("a1 =",1),("b1 =",1),("c1 =",4),("a2 =",1),("b2 =",-1),("c2 =",2)]: entrada(n,val)
    boton_graficar(calcular_s); calcular_s()

def calcular_s():
    v=numeros()
    if v is None:return
    a1,b1,c1,a2,b2,c2=v; A,B,det,sol,tipo=calcular_2x2(*v); grafica.clear(); ax=grafica.add_subplot(111); x=np.linspace(-10,10,400)
    for a,b,c,label in [(a1,b1,c1,"Ecuación 1"),(a2,b2,c2,"Ecuación 2")]:
        if abs(b)>1e-12: ax.plot(x,(c-a*x)/b,label=label)
        elif abs(a)>1e-12: ax.axvline(c/a,label=label)
    texto=f"Determinante: {det:.3g}\n{tipo}."
    if sol is not None: ax.scatter([sol[0]],[sol[1]],s=65,label="Intersección"); texto+=f"\nx = {sol[0]:.3g}\ny = {sol[1]:.3g}"
    ax.set_xlim(-10,10); ax.set_ylim(-10,10); dibujar_ejes(ax,"Sistema de ecuaciones 2x2"); canvas.draw(); etiqueta_resultado.config(text=texto)

def sistema_3x3():
    preparar("Sistema de ecuaciones 3x3", "a₁x + b₁y + c₁z = d₁")
    for n,val in [("a1 =",1),("b1 =",1),("c1 =",1),("d1 =",6),("a2 =",1),("b2 =",-1),("c2 =",2),("d2 =",5),("a3 =",2),("b3 =",1),("c3 =",-1),("d3 =",1)]: entrada(n,val)
    boton_graficar(calcular_s3); calcular_s3()

def calcular_s3():
    v=numeros()
    if v is None:return
    A,B,det,sol,tipo=calcular_3x3(v); grafica.clear(); ax=grafica.add_subplot(111,projection="3d"); texto=f"Determinante: {det:.3g}\n{tipo}."
    xx,yy=np.meshgrid(np.linspace(-5,5,18),np.linspace(-5,5,18))
    for i in range(3):
        a,b,c,d=v[i*4:i*4+4]
        if abs(c)>1e-12: zz=(d-a*xx-b*yy)/c; ax.plot_surface(xx,yy,zz,alpha=.25)
    if sol is not None: ax.scatter([sol[0]],[sol[1]],[sol[2]],s=70,label="Solución"); texto+=f"\nx = {sol[0]:.3g}\ny = {sol[1]:.3g}\nz = {sol[2]:.3g}"
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z"); ax.set_title("Sistema de ecuaciones 3x3"); canvas.draw(); etiqueta_resultado.config(text=texto)


def trig_rectangulo():
    preparar("Trigonometría: triángulo rectángulo",
             "Ingresa datos conocidos. Usa lados a, b, c (c es hipotenusa) y ángulos A, B. C = 90°.")
    for n in ["Cateto a =", "Cateto b =", "Hipotenusa c =", "Ángulo A =", "Ángulo B ="]:
        entrada(n, "")
    tk.Label(panel_entradas, text="Deja en blanco los datos que no conozcas. Escribe al menos dos datos compatibles.",
             wraplength=300, justify="left").pack(pady=5)
    boton_graficar(calcular_trig_rectangulo)

def calcular_trig_rectangulo():
    import math
    try:
        vals = [float(c.get()) if c.get().strip() else None for c in campos]
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Usa números válidos o deja en blanco los datos desconocidos."); return
    a,b,c,A,B = vals
    known_sides = [x for x in (a,b,c) if x is not None]
    known_angles = [x for x in (A,B) if x is not None]
    if any(x <= 0 for x in known_sides):
        messagebox.showerror("Dato incorrecto", "Los lados deben ser mayores que cero."); return
    if any(x <= 0 or x >= 90 for x in known_angles):
        messagebox.showerror("Dato incorrecto", "Los ángulos A y B deben estar entre 0° y 90°."); return
    if len(known_sides) + len(known_angles) < 2:
        messagebox.showerror("Faltan datos", "Ingresa al menos dos datos conocidos."); return
    # Resolver mediante iteraciones usando Pitágoras y razones trigonométricas.
    for _ in range(8):
        if A is not None and B is None: B = 90-A
        if B is not None and A is None: A = 90-B
        if A is not None and B is not None and abs(A+B-90) > 1e-5:
            messagebox.showerror("Datos incompatibles", "En un triángulo rectángulo A + B debe ser 90°."); return
        if a is not None and b is not None:
            c = math.hypot(a,b)
        if a is not None and c is not None:
            if c <= a: messagebox.showerror("Datos incompatibles", "La hipotenusa debe ser mayor que cada cateto."); return
            b = math.sqrt(max(0,c*c-a*a))
        if b is not None and c is not None:
            if c <= b: messagebox.showerror("Datos incompatibles", "La hipotenusa debe ser mayor que cada cateto."); return
            a = math.sqrt(max(0,c*c-b*b))
        if A is not None:
            if a is not None: b = a / math.tan(math.radians(A))
            if b is not None: a = b * math.tan(math.radians(A))
            if a is not None: c = a / math.sin(math.radians(A))
            if c is not None: a = c * math.sin(math.radians(A))
            if b is not None: c = b / math.cos(math.radians(A))
            if c is not None: b = c * math.cos(math.radians(A))
        if B is not None:
            if b is not None: a = b / math.tan(math.radians(B))
            if a is not None: b = a * math.tan(math.radians(B))
            if b is not None: c = b / math.sin(math.radians(B))
            if c is not None: b = c * math.sin(math.radians(B))
            if a is not None: c = a / math.cos(math.radians(B))
            if c is not None: a = c * math.cos(math.radians(B))
    if any(x is None or not math.isfinite(x) or x <= 0 for x in (a,b,c)):
        messagebox.showerror("Faltan datos", "Con esos datos no se puede determinar el triángulo. Prueba con dos lados o un lado y un ángulo."); return
    A = math.degrees(math.atan2(a,b)); B = 90-A
    for caja, valor in zip(campos, [a,b,c,A,B]):
        caja.delete(0,"end"); caja.insert(0,f"{valor:.6g}")
    grafica.clear(); ax=grafica.add_subplot(111)
    ax.plot([0,b,0,0],[0,0,a,0], marker="o", label="Triángulo rectángulo")
    ax.set_aspect("equal", adjustable="datalim"); ax.grid(True); ax.legend()
    ax.set_title("Triángulo rectángulo"); canvas.draw()
    etiqueta_resultado.config(text=f"a = {a:.5g}\\nb = {b:.5g}\\nc = {c:.5g}\\nA = {A:.5g}°\\nB = {B:.5g}°\\nC = 90°")

def trig_oblicuangulo():
    preparar("Trigonometría: triángulo oblicuángulo",
             "Ingresa tres datos compatibles: lados a, b, c y ángulos A, B, C. Los ángulos suman 180°.")
    for n in ["Lado a =", "Lado b =", "Lado c =", "Ángulo A =", "Ángulo B =", "Ángulo C ="]:
        entrada(n, "")
    tk.Label(panel_entradas, text="Deja en blanco lo que no conozcas. Se aceptan casos SSS, SAS, ASA y AAS.",
             wraplength=300, justify="left").pack(pady=5)
    boton_graficar(calcular_trig_oblicuo)

def calcular_trig_oblicuo():
    import math
    try:
        v = [float(c.get()) if c.get().strip() else None for c in campos]
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Usa números válidos o deja en blanco los datos desconocidos."); return
    a,b,c,A,B,C = v
    lados=[x for x in (a,b,c) if x is not None]
    angulos=[x for x in (A,B,C) if x is not None]
    if any(x <= 0 for x in lados):
        messagebox.showerror("Dato incorrecto", "Los lados deben ser mayores que cero."); return
    if any(x <= 0 or x >= 180 for x in angulos):
        messagebox.showerror("Dato incorrecto", "Cada ángulo debe estar entre 0° y 180°."); return
    if len(lados)+len(angulos)<3:
        messagebox.showerror("Faltan datos", "Ingresa al menos tres datos compatibles."); return
    if len(angulos)>=2:
        if A is not None and B is not None: C=180-A-B
        elif A is not None and C is not None: B=180-A-C
        elif B is not None and C is not None: A=180-B-C
        if any(x is not None and x <= 0 for x in (A,B,C)):
            messagebox.showerror("Datos incompatibles", "La suma de dos ángulos debe ser menor que 180°."); return
    # Ley de senos
    pairs=[(a,A),(b,B),(c,C)]
    known=[(s,ang) for s,ang in pairs if s is not None and ang is not None]
    if known:
        ratio=known[0][0]/math.sin(math.radians(known[0][1]))
        if a is None and A is not None: a=ratio*math.sin(math.radians(A))
        if b is None and B is not None: b=ratio*math.sin(math.radians(B))
        if c is None and C is not None: c=ratio*math.sin(math.radians(C))
    # Ley de cosenos con dos lados y el ángulo comprendido
    if a is not None and b is not None and C is not None and c is None:
        c=math.sqrt(max(0,a*a+b*b-2*a*b*math.cos(math.radians(C))))
    if a is not None and c is not None and B is not None and b is None:
        b=math.sqrt(max(0,a*a+c*c-2*a*c*math.cos(math.radians(B))))
    if b is not None and c is not None and A is not None and a is None:
        a=math.sqrt(max(0,b*b+c*c-2*b*c*math.cos(math.radians(A))))
    # SSS: obtener ángulos
    if all(x is not None for x in (a,b,c)):
        if a+b<=c or a+c<=b or b+c<=a:
            messagebox.showerror("Datos incompatibles", "Los lados no cumplen la desigualdad triangular."); return
        A=math.degrees(math.acos(max(-1,min(1,(b*b+c*c-a*a)/(2*b*c)))))
        B=math.degrees(math.acos(max(-1,min(1,(a*a+c*c-b*b)/(2*a*c)))))
        C=180-A-B
    # Recalcular lados por ley de senos una vez conocidos los ángulos
    if all(x is not None for x in (A,B,C)) and any(x is not None for x in (a,b,c)):
        ref=next((s/math.sin(math.radians(ang)) for s,ang in [(a,A),(b,B),(c,C)] if s is not None and ang is not None),None)
        if ref:
            if a is None:a=ref*math.sin(math.radians(A))
            if b is None:b=ref*math.sin(math.radians(B))
            if c is None:c=ref*math.sin(math.radians(C))
    if any(x is None for x in (a,b,c,A,B,C)):
        messagebox.showerror("Datos insuficientes", "No se pudo determinar el triángulo. Usa SSS, SAS, ASA o AAS con datos compatibles."); return
    if abs(A+B+C-180)>1e-3 or min(a,b,c)<=0:
        messagebox.showerror("Datos incompatibles", "Revisa los lados y ángulos; los ángulos deben sumar 180°."); return
    for caja,valor in zip(campos,[a,b,c,A,B,C]):
        caja.delete(0,"end"); caja.insert(0,f"{valor:.6g}")
    # Dibujar con c como base, coordenadas calculadas por ley de cosenos
    xx=(b*b+c*c-a*a)/(2*c); yy=math.sqrt(max(0,b*b-xx*xx))
    grafica.clear(); ax=grafica.add_subplot(111)
    ax.plot([0,c,xx,0],[0,0,yy,0],marker="o",label="Triángulo oblicuángulo")
    ax.set_aspect("equal",adjustable="datalim"); ax.grid(True); ax.legend(); ax.set_title("Triángulo oblicuángulo"); canvas.draw()
    etiqueta_resultado.config(text=f"a = {a:.5g}\\nb = {b:.5g}\\nc = {c:.5g}\\nA = {A:.5g}°\\nB = {B:.5g}°\\nC = {C:.5g}°")


def inicio():
    limpiar(); tk.Label(contenedor,text="GRAFICADOR DE ECUACIONES",font=("Arial",24,"bold")).pack(pady=(130,15)); tk.Label(contenedor,text="CECYTEQ · Selecciona una opción del menú Ecuaciones.",font=("Arial",13)).pack(); tk.Label(contenedor,text="Cada opción muestra su gráfica y los valores clave.",font=("Arial",11)).pack(pady=8)

menu_trig=tk.Menu(barra if 'barra' in globals() else ventana, tearoff=0)
menu_trig.add_command(label="Triángulo rectángulo", command=trig_rectangulo)
menu_trig.add_command(label="Triángulo oblicuángulo", command=trig_oblicuangulo)

barra=tk.Menu(ventana); ventana.config(menu=barra)
menu_archivo=tk.Menu(barra,tearoff=0); menu_archivo.add_command(label="Inicio",command=inicio); menu_archivo.add_separator(); menu_archivo.add_command(label="Salir",command=ventana.destroy); barra.add_cascade(label="Archivo",menu=menu_archivo)
menu_ecuaciones=tk.Menu(barra,tearoff=0); menu_ecuaciones.add_command(label="Gráfica de primer grado",command=primer_grado); menu_ecuaciones.add_command(label="Gráfica de segundo grado",command=segundo_grado)
menu_sistemas=tk.Menu(menu_ecuaciones,tearoff=0); menu_sistemas.add_command(label="Sistemas de 2x2",command=sistema_2x2); menu_sistemas.add_command(label="Sistemas de 3x3",command=sistema_3x3); menu_ecuaciones.add_cascade(label="Sistema de ecuaciones",menu=menu_sistemas); barra.add_cascade(label="Ecuaciones",menu=menu_ecuaciones); barra.add_cascade(label="Trigonometría", menu=menu_trig)
inicio(); ventana.mainloop()
