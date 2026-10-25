import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Ventana principal
v = tk.Tk()
v.title("CECYTEQ - Matemáticas")
v.geometry("700x650")

try:
    v.iconbitmap("cecyteq.ico")
except:
    pass

c_f, cnv = None, None

def reset():
    global c_f, cnv
    if c_f: c_f.destroy()
    if cnv: cnv.get_tk_widget().destroy()
    c_f = tk.Frame(v)
    c_f.pack(pady=10)

def plot(fig):
    global cnv
    if cnv: cnv.get_tk_widget().destroy()
    cnv = FigureCanvasTkAgg(fig, v)
    cnv.get_tk_widget().pack(fill="both", expand=True)

# 1. Ecuación de Primer Grado
def p_grado():
    reset()
    tk.Label(c_f, text="Ecuación de 1er Grado: y = m*x + b", font=("Arial", 10, "bold")).pack(pady=5)
    
    f = tk.Frame(c_f)
    f.pack()
    tk.Label(f, text="m:").grid(row=0, column=0)
    em = tk.Entry(f, width=8); em.insert(0, "2"); em.grid(row=0, column=1, padx=5)
    tk.Label(f, text="b:").grid(row=0, column=2)
    eb = tk.Entry(f, width=8); eb.insert(0, "1"); eb.grid(row=0, column=3, padx=5)
    
    lbl_res = tk.Label(c_f, text="", font=("Arial", 9), justify="left")
    lbl_res.pack(pady=5)

    def run():
        try:
            m, b = float(em.get()), float(eb.get())
            x = np.linspace(-10, 10, 100)
            y = m * x + b
            
            y_intercept = (0, b)
            x_intercept_str = ""
            x_int = None
            if m != 0:
                x_int = -b / m
                x_intercept_str = f"({x_int:.2f}, 0)"
            else:
                x_intercept_str = "No cruza el eje X (Pendiente m=0)"
            
            lbl_res.config(
                text=f"• Pendiente (m): {m}\n"
                     f"• Ordenada al origen (Eje Y): {y_intercept}\n"
                     f"• Raíz / Cero (Eje X): {x_intercept_str}"
            )
            
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(x, y, color="blue", label=f"y = {m}x + {b}")
            
            ax.plot(0, b, 'ro', label=f"Eje Y: (0, {b})")
            if x_int is not None:
                ax.plot(x_int, 0, 'go', label=f"Eje X: ({x_int:.2f}, 0)")

            ax.axhline(0, color="black", lw=0.8)
            ax.axvline(0, color="black", lw=0.8)
            ax.grid(True)
            ax.legend(fontsize=8)
            plot(fig)
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")

    # Vinculación del evento Enter a los cuadros de texto
    em.bind("<Return>", lambda event: run())
    eb.bind("<Return>", lambda event: run())

    tk.Button(c_f, text="Graficar", command=run, bg="#e1e1e1").pack(pady=5)

# 2. Ecuación de Segundo Grado
def s_grado():
    reset()
    tk.Label(c_f, text="Ecuación de 2do Grado: y = a*x² + b*x + c", font=("Arial", 10, "bold")).pack(pady=5)
    
    f = tk.Frame(c_f)
    f.pack()
    tk.Label(f, text="a:").grid(row=0, column=0)
    ea = tk.Entry(f, width=5); ea.insert(0, "1"); ea.grid(row=0, column=1)
    tk.Label(f, text="b:").grid(row=0, column=2)
    eb = tk.Entry(f, width=5); eb.insert(0, "0"); eb.grid(row=0, column=3)
    tk.Label(f, text="c:").grid(row=0, column=4)
    ec = tk.Entry(f, width=5); ec.insert(0, "-4"); ec.grid(row=0, column=5)
    
    lbl_res = tk.Label(c_f, text="", font=("Arial", 9), justify="left")
    lbl_res.pack(pady=5)

    def run():
        try:
            a, b, c = float(ea.get()), float(eb.get()), float(ec.get())
            if a == 0:
                messagebox.showwarning("Atención", "Si 'a' es 0, no es una ecuación cuadrática.")
                return

            vx = -b / (2 * a)
            vy = a * (vx ** 2) + b * vx + c
            vertice = (vx, vy)
            
            disc = b**2 - 4*a*c
            raices = []
            if disc > 0:
                r1 = (-b + np.sqrt(disc)) / (2*a)
                r2 = (-b - np.sqrt(disc)) / (2*a)
                raices = [r1, r2]
                str_raices = f"x1 = {r1:.2f}, x2 = {r2:.2f}"
            elif disc == 0:
                r1 = -b / (2*a)
                raices = [r1]
                str_raices = f"x1 = x2 = {r1:.2f}"
            else:
                str_raices = "Sin raíces reales (Discriminante < 0)"

            lbl_res.config(
                text=f"• Vértice: ({vx:.2f}, {vy:.2f})\n"
                     f"• Discriminante (Δ): {disc:.2f}\n"
                     f"• Intersección Y: (0, {c})\n"
                     f"• Raíces (Eje X): {str_raices}"
            )

            x = np.linspace(vx - 10, vx + 10, 200)
            y = a * (x**2) + b * x + c
            
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(x, y, color="green", label=f"y = {a}x² + {b}x + {c}")
            
            ax.plot(vx, vy, 'mo', label=f"Vértice: ({vx:.2f}, {vy:.2f})")
            ax.plot(0, c, 'ro', label=f"Eje Y: (0, {c})")
            for r in raices:
                ax.plot(r, 0, 'go', label=f"Raíz: {r:.2f}")

            ax.axhline(0, color="black", lw=0.8)
            ax.axvline(0, color="black", lw=0.8)
            ax.grid(True)
            ax.legend(fontsize=8)
            plot(fig)
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")

    # Vinculación del evento Enter a los cuadros de texto
    ea.bind("<Return>", lambda event: run())
    eb.bind("<Return>", lambda event: run())
    ec.bind("<Return>", lambda event: run())

    tk.Button(c_f, text="Graficar", command=run, bg="#e1e1e1").pack(pady=5)

# 3. Sistema de Ecuaciones 2x2
def sys_2x2():
    reset()
    tk.Label(c_f, text="Sistema de Ecuaciones 2x2", font=("Arial", 10, "bold")).pack(pady=5)
    
    f = tk.Frame(c_f)
    f.pack()
    
    tk.Label(f, text="Ec 1:").grid(row=0, column=0)
    e_a1 = tk.Entry(f, width=4); e_a1.insert(0, "1"); e_a1.grid(row=0, column=1)
    tk.Label(f, text="x +").grid(row=0, column=2)
    e_b1 = tk.Entry(f, width=4); e_b1.insert(0, "1"); e_b1.grid(row=0, column=3)
    tk.Label(f, text="y =").grid(row=0, column=4)
    e_c1 = tk.Entry(f, width=4); e_c1.insert(0, "5"); e_c1.grid(row=0, column=5)

    tk.Label(f, text="Ec 2:").grid(row=1, column=0)
    e_a2 = tk.Entry(f, width=4); e_a2.insert(0, "1"); e_a2.grid(row=1, column=1)
    tk.Label(f, text="x +").grid(row=1, column=2)
    e_b2 = tk.Entry(f, width=4); e_b2.insert(0, "-1"); e_b2.grid(row=1, column=3)
    tk.Label(f, text="y =").grid(row=1, column=4)
    e_c2 = tk.Entry(f, width=4); e_c2.insert(0, "1"); e_c2.grid(row=1, column=5)
        
    lbl_res = tk.Label(c_f, text="", font=("Arial", 9, "bold"))
    lbl_res.pack(pady=5)

    def run():
        try:
            a1, b1, c1 = float(e_a1.get()), float(e_b1.get()), float(e_c1.get())
            a2, b2, c2 = float(e_a2.get()), float(e_b2.get()), float(e_c2.get())
            
            A = np.array([[a1, b1], [a2, b2]])
            B = np.array([c1, c2])
            
            try:
                sol = np.linalg.solve(A, B)
                txt = f"Punto de Cruce (Solución): x = {sol[0]:.2f}, y = {sol[1]:.2f}"
            except np.linalg.LinAlgError:
                sol = None
                txt = "Sin solución única (Rectas paralelas o coincidentes)"
            
            lbl_res.config(text=txt)
                
            x = np.linspace(-10, 10, 100)
            fig, ax = plt.subplots(figsize=(5, 3))
            
            if b1 != 0: 
                ax.plot(x, (c1 - a1*x)/b1, label=f"Ec 1: {a1}x + {b1}y = {c1}")
            else:
                ax.axvline(c1/a1, label=f"Ec 1: x = {c1/a1:.2f}")

            if b2 != 0: 
                ax.plot(x, (c2 - a2*x)/b2, label=f"Ec 2: {a2}x + {b2}y = {c2}")
            else:
                ax.axvline(c2/a2, label=f"Ec 2: x = {c2/a2:.2f}")

            if sol is not None: 
                ax.plot(sol[0], sol[1], 'ro', markersize=8, label=f"Cruce: ({sol[0]:.2f}, {sol[1]:.2f})")
            
            ax.axhline(0, color="black", lw=0.8)
            ax.axvline(0, color="black", lw=0.8)
            ax.grid(True)
            ax.legend(fontsize=8)
            plot(fig)
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")

    # Vinculación del evento Enter a todos los cuadros de texto
    for entry in [e_a1, e_b1, e_c1, e_a2, e_b2, e_c2]:
        entry.bind("<Return>", lambda event: run())

    tk.Button(c_f, text="Resolver y Graficar", command=run, bg="#e1e1e1").pack(pady=5)

# 4. Sistema de Ecuaciones 3x3
def sys_3x3():
    reset()
    tk.Label(c_f, text="Sistema de Ecuaciones 3x3", font=("Arial", 10, "bold")).pack(pady=5)
    
    f = tk.Frame(c_f)
    f.pack()
    
    mat = []
    defs = [["1","1","1","6"], ["0","2","5","-4"], ["2","5","-1","27"]]
    
    for r in range(3):
        row = []
        tk.Label(f, text=f"Ec {r+1}:").grid(row=r, column=0)
        e_a = tk.Entry(f, width=4); e_a.insert(0, defs[r][0]); e_a.grid(row=r, column=1)
        tk.Label(f, text="x +").grid(row=r, column=2)
        e_b = tk.Entry(f, width=4); e_b.insert(0, defs[r][1]); e_b.grid(row=r, column=3)
        tk.Label(f, text="y +").grid(row=r, column=4)
        e_c = tk.Entry(f, width=4); e_c.insert(0, defs[r][2]); e_c.grid(row=r, column=5)
        tk.Label(f, text="z =").grid(row=r, column=6)
        e_d = tk.Entry(f, width=4); e_d.insert(0, defs[r][3]); e_d.grid(row=r, column=7)
        row.extend([e_a, e_b, e_c, e_d])
        mat.append(row)
        
    lbl_res = tk.Label(c_f, text="", font=("Arial", 9, "bold"))
    lbl_res.pack(pady=5)

    def run():
        try:
            A = np.array([[float(mat[r][c].get()) for c in range(3)] for r in range(3)])
            B = np.array([float(mat[r][3].get()) for r in range(3)])
            
            try:
                sol = np.linalg.solve(A, B)
                lbl_res.config(text=f"Punto de Intersección (Solución):\n x = {sol[0]:.2f} | y = {sol[1]:.2f} | z = {sol[2]:.2f}")
            except np.linalg.LinAlgError:
                sol = None
                lbl_res.config(text="El sistema no tiene solución única.")

            fig = plt.figure(figsize=(5, 3.5))
            ax = fig.add_subplot(111, projection='3d')
            
            x_vals = np.linspace(-10, 10, 10)
            y_vals = np.linspace(-10, 10, 10)
            X, Y = np.meshgrid(x_vals, y_vals)

            colors = ['red', 'blue', 'green']
            for r in range(3):
                a, b, c, d = A[r][0], A[r][1], A[r][2], B[r]
                if c != 0:
                    Z = (d - a*X - b*Y) / c
                    ax.plot_surface(X, Y, Z, alpha=0.4, color=colors[r])

            if sol is not None:
                ax.scatter(sol[0], sol[1], sol[2], color='black', s=50, label='Solución (Punto)')

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title("Planos 3D", fontsize=9)
            plot(fig)

        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")

    # Vinculación del evento Enter a todos los cuadros de la matriz 3x3
    for row in mat:
        for entry in row:
            entry.bind("<Return>", lambda event: run())

    tk.Button(c_f, text="Resolver y Graficar 3D", command=run, bg="#e1e1e1").pack(pady=5)

# Menú Principal
m_bar = tk.Menu(v)

m_bar.add_command(label="Gráfica 1er Grado", command=p_grado)
m_bar.add_command(label="Gráfica 2do Grado", command=s_grado)

m_sub = tk.Menu(m_bar, tearoff=0)
m_sub.add_command(label="Sistemas de 2x2", command=sys_2x2)
m_sub.add_command(label="Sistemas de 3x3", command=sys_3x3)
m_bar.add_cascade(label="Sistema de Ecuaciones", menu=m_sub)

v.config(menu=m_bar)

# Pantalla Inicial
tk.Label(v, text="CECYTEQ", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(v, text="Selecciona una opción del menú superior para comenzar.", font=("Arial", 10)).pack()

v.mainloop()