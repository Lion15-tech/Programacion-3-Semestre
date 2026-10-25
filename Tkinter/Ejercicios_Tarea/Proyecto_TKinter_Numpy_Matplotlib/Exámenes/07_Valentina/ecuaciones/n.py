import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def graficar_3x3():
    # Sistema: 
    # 2x + y - z = 2
    # x -2y + z = 3
    # 3x + y +2z =11
    A = np.array([[2,1,-1],[1,-2,1],[3,1,2]])
    B = np.array([2,3,11])
    sol = np.linalg.solve(A, B)
    x0,y0,z0 = sol
    print(f"Solución: {sol}") # [1.875, 0.625, 2.375]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Crear malla para graficar planos
    xx, yy = np.meshgrid(np.linspace(-2, 4, 10), np.linspace(-2, 4, 10))

    # Despejamos z de cada ecuación: z = ...
    # E1: z = 2x + y -2
    # E2: z = -x +2y +3
    # E3: z = (11 -3x -y)/2
    z1 = 2*xx + yy - 2
    z2 = -xx + 2*yy + 3
    z3 = (11 - 3*xx - yy)/2

    ax.plot_surface(xx, yy, z1, alpha=0.5)
    ax.plot_surface(xx, yy, z2, alpha=0.5)
    ax.plot_surface(xx, yy, z3, alpha=0.5)
    ax.scatter(x0,y0,z0, color='red', s=100, label=f'Sol {sol}')

    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    ax.set_title("Sistema 3x3 - Intersección de 3 planos")

    root = tk.Tk()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    root.mainloop()

graficar_3x3()



# Sistema: 
            # 2x + y - z = 2
            # x -2y + z = 3
            # 3x + y +2z =11
            A = np.array([[2,1,-1],[1,-2,1],[3,1,2]])
            B = np.array([2,3,11])
            sol = np.linalg.solve(A, B)
            x0,y0,z0 = sol
            print(f"Solución: {sol}") # [1.875, 0.625, 2.375]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            xx, yy = np.meshgrid(np.linspace(-2, 4, 10), np.linspace(-2, 4, 10))

            # Despejamos z de cada ecuación: z = ...
            # E1 z = 2x + y -2
            # E2 z = -x +2y +3
            # E3 z = (11 -3x -y)/2
            z1 = 2*xx + yy - 2
            z2 = -xx + 2*yy + 3
            z3 = (11 - 3*xx - yy)/2

            ax.plot_surface(xx, yy, z1, alpha=0.5)
            ax.plot_surface(xx, yy, z2, alpha=0.5)
            ax.plot_surface(xx, yy, z3, alpha=0.5)
            ax.scatter(x0,y0,z0, color='red', s=100, label=f'Sol {sol}')

            ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
            ax.set_title("Sistema 3x3 - Intersección de 3 planos")

            ventana3 = teca.Tk()
            canvas = FigureCanvasTkAgg(fig, master=ventana3)
            canvas.draw()
            canvas.get_tk_widget().pack()
            ventana3.mainloop()
