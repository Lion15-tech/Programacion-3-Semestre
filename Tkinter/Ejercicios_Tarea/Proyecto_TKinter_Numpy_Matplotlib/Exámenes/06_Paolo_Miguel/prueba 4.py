import math
import os
import tkinter as tk
from tkinter import messagebox

# Necesario para las gráficas de los sistemas 2x2 y 3x3.
# Si no lo tienes instalado: pip install matplotlib
try:
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    np = None
    Figure = None
    FigureCanvasTkAgg = None


class AppCECYTEQ:
    def __init__(self, root):
        self.root = root
        self.root.title("CECYTEQ - Herramienta Matemática")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f4f6f9")

        self.cargar_icono()

        self.main_container = tk.Frame(self.root, bg="#f4f6f9")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.crear_menu()
        self.vista_bienvenida()

    def cargar_icono(self):
        """Carga el icono si existe en la misma carpeta."""
        icon_path_png = "cecyteq_logo.png"
        icon_path_ico = "cecyteq_logo.ico"

        try:
            if os.path.exists(icon_path_png):
                self.icon_img = tk.PhotoImage(file=icon_path_png)
                self.root.iconphoto(True, self.icon_img)
            elif os.path.exists(icon_path_ico):
                self.root.iconbitmap(icon_path_ico)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")

    def crear_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_bar.add_command(
            label="Gráfica 1er Grado",
            command=self.vista_primer_grado
        )

        self.menu_bar.add_command(
            label="Gráfica 2do Grado",
            command=self.vista_segundo_grado
        )

        self.menu_sistemas = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_sistemas.add_command(
            label="Sistemas de 2x2",
            command=self.vista_sistema_2x2
        )
        self.menu_sistemas.add_command(
            label="Sistemas de 3x3",
            command=self.vista_sistema_3x3
        )

        self.menu_bar.add_cascade(
            label="Sistemas de Ecuaciones",
            menu=self.menu_sistemas
        )

        # Menú de Trigonometría
        self.menu_trig = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_trig.add_command(
            label="Triángulo rectángulo",
            command=self.vista_triangulo_rectangulo
        )
        self.menu_trig.add_command(
            label="Triángulo oblicuángulo",
            command=self.vista_triangulo_oblicuangulo
        )

        self.menu_bar.add_cascade(
            label="Trigonometría",
            menu=self.menu_trig
        )

    def limpiar_pantalla(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def crear_plano_cartesiano(self, parent, width=600, height=430):
        """Crea un plano cartesiano básico usando Canvas."""
        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg="white",
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        canvas.pack(pady=10)

        cx, cy = width // 2, height // 2
        scale = 20

        # Cuadrícula
        for x in range(0, width, scale):
            canvas.create_line(x, 0, x, height, fill="#eeeeee")

        for y in range(0, height, scale):
            canvas.create_line(0, y, width, y, fill="#eeeeee")

        # Ejes
        canvas.create_line(0, cy, width, cy, fill="#333333", width=2)
        canvas.create_line(cx, 0, cx, height, fill="#333333", width=2)

        # Flechas
        canvas.create_polygon(width - 10, cy, width - 20, cy - 5,
                              width - 20, cy + 5, fill="#333333")
        canvas.create_polygon(cx, 10, cx - 5, 20,
                              cx + 5, 20, fill="#333333")

        # Números de referencia
        for i in range(-14, 15):
            if i != 0:
                px = cx + i * scale
                if 0 < px < width:
                    canvas.create_text(px, cy + 12, text=str(i),
                                       font=("Arial", 7), fill="#555555")

                py = cy - i * scale
                if 0 < py < height:
                    canvas.create_text(cx - 12, py, text=str(i),
                                       font=("Arial", 7), fill="#555555")

        canvas.create_text(width - 12, cy - 12, text="X",
                           font=("Arial", 9, "bold"))
        canvas.create_text(cx + 12, 12, text="Y",
                           font=("Arial", 9, "bold"))

        return canvas, cx, cy, scale

    def agregar_valores(self, parent, titulo, valores):
        """Muestra los valores clave debajo de una gráfica."""
        frame = tk.LabelFrame(
            parent,
            text=titulo,
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#003366",
            padx=10,
            pady=8
        )
        frame.pack(fill=tk.X, padx=20, pady=8)

        for i, (nombre, valor) in enumerate(valores):
            tk.Label(
                frame,
                text=f"{nombre}: {valor}",
                font=("Arial", 10),
                bg="#ffffff",
                fg="#333333",
                anchor="w"
            ).grid(row=i // 3, column=i % 3, sticky="w", padx=15, pady=3)

        return frame

    def verificar_matplotlib(self):
        if Figure is None or FigureCanvasTkAgg is None or np is None:
            messagebox.showerror(
                "Falta una librería",
                "Para las gráficas de los sistemas instala matplotlib y numpy:\n\n"
                "pip install matplotlib numpy"
            )
            return False
        return True

    def dibujar_triangulo_canvas(self, parent, a, b, c, A, B, C):
        """Dibuja un triángulo genérico dadas las longitudes de sus lados y ángulos."""
        canvas = tk.Canvas(parent, width=550, height=350, bg="white", highlightthickness=1, highlightbackground="#cccccc")
        canvas.pack(pady=10)

        # Coordenadas: C en origen (0,0), B en (a, 0), A mediante trigonometría
        rad_C = math.radians(C)
        x_C, y_C = 0.0, 0.0
        x_B, y_B = a, 0.0
        x_A = b * math.cos(rad_C)
        y_A = b * math.sin(rad_C)

        xs = [x_A, x_B, x_C]
        ys = [y_A, y_B, y_C]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        ancho_real = max_x - min_x if max_x != min_x else 1
        alto_real = max_y - min_y if max_y != min_y else 1

        margin = 40
        scale = min((550 - 2 * margin) / ancho_real, (350 - 2 * margin) / alto_real)

        def transform(x, y):
            px = margin + (x - min_x) * scale
            py = 350 - (margin + (y - min_y) * scale)
            return px, py

        pA = transform(x_A, y_A)
        pB = transform(x_B, y_B)
        pC = transform(x_C, y_C)

        # Dibujar polígono
        canvas.create_polygon([pA[0], pA[1], pB[0], pB[1], pC[0], pC[1]], fill="#e6f0fa", outline="#003366", width=2)

        # Etiquetas Vértices
        canvas.create_text(pA[0], pA[1] - 12, text="A", font=("Arial", 10, "bold"), fill="#d9534f")
        canvas.create_text(pB[0] + 12, pB[1], text="B", font=("Arial", 10, "bold"), fill="#d9534f")
        canvas.create_text(pC[0] - 12, pC[1], text="C", font=("Arial", 10, "bold"), fill="#d9534f")

        # Etiquetas Lados
        canvas.create_text((pB[0] + pC[0]) / 2, (pB[1] + pC[1]) / 2 + 15, text=f"a={a:.2f}", font=("Arial", 9, "bold"), fill="#003366")
        canvas.create_text((pA[0] + pC[0]) / 2 - 20, (pA[1] + pC[1]) / 2, text=f"b={b:.2f}", font=("Arial", 9, "bold"), fill="#003366")
        canvas.create_text((pA[0] + pB[0]) / 2 + 15, (pA[1] + pB[1]) / 2, text=f"c={c:.2f}", font=("Arial", 9, "bold"), fill="#003366")

        return canvas

    # ==========================================================
    # VISTA INICIAL
    # ==========================================================

    def vista_bienvenida(self):
        self.limpiar_pantalla()

        frame = tk.Frame(self.main_container, bg="#f4f6f9")
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Colegio de Estudios Científicos y Tecnológicos\ndel Estado de Querétaro",
            font=("Arial", 18, "bold"),
            fg="#003366",
            bg="#f4f6f9",
            justify="center"
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Herramienta Matemática",
            font=("Arial", 16, "bold"),
            fg="#333333",
            bg="#f4f6f9"
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Selecciona una opción del menú superior para comenzar.",
            font=("Arial", 11),
            bg="#f4f6f9",
            fg="#555555"
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Ahora cada opción muestra su gráfica y sus valores clave.",
            font=("Arial", 10, "italic"),
            bg="#f4f6f9",
            fg="#666666"
        ).pack(pady=5)

    # ==========================================================
    # ECUACIÓN DE PRIMER GRADO
    # ==========================================================

    def vista_primer_grado(self):
        self.limpiar_pantalla()

        tk.Label(
            self.main_container,
            text="Ecuación de Primer Grado: y = mx + b",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        f_inputs = tk.Frame(self.main_container, bg="#f4f6f9")
        f_inputs.pack(pady=5)

        tk.Label(f_inputs, text="m (Pendiente):",
                 bg="#f4f6f9").grid(row=0, column=0, padx=5)

        e_m = tk.Entry(f_inputs, width=7)
        e_m.grid(row=0, column=1, padx=5)
        e_m.insert(0, "2")

        tk.Label(f_inputs, text="b (Intersección con Y):",
                 bg="#f4f6f9").grid(row=0, column=2, padx=5)

        e_b = tk.Entry(f_inputs, width=7)
        e_b.grid(row=0, column=3, padx=5)
        e_b.insert(0, "1")

        f_canvas = tk.Frame(self.main_container, bg="#f4f6f9")
        f_canvas.pack()

        info_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        info_frame.pack(fill=tk.X)

        def graficar(event=None):
            for widget in f_canvas.winfo_children():
                widget.destroy()

            for widget in info_frame.winfo_children():
                widget.destroy()

            try:
                m = float(e_m.get())
                b = float(e_b.get())

                canvas, cx, cy, scale = self.crear_plano_cartesiano(f_canvas)

                x1, x2 = -15, 15
                y1 = m * x1 + b
                y2 = m * x2 + b

                px1 = cx + x1 * scale
                py1 = cy - y1 * scale
                px2 = cx + x2 * scale
                py2 = cy - y2 * scale

                canvas.create_line(
                    px1, py1, px2, py2,
                    fill="#003366",
                    width=3
                )

                # Intersección con Y
                py_b = cy - b * scale
                if 0 <= py_b <= 430:
                    canvas.create_oval(
                        cx - 5, py_b - 5, cx + 5, py_b + 5,
                        fill="#d9534f", outline=""
                    )

                # Intersección con X
                if m != 0:
                    x_inter = -b / m
                    if -15 <= x_inter <= 15:
                        px = cx + x_inter * scale
                        canvas.create_oval(
                            px - 5, cy - 5, px + 5, cy + 5,
                            fill="#5cb85c", outline=""
                        )

                    x_text = f"{x_inter:.2f}"
                else:
                    x_text = "No existe (recta horizontal)"

                self.agregar_valores(
                    info_frame,
                    "Valores clave",
                    [
                        ("Pendiente m", f"{m:.2f}"),
                        ("Intersección con Y", f"(0, {b:.2f})"),
                        ("Intersección con X",
                         f"({x_inter:.2f}, 0)" if m != 0 else x_text),
                        ("Ecuación", f"y = {m:g}x + {b:g}")
                    ]
                )

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Ingresa números válidos."
                )

        tk.Button(
            f_inputs,
            text="Graficar",
            command=graficar,
            bg="#003366",
            fg="white",
            font=("Arial", 9, "bold")
        ).grid(row=0, column=4, padx=10)

        # Vincular la tecla Enter para cada Entry
        e_m.bind("<Return>", graficar)
        e_b.bind("<Return>", graficar)

        graficar()

    # ==========================================================
    # ECUACIÓN DE SEGUNDO GRADO
    # ==========================================================

    def vista_segundo_grado(self):
        self.limpiar_pantalla()

        tk.Label(
            self.main_container,
            text="Ecuación de Segundo Grado: y = ax² + bx + c",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        f_inputs = tk.Frame(self.main_container, bg="#f4f6f9")
        f_inputs.pack(pady=5)

        tk.Label(f_inputs, text="a:", bg="#f4f6f9").grid(row=0, column=0)
        e_a = tk.Entry(f_inputs, width=6)
        e_a.grid(row=0, column=1, padx=4)
        e_a.insert(0, "1")

        tk.Label(f_inputs, text="b:", bg="#f4f6f9").grid(row=0, column=2)
        e_b = tk.Entry(f_inputs, width=6)
        e_b.grid(row=0, column=3, padx=4)
        e_b.insert(0, "0")

        tk.Label(f_inputs, text="c:", bg="#f4f6f9").grid(row=0, column=4)
        e_c = tk.Entry(f_inputs, width=6)
        e_c.grid(row=0, column=5, padx=4)
        e_c.insert(0, "-3")

        f_canvas = tk.Frame(self.main_container, bg="#f4f6f9")
        f_canvas.pack()

        info_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        info_frame.pack(fill=tk.X)

        def graficar(event=None):
            for widget in f_canvas.winfo_children():
                widget.destroy()

            for widget in info_frame.winfo_children():
                widget.destroy()

            try:
                a = float(e_a.get())
                b = float(e_b.get())
                c = float(e_c.get())

                if a == 0:
                    messagebox.showerror(
                        "Error",
                        "En una ecuación de segundo grado, 'a' no puede ser 0."
                    )
                    return

                canvas, cx, cy, scale = self.crear_plano_cartesiano(f_canvas)

                puntos = []
                x = -12.0

                while x <= 12.0:
                    y = a * x**2 + b * x + c
                    px = cx + x * scale
                    py = cy - y * scale

                    if -100 <= py <= 530:
                        puntos.extend([px, py])

                    x += 0.05

                if len(puntos) >= 4:
                    canvas.create_line(
                        puntos,
                        fill="#d9534f",
                        width=2,
                        smooth=True
                    )

                discriminante = b**2 - 4*a*c
                xv = -b / (2*a)
                yv = a*xv**2 + b*xv + c

                if -15 <= xv <= 15 and -10 <= yv <= 10:
                    pxv = cx + xv * scale
                    pyv = cy - yv * scale
                    canvas.create_oval(
                        pxv - 6, pyv - 6,
                        pxv + 6, pyv + 6,
                        fill="#003366",
                        outline=""
                    )

                valores = [
                    ("Vértice", f"({xv:.2f}, {yv:.2f})"),
                    ("Intersección con Y", f"(0, {c:.2f})"),
                    ("Discriminante", f"{discriminante:.2f}")
                ]

                if discriminante > 0:
                    r1 = (-b + math.sqrt(discriminante)) / (2*a)
                    r2 = (-b - math.sqrt(discriminante)) / (2*a)

                    valores.extend([
                        ("Raíz 1", f"{r1:.2f}"),
                        ("Raíz 2", f"{r2:.2f}"),
                        ("Tipo", "2 raíces reales")
                    ])

                    for r in (r1, r2):
                        if -15 <= r <= 15:
                            px = cx + r * scale
                            canvas.create_oval(
                                px - 5, cy - 5,
                                px + 5, cy + 5,
                                fill="#5cb85c",
                                outline=""
                            )

                elif discriminante == 0:
                    r = -b / (2*a)
                    valores.extend([
                        ("Raíz", f"{r:.2f}"),
                        ("Tipo", "1 raíz real doble")
                    ])

                else:
                    valores.append(("Tipo", "Sin raíces reales"))

                self.agregar_valores(
                    info_frame,
                    "Valores clave",
                    valores
                )

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Ingresa números válidos."
                )

        tk.Button(
            f_inputs,
            text="Graficar",
            command=graficar,
            bg="#003366",
            fg="white",
            font=("Arial", 9, "bold")
        ).grid(row=0, column=6, padx=10)

        # Vincular la tecla Enter para cada Entry
        e_a.bind("<Return>", graficar)
        e_b.bind("<Return>", graficar)
        e_c.bind("<Return>", graficar)

        graficar()

    # ==========================================================
    # SISTEMA 2x2
    # ==========================================================

    def vista_sistema_2x2(self):
        self.limpiar_pantalla()

        tk.Label(
            self.main_container,
            text="Sistema de Ecuaciones 2x2",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        f_inputs = tk.Frame(self.main_container, bg="#f4f6f9")
        f_inputs.pack(pady=10)

        # Ecuación 1
        tk.Label(f_inputs, text="Ec 1:", bg="#f4f6f9").grid(row=0, column=0)
        e_a1 = tk.Entry(f_inputs, width=5)
        e_a1.grid(row=0, column=1)
        e_a1.insert(0, "1")

        tk.Label(f_inputs, text="x +", bg="#f4f6f9").grid(row=0, column=2)
        e_b1 = tk.Entry(f_inputs, width=5)
        e_b1.grid(row=0, column=3)
        e_b1.insert(0, "1")

        tk.Label(f_inputs, text="y =", bg="#f4f6f9").grid(row=0, column=4)
        e_c1 = tk.Entry(f_inputs, width=5)
        e_c1.grid(row=0, column=5)
        e_c1.insert(0, "5")

        # Ecuación 2
        tk.Label(f_inputs, text="Ec 2:", bg="#f4f6f9").grid(
            row=1, column=0, pady=5
        )
        e_a2 = tk.Entry(f_inputs, width=5)
        e_a2.grid(row=1, column=1)
        e_a2.insert(0, "1")

        tk.Label(f_inputs, text="x +", bg="#f4f6f9").grid(row=1, column=2)
        e_b2 = tk.Entry(f_inputs, width=5)
        e_b2.grid(row=1, column=3)
        e_b2.insert(0, "-1")

        tk.Label(f_inputs, text="y =", bg="#f4f6f9").grid(row=1, column=4)
        e_c2 = tk.Entry(f_inputs, width=5)
        e_c2.grid(row=1, column=5)
        e_c2.insert(0, "1")

        graph_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        graph_frame.pack()

        info_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        info_frame.pack(fill=tk.X)

        def resolver(event=None):
            if not self.verificar_matplotlib():
                return

            for widget in graph_frame.winfo_children():
                widget.destroy()

            for widget in info_frame.winfo_children():
                widget.destroy()

            try:
                a1 = float(e_a1.get())
                b1 = float(e_b1.get())
                c1 = float(e_c1.get())

                a2 = float(e_a2.get())
                b2 = float(e_b2.get())
                c2 = float(e_c2.get())

                det = a1*b2 - a2*b1

                fig = Figure(figsize=(7.5, 4.5), dpi=90)
                ax = fig.add_subplot(111)

                x = np.linspace(-10, 10, 500)

                if b1 != 0:
                    y1 = (c1 - a1*x) / b1
                    ax.plot(x, y1, label="Ecuación 1")
                elif a1 != 0:
                    x1 = np.full_like(x, c1/a1)
                    ax.plot(x1, x, label="Ecuación 1")

                if b2 != 0:
                    y2 = (c2 - a2*x) / b2
                    ax.plot(x, y2, label="Ecuación 2")
                elif a2 != 0:
                    x2 = np.full_like(x, c2/a2)
                    ax.plot(x2, x, label="Ecuación 2")

                ax.axhline(0, linewidth=1)
                ax.axvline(0, linewidth=1)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_title("Gráfica del sistema 2x2")
                ax.legend()

                valores = [
                    ("Determinante", f"{det:.2f}")
                ]

                if abs(det) > 1e-10:
                    x_sol = (c1*b2 - c2*b1) / det
                    y_sol = (a1*c2 - a2*c1) / det

                    ax.scatter(
                        [x_sol], [y_sol],
                        s=70,
                        zorder=5,
                        label="Solución"
                    )
                    ax.legend()

                    valores.extend([
                        ("Solución x", f"{x_sol:.2f}"),
                        ("Solución y", f"{y_sol:.2f}"),
                        ("Punto de intersección",
                         f"({x_sol:.2f}, {y_sol:.2f})"),
                        ("Tipo", "Una solución")
                    ])
                else:
                    valores.extend([
                        ("Solución", "No hay solución única"),
                        ("Tipo", "Rectas paralelas o coincidentes")
                    ])

                canvas = FigureCanvasTkAgg(fig, master=graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                self.agregar_valores(
                    info_frame,
                    "Valores clave",
                    valores
                )

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Ingresa números válidos."
                )

        btn = tk.Button(
            f_inputs,
            text="Resolver y graficar",
            command=resolver,
            bg="#003366",
            fg="white",
            font=("Arial", 9, "bold")
        )
        btn.grid(row=0, column=6, rowspan=2, padx=15)

        # Vincular la tecla Enter para todos los Entry del 2x2
        for entry in (e_a1, e_b1, e_c1, e_a2, e_b2, e_c2):
            entry.bind("<Return>", resolver)

        resolver()

    # ==========================================================
    # SISTEMA 3x3
    # ==========================================================

    def vista_sistema_3x3(self):
        self.limpiar_pantalla()

        tk.Label(
            self.main_container,
            text="Sistema de Ecuaciones 3x3",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        f_inputs = tk.Frame(self.main_container, bg="#f4f6f9")
        f_inputs.pack(pady=10)

        entries = []

        for i in range(3):
            row = []

            tk.Label(
                f_inputs,
                text=f"Ec {i+1}:",
                bg="#f4f6f9"
            ).grid(row=i, column=0, pady=3)

            ea = tk.Entry(f_inputs, width=5)
            ea.grid(row=i, column=1)
            ea.insert(0, "1" if i == 0 else "0")

            tk.Label(f_inputs, text="x +", bg="#f4f6f9").grid(
                row=i, column=2
            )

            eb = tk.Entry(f_inputs, width=5)
            eb.grid(row=i, column=3)
            eb.insert(0, "1" if i == 1 else "0")

            tk.Label(f_inputs, text="y +", bg="#f4f6f9").grid(
                row=i, column=4
            )

            ec = tk.Entry(f_inputs, width=5)
            ec.grid(row=i, column=5)
            ec.insert(0, "1" if i == 2 else "0")

            tk.Label(f_inputs, text="z =", bg="#f4f6f9").grid(
                row=i, column=6
            )

            ed = tk.Entry(f_inputs, width=5)
            ed.grid(row=i, column=7)
            ed.insert(0, str(i + 1))

            row.extend([ea, eb, ec, ed])
            entries.append(row)

        graph_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        graph_frame.pack()

        info_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        info_frame.pack(fill=tk.X)

        def determinante_3x3(m):
            return (
                m[0][0] * (m[1][1]*m[2][2] - m[1][2]*m[2][1])
                - m[0][1] * (m[1][0]*m[2][2] - m[1][2]*m[2][0])
                + m[0][2] * (m[1][0]*m[2][1] - m[1][1]*m[2][0])
            )

        def graficar_plano(ax, coef, d, numero):
            a, b, c = coef
            rango = np.linspace(-5, 5, 25)

            if abs(c) > 1e-10:
                X, Y = np.meshgrid(rango, rango)
                Z = (d - a*X - b*Y) / c
                Z = np.clip(Z, -10, 10)
                ax.plot_surface(X, Y, Z, alpha=0.35)
            elif abs(b) > 1e-10:
                X, Z = np.meshgrid(rango, rango)
                Y = (d - a*X - c*Z) / b
                Y = np.clip(Y, -10, 10)
                ax.plot_surface(X, Y, Z, alpha=0.35)
            elif abs(a) > 1e-10:
                Y, Z = np.meshgrid(rango, rango)
                X = (d - b*Y - c*Z) / a
                X = np.clip(X, -10, 10)
                ax.plot_surface(X, Y, Z, alpha=0.35)

        def resolver(event=None):
            if not self.verificar_matplotlib():
                return

            for widget in graph_frame.winfo_children():
                widget.destroy()

            for widget in info_frame.winfo_children():
                widget.destroy()

            try:
                m = [
                    [float(e.get()) for e in row]
                    for row in entries
                ]

                det = determinante_3x3([
                    [m[0][0], m[0][1], m[0][2]],
                    [m[1][0], m[1][1], m[1][2]],
                    [m[2][0], m[2][1], m[2][2]]
                ])

                fig = Figure(figsize=(7.5, 5.0), dpi=90)
                ax = fig.add_subplot(111, projection="3d")

                for i in range(3):
                    graficar_plano(
                        ax,
                        [m[i][0], m[i][1], m[i][2]],
                        m[i][3],
                        i + 1
                    )

                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")
                ax.set_title("Gráfica 3D de los tres planos")

                valores = [
                    ("Determinante", f"{det:.2f}")
                ]

                if abs(det) > 1e-10:
                    dx_matrix = [
                        [m[0][3], m[0][1], m[0][2]],
                        [m[1][3], m[1][1], m[1][2]],
                        [m[2][3], m[2][1], m[2][2]]
                    ]

                    dy_matrix = [
                        [m[0][0], m[0][3], m[0][2]],
                        [m[1][0], m[1][3], m[1][2]],
                        [m[2][0], m[2][3], m[2][2]]
                    ]

                    dz_matrix = [
                        [m[0][0], m[0][1], m[0][3]],
                        [m[1][0], m[1][1], m[1][3]],
                        [m[2][0], m[2][1], m[2][3]]
                    ]

                    dx = determinante_3x3(dx_matrix)
                    dy = determinante_3x3(dy_matrix)
                    dz = determinante_3x3(dz_matrix)

                    x_sol = dx / det
                    y_sol = dy / det
                    z_sol = dz / det

                    ax.scatter(
                        [x_sol],
                        [y_sol],
                        [z_sol],
                        s=90,
                        zorder=10,
                        label="Solución"
                    )
                    ax.legend()

                    valores.extend([
                        ("Dx", f"{dx:.2f}"),
                        ("Dy", f"{dy:.2f}"),
                        ("Dz", f"{dz:.2f}"),
                        ("x", f"{x_sol:.2f}"),
                        ("y", f"{y_sol:.2f}"),
                        ("z", f"{z_sol:.2f}"),
                        ("Solución", f"({x_sol:.2f}, {y_sol:.2f}, {z_sol:.2f})")
                    ])

                else:
                    valores.extend([
                        ("Solución", "No existe solución única"),
                        ("Tipo", "Determinante = 0")
                    ])

                canvas = FigureCanvasTkAgg(fig, master=graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                self.agregar_valores(
                    info_frame,
                    "Valores clave",
                    valores
                )

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Ingresa números válidos."
                )

        btn_resolver = tk.Button(
            f_inputs,
            text="Resolver y graficar",
            command=resolver,
            bg="#003366",
            fg="white",
            font=("Arial", 9, "bold")
        )
        btn_resolver.grid(row=3, column=0, columnspan=8, pady=8)

        # Vincular la tecla Enter para cada Entry de la matriz 3x3
        for row in entries:
            for entry in row:
                entry.bind("<Return>", resolver)

        resolver()

    # ==========================================================
    # TRIGONOMETRÍA: TRIÁNGULO RECTÁNGULO
    # ==========================================================

    def vista_triangulo_rectangulo(self):
        self.limpiar_pantalla()

        tk.Label(
            self.main_container,
            text="Trigonometría - Triángulo Rectángulo (C = 90°)",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        tk.Label(
            self.main_container,
            text="Ingresa al menos 2 datos (al menos un lado: a, b o c, y/o un ángulo agudo: A o B):",
            font=("Arial", 10),
            bg="#f4f6f9",
            fg="#555555"
        ).pack()

        f_inputs = tk.Frame(self.main_container, bg="#f4f6f9")
        f_inputs.pack(pady=10)

        # Entradas
        tk.Label(f_inputs, text="a (Cateto):", bg="#f4f6f9").grid(row=0, column=0, padx=5)
        e_a = tk.Entry(f_inputs, width=8)
        e_a.grid(row=0, column=1, padx=5)

        tk.Label(f_inputs, text="b (Cateto):", bg="#f4f6f9").grid(row=0, column=2, padx=5)
        e_b = tk.Entry(f_inputs, width=8)
        e_b.grid(row=0, column=3, padx=5)

        tk.Label(f_inputs, text="c (Hipotenusa):", bg="#f4f6f9").grid(row=0, column=4, padx=5)
        e_c = tk.Entry(f_inputs, width=8)
        e_c.grid(row=0, column=5, padx=5)

        tk.Label(f_inputs, text="Ángulo A (°):", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5)
        e_A = tk.Entry(f_inputs, width=8)
        e_A.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(f_inputs, text="Ángulo B (°):", bg="#f4f6f9").grid(row=1, column=2, padx=5, pady=5)
        e_B = tk.Entry(f_inputs, width=8)
        e_B.grid(row=1, column=3, padx=5, pady=5)

        # C es siempre 90
        tk.Label(f_inputs, text="Ángulo C = 90°", font=("Arial", 9, "bold"), bg="#f4f6f9", fg="#003366").grid(row=1, column=4, columnspan=2)

        e_a.insert(0, "3")
        e_b.insert(0, "4")

        graph_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        graph_frame.pack()

        info_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        info_frame.pack(fill=tk.X)

        def resolver(event=None):
            for widget in graph_frame.winfo_children():
                widget.destroy()
            for widget in info_frame.winfo_children():
                widget.destroy()

            try:
                a = float(e_a.get()) if e_a.get().strip() else None
                b = float(e_b.get()) if e_b.get().strip() else None
                c = float(e_c.get()) if e_c.get().strip() else None
                A = float(e_A.get()) if e_A.get().strip() else None
                B = float(e_B.get()) if e_B.get().strip() else None

                # Validaciones iniciales de positividad
                for val, nombre in [(a, "a"), (b, "b"), (c, "c"), (A, "A"), (B, "B")]:
                    if val is not None and val <= 0:
                        messagebox.showerror("Error", f"El valor de {nombre} debe ser mayor que 0.")
                        return

                if A is not None and A >= 90:
                    messagebox.showerror("Error", "El ángulo agudo A debe ser menor a 90°.")
                    return
                if B is not None and B >= 90:
                    messagebox.showerror("Error", "El ángulo agudo B debe ser menor a 90°.")
                    return

                # Resolver triángulo
                if a is not None and b is not None:
                    c = math.sqrt(a**2 + b**2)
                    A = math.degrees(math.atan(a / b))
                    B = 90 - A
                elif a is not None and c is not None:
                    if a >= c:
                        messagebox.showerror("Error", "El cateto 'a' debe ser menor que la hipotenusa 'c'.")
                        return
                    b = math.sqrt(c**2 - a**2)
                    A = math.degrees(math.asin(a / c))
                    B = 90 - A
                elif b is not None and c is not None:
                    if b >= c:
                        messagebox.showerror("Error", "El cateto 'b' debe ser menor que la hipotenusa 'c'.")
                        return
                    a = math.sqrt(c**2 - b**2)
                    B = math.degrees(math.asin(b / c))
                    A = 90 - B
                elif a is not None and A is not None:
                    B = 90 - A
                    c = a / math.sin(math.radians(A))
                    b = math.sqrt(c**2 - a**2)
                elif a is not None and B is not None:
                    A = 90 - B
                    c = a / math.cos(math.radians(B))
                    b = a * math.tan(math.radians(B))
                elif b is not None and A is not None:
                    B = 90 - A
                    c = b / math.cos(math.radians(A))
                    a = b * math.tan(math.radians(A))
                elif b is not None and B is not None:
                    A = 90 - B
                    c = b / math.sin(math.radians(B))
                    a = b / math.tan(math.radians(B))
                elif c is not None and A is not None:
                    B = 90 - A
                    a = c * math.sin(math.radians(A))
                    b = c * math.cos(math.radians(A))
                elif c is not None and B is not None:
                    A = 90 - B
                    b = c * math.sin(math.radians(B))
                    a = c * math.cos(math.radians(B))
                else:
                    messagebox.showerror("Datos Insuficientes", "Ingresa al menos 2 datos válidos (al menos 1 lado).")
                    return

                C = 90.0
                area = 0.5 * a * b
                perimetro = a + b + c

                self.dibujar_triangulo_canvas(graph_frame, a, b, c, A, B, C)

                self.agregar_valores(
                    info_frame,
                    "Resultados del Triángulo Rectángulo",
                    [
                        ("Lado a (cateto)", f"{a:.2f}"),
                        ("Lado b (cateto)", f"{b:.2f}"),
                        ("Lado c (hipotenusa)", f"{c:.2f}"),
                        ("Ángulo A", f"{A:.2f}°"),
                        ("Ángulo B", f"{B:.2f}°"),
                        ("Ángulo C", "90.00°"),
                        ("Área", f"{area:.2f}"),
                        ("Perímetro", f"{perimetro:.2f}")
                    ]
                )

            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa números válidos.")

        btn = tk.Button(
            f_inputs, text="Calcular y Graficar", command=resolver,
            bg="#003366", fg="white", font=("Arial", 9, "bold")
        )
        btn.grid(row=0, column=6, rowspan=2, padx=15)

        for e in (e_a, e_b, e_c, e_A, e_B):
            e.bind("<Return>", resolver)

        resolver()

    # ==========================================================
    # TRIGONOMETRÍA: TRIÁNGULO OBLICUÁNGULO
    # ==========================================================

    def vista_triangulo_oblicuangulo(self):
        self.limpiar_pantalla()

        tk.Label(
            self.main_container,
            text="Trigonometría - Triángulo Oblicuángulo",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        tk.Label(
            self.main_container,
            text="Ingresa exactamente 3 datos conocidos (al menos un lado: a, b o c):",
            font=("Arial", 10),
            bg="#f4f6f9",
            fg="#555555"
        ).pack()

        f_inputs = tk.Frame(self.main_container, bg="#f4f6f9")
        f_inputs.pack(pady=10)

        tk.Label(f_inputs, text="Lado a:", bg="#f4f6f9").grid(row=0, column=0, padx=5)
        e_a = tk.Entry(f_inputs, width=7)
        e_a.grid(row=0, column=1, padx=5)

        tk.Label(f_inputs, text="Lado b:", bg="#f4f6f9").grid(row=0, column=2, padx=5)
        e_b = tk.Entry(f_inputs, width=7)
        e_b.grid(row=0, column=3, padx=5)

        tk.Label(f_inputs, text="Lado c:", bg="#f4f6f9").grid(row=0, column=4, padx=5)
        e_c = tk.Entry(f_inputs, width=7)
        e_c.grid(row=0, column=5, padx=5)

        tk.Label(f_inputs, text="Ángulo A (°):", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5)
        e_A = tk.Entry(f_inputs, width=7)
        e_A.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(f_inputs, text="Ángulo B (°):", bg="#f4f6f9").grid(row=1, column=2, padx=5, pady=5)
        e_B = tk.Entry(f_inputs, width=7)
        e_B.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(f_inputs, text="Ángulo C (°):", bg="#f4f6f9").grid(row=1, column=4, padx=5, pady=5)
        e_C = tk.Entry(f_inputs, width=7)
        e_C.grid(row=1, column=5, padx=5, pady=5)

        e_a.insert(0, "5")
        e_b.insert(0, "7")
        e_c.insert(0, "10")

        graph_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        graph_frame.pack()

        info_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        info_frame.pack(fill=tk.X)

        def resolver(event=None):
            for widget in graph_frame.winfo_children():
                widget.destroy()
            for widget in info_frame.winfo_children():
                widget.destroy()

            try:
                a = float(e_a.get()) if e_a.get().strip() else None
                b = float(e_b.get()) if e_b.get().strip() else None
                c = float(e_c.get()) if e_c.get().strip() else None
                A = float(e_A.get()) if e_A.get().strip() else None
                B = float(e_B.get()) if e_B.get().strip() else None
                C = float(e_C.get()) if e_C.get().strip() else None

                ingresados = [v for v in (a, b, c, A, B, C) if v is not None]
                if len(ingresados) != 3:
                    messagebox.showerror("Error de entradas", "Debes ingresar exactamente 3 datos para resolver el triángulo.")
                    return

                lados_count = sum(1 for v in (a, b, c) if v is not None)
                if lados_count == 0:
                    messagebox.showerror("Error", "Debes proporcionar al menos un lado.")
                    return

                # Validaciones de valor
                for val, nom in [(a, 'a'), (b, 'b'), (c, 'c'), (A, 'A'), (B, 'B'), (C, 'C')]:
                    if val is not None and val <= 0:
                        messagebox.showerror("Error", f"El valor de {nom} debe ser positivo.")
                        return

                # CASO 1: LLL (Tres Lados)
                if a is not None and b is not None and c is not None:
                    if (a + b <= c) or (a + c <= b) or (b + c <= a):
                        messagebox.showerror("Error de Geometría", "Los lados ingresados no cumplen la desigualdad triangular.")
                        return
                    cosA = (b**2 + c**2 - a**2) / (2 * b * c)
                    cosB = (a**2 + c**2 - b**2) / (2 * a * c)
                    A = math.degrees(math.acos(max(-1.0, min(1.0, cosA))))
                    B = math.degrees(math.acos(max(-1.0, min(1.0, cosB))))
                    C = 180.0 - A - B

                # CASO 2: Dos ángulos y un lado (ALA / AAL)
                elif sum(1 for v in (A, B, C) if v is not None) == 2:
                    if A is not None and B is not None:
                        C = 180.0 - A - B
                    elif A is not None and C is not None:
                        B = 180.0 - A - C
                    elif B is not None and C is not None:
                        A = 180.0 - B - C

                    if A <= 0 or B <= 0 or C <= 0:
                        messagebox.showerror("Error", "La suma de los ángulos dados debe ser menor a 180°.")
                        return

                    radA, radB, radC = math.radians(A), math.radians(B), math.radians(C)

                    if a is not None:
                        b = a * math.sin(radB) / math.sin(radA)
                        c = a * math.sin(radC) / math.sin(radA)
                    elif b is not None:
                        a = b * math.sin(radA) / math.sin(radB)
                        c = b * math.sin(radC) / math.sin(radB)
                    elif c is not None:
                        a = c * math.sin(radA) / math.sin(radC)
                        b = c * math.sin(radB) / math.sin(radC)

                # CASO 3: Dos lados y un ángulo
                elif lados_count == 2:
                    # LAL (Ángulo comprendido)
                    if a is not None and b is not None and C is not None:
                        c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C)))
                        A = math.degrees(math.acos(max(-1.0, min(1.0, (b**2 + c**2 - a**2)/(2*b*c)))))
                        B = 180.0 - A - C
                    elif a is not None and c is not None and B is not None:
                        b = math.sqrt(a**2 + c**2 - 2*a*c*math.cos(math.radians(B)))
                        A = math.degrees(math.acos(max(-1.0, min(1.0, (b**2 + c**2 - a**2)/(2*b*c)))))
                        C = 180.0 - A - B
                    elif b is not None and c is not None and A is not None:
                        a = math.sqrt(b**2 + c**2 - 2*b*c*math.cos(math.radians(A)))
                        B = math.degrees(math.acos(max(-1.0, min(1.0, (a**2 + c**2 - b**2)/(2*a*c)))))
                        C = 180.0 - A - B

                    # LLA (Ángulo no comprendido - Ley de Senos)
                    else:
                        if a is not None and b is not None and A is not None:
                            sinB = (b * math.sin(math.radians(A))) / a
                            if sinB > 1.0:
                                messagebox.showerror("Error", "No se puede formar un triángulo con estos datos.")
                                return
                            B = math.degrees(math.asin(sinB))
                            C = 180.0 - A - B
                            c = a * math.sin(math.radians(C)) / math.sin(math.radians(A))

                        elif a is not None and b is not None and B is not None:
                            sinA = (a * math.sin(math.radians(B))) / b
                            if sinA > 1.0:
                                messagebox.showerror("Error", "No se puede formar un triángulo con estos datos.")
                                return
                            A = math.degrees(math.asin(sinA))
                            C = 180.0 - A - B
                            c = b * math.sin(math.radians(C)) / math.sin(math.radians(B))

                        elif b is not None and c is not None and B is not None:
                            sinC = (c * math.sin(math.radians(B))) / b
                            if sinC > 1.0:
                                messagebox.showerror("Error", "No se puede formar un triángulo con estos datos.")
                                return
                            C = math.degrees(math.asin(sinC))
                            A = 180.0 - B - C
                            a = b * math.sin(math.radians(A)) / math.sin(math.radians(B))

                        elif b is not None and c is not None and C is not None:
                            sinB = (b * math.sin(math.radians(C))) / c
                            if sinB > 1.0:
                                messagebox.showerror("Error", "No se puede formar un triángulo con estos datos.")
                                return
                            B = math.degrees(math.asin(sinB))
                            A = 180.0 - B - C
                            a = c * math.sin(math.radians(A)) / math.sin(math.radians(C))

                        elif a is not None and c is not None and A is not None:
                            sinC = (c * math.sin(math.radians(A))) / a
                            if sinC > 1.0:
                                messagebox.showerror("Error", "No se puede formar un triángulo con estos datos.")
                                return
                            C = math.degrees(math.asin(sinC))
                            B = 180.0 - A - C
                            b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))

                        elif a is not None and c is not None and C is not None:
                            sinA = (a * math.sin(math.radians(C))) / c
                            if sinA > 1.0:
                                messagebox.showerror("Error", "No se puede formar un triángulo con estos datos.")
                                return
                            A = math.degrees(math.asin(sinA))
                            B = 180.0 - A - C
                            b = c * math.sin(math.radians(B)) / math.sin(math.radians(C))

                s = (a + b + c) / 2
                area = math.sqrt(max(0, s * (s - a) * (s - b) * (s - c)))
                perimetro = a + b + c

                self.dibujar_triangulo_canvas(graph_frame, a, b, c, A, B, C)

                self.agregar_valores(
                    info_frame,
                    "Resultados del Triángulo Oblicuángulo",
                    [
                        ("Lado a", f"{a:.2f}"),
                        ("Lado b", f"{b:.2f}"),
                        ("Lado c", f"{c:.2f}"),
                        ("Ángulo A", f"{A:.2f}°"),
                        ("Ángulo B", f"{B:.2f}°"),
                        ("Ángulo C", f"{C:.2f}°"),
                        ("Área", f"{area:.2f}"),
                        ("Perímetro", f"{perimetro:.2f}")
                    ]
                )

            except ValueError:
                messagebox.showerror("Error", "Ingresa datos numéricos válidos.")

        btn = tk.Button(
            f_inputs, text="Calcular y Graficar", command=resolver,
            bg="#003366", fg="white", font=("Arial", 9, "bold")
        )
        btn.grid(row=0, column=6, rowspan=2, padx=15)

        for e in (e_a, e_b, e_c, e_A, e_B, e_C):
            e.bind("<Return>", resolver)

        resolver()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppCECYTEQ(root)
    root.mainloop()