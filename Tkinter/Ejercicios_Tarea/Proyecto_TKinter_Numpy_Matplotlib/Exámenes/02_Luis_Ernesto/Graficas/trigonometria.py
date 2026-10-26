# -*- coding: utf-8 -*-
# MÓDULO DE TRIGONOMETRÍA: calcula triángulos y dibuja su forma con Matplotlib.
# Tkinter presenta campos de captura y resultados; math realiza operaciones trigonométricas.
# Los comentarios explican el propósito de cada sección y los pasos principales.

import tkinter as tk
from tkinter import messagebox
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tolerancia numérica pequeña para comparar resultados de cálculos decimales.
TOL = 1e-7


# Lee cada Entry; un campo vacío se interpreta como dato desconocido.
def _leer_campos(campos):
    """Lee campos opcionales: vacíos significan dato desconocido."""
    datos = {}
    for clave, entrada in campos.items():
        texto = entrada.get().strip().replace(",", ".")
        if texto:
            try:
                valor = float(texto)
            except ValueError:
                raise ValueError(f"El dato '{clave}' debe ser numérico.")
            if not math.isfinite(valor):
                raise ValueError(f"El dato '{clave}' debe ser un número finito.")
            datos[clave] = valor
    return datos


# Revisa que los lados proporcionados sean mayores que cero.
def _validar_positivo(datos, claves):
    for clave in claves:
        if clave in datos and datos[clave] <= 0:
            raise ValueError(f"El valor de {clave} debe ser mayor que cero.")



# Inserta una gráfica de triángulo dentro del formulario de Tkinter.
def _dibujar_triangulo(contenedor, puntos, etiquetas_lados, etiquetas_angulos, titulo):
    """Dibuja el triángulo calculado dentro de la ventana de Tkinter."""
    for widget in contenedor.winfo_children():
        widget.destroy()

    # Crea la figura Matplotlib que se incrustará en la ventana.
    figura = Figure(figsize=(5.0, 2.8), dpi=100)
    # Añade un sistema de ejes para dibujar los tres lados.
    ax = figura.add_subplot(111)
    xs = [puntos[k][0] for k in ("A", "B", "C", "A")]
    ys = [puntos[k][1] for k in ("A", "B", "C", "A")]
    # Une A, B, C y regresa a A para cerrar el triángulo.
    ax.plot(xs, ys, marker="o", linewidth=2)
    ax.set_title(titulo, fontsize=10)

    for nombre in ("A", "B", "C"):
        x, y = puntos[nombre]
        ax.annotate(nombre, (x, y), xytext=(5, 5), textcoords="offset points",
                    fontsize=10, fontweight="bold")

    # Etiquetas de lados, colocadas aproximadamente en el punto medio.
    pares = [("A", "B", "c"), ("B", "C", "a"), ("C", "A", "b")]
    for p1, p2, clave in pares:
        x1, y1 = puntos[p1]
        x2, y2 = puntos[p2]
        texto = etiquetas_lados.get(clave, "")
        ax.text((x1+x2)/2, (y1+y2)/2, texto, fontsize=9,
                bbox=dict(boxstyle="round,pad=0.15", alpha=0.7))

    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.25)
    ax.margins(0.22)
    figura.tight_layout()
    canvas = FigureCanvasTkAgg(figura, master=contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# Abre el formulario de triángulo rectángulo.
def ventana_rectangulo():
    ventana = tk.Toplevel()
    ventana.title("Trigonometría - Triángulo rectángulo")
    ventana.geometry("650x760")
    ventana.resizable(False, False)
    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except Exception:
        pass

    tk.Label(ventana, text="TRIÁNGULO RECTÁNGULO", font=("Arial", 17, "bold")).pack(pady=14)
    tk.Label(
        ventana,
        text="Completa los datos que conozcas. Deja en blanco los desconocidos.\n"
             "Se necesita información suficiente para determinar el triángulo.",
        justify="center"
    ).pack(pady=4)

    marco = tk.Frame(ventana)
    marco.pack(pady=12)
    definiciones = [
        ("Cateto opuesto (a):", "a"),
        ("Cateto adyacente (b):", "b"),
        ("Hipotenusa (c):", "c"),
        ("Ángulo A (grados):", "A"),
    ]
    campos = {}
    for fila, (etiqueta, clave) in enumerate(definiciones):
        tk.Label(marco, text=etiqueta, anchor="e", width=24).grid(row=fila, column=0, padx=6, pady=7, sticky="e")
        entrada = tk.Entry(marco, width=18)
        entrada.grid(row=fila, column=1, padx=6, pady=7)
        campos[clave] = entrada

    resultado = tk.Label(ventana, text="", justify="left", font=("Arial", 11), wraplength=600)
    resultado.pack(pady=5)
    marco_grafica = tk.Frame(ventana, height=270)
    marco_grafica.pack(fill="both", expand=True, padx=12, pady=4)

    # Determina los datos faltantes usando Pitágoras y razones trigonométricas.
    def calcular():
        try:
            d = _leer_campos(campos)
            _validar_positivo(d, ["a", "b", "c"])
            if "A" in d and not (0 < d["A"] < 90):
                raise ValueError("El ángulo A debe estar entre 0° y 90° (sin incluirlos).")

            a, b, c, A = d.get("a"), d.get("b"), d.get("c"), d.get("A")
            conocidos_lados = sum(k in d for k in ("a", "b", "c"))

            # Si se conocen dos lados, calcula el tercero y los ángulos.
            # Resolver con dos lados conocidos.
            if a is not None and b is not None:
                c_calc = math.hypot(a, b)
                A_calc = math.degrees(math.atan2(a, b))
                if c is not None and not math.isclose(c, c_calc, rel_tol=1e-5, abs_tol=1e-5):
                    raise ValueError("Los lados no cumplen el teorema de Pitágoras.")
                if A is not None and not math.isclose(A, A_calc, abs_tol=1e-3):
                    raise ValueError("El ángulo A no coincide con los catetos introducidos.")
                c, A = c_calc, A_calc
            elif a is not None and c is not None:
                if c <= a:
                    raise ValueError("La hipotenusa debe ser mayor que el cateto opuesto.")
                b_calc = math.sqrt(max(0.0, c*c - a*a))
                A_calc = math.degrees(math.asin(a / c))
                if b is not None and not math.isclose(b, b_calc, rel_tol=1e-5, abs_tol=1e-5):
                    raise ValueError("Los lados no cumplen el teorema de Pitágoras.")
                if A is not None and not math.isclose(A, A_calc, abs_tol=1e-3):
                    raise ValueError("El ángulo A no coincide con los lados introducidos.")
                b, A = b_calc, A_calc
            elif b is not None and c is not None:
                if c <= b:
                    raise ValueError("La hipotenusa debe ser mayor que el cateto adyacente.")
                a_calc = math.sqrt(max(0.0, c*c - b*b))
                A_calc = math.degrees(math.atan2(a_calc, b))
                if a is not None and not math.isclose(a, a_calc, rel_tol=1e-5, abs_tol=1e-5):
                    raise ValueError("Los lados no cumplen el teorema de Pitágoras.")
                if A is not None and not math.isclose(A, A_calc, abs_tol=1e-3):
                    raise ValueError("El ángulo A no coincide con los lados introducidos.")
                a, A = a_calc, A_calc
            elif A is not None and a is not None:
                rad = math.radians(A)
                b = a / math.tan(rad)
                c = a / math.sin(rad)
            elif A is not None and b is not None:
                rad = math.radians(A)
                a = b * math.tan(rad)
                c = b / math.cos(rad)
            elif A is not None and c is not None:
                rad = math.radians(A)
                a = c * math.sin(rad)
                b = c * math.cos(rad)
            else:
                raise ValueError("Datos insuficientes. Ingresa dos lados, o un ángulo agudo y un lado.")

            if min(a, b, c) <= 0 or c <= max(a, b):
                raise ValueError("Los datos no forman un triángulo rectángulo válido.")
            # Comprueba que los datos adicionales concuerden con el triángulo calculado.
            # Verificar cualquier dato extra introducido.
            if "a" in d and not math.isclose(d["a"], a, rel_tol=1e-5, abs_tol=1e-5):
                raise ValueError("El cateto opuesto no coincide con los demás datos.")
            if "b" in d and not math.isclose(d["b"], b, rel_tol=1e-5, abs_tol=1e-5):
                raise ValueError("El cateto adyacente no coincide con los demás datos.")
            if "c" in d and not math.isclose(d["c"], c, rel_tol=1e-5, abs_tol=1e-5):
                raise ValueError("La hipotenusa no coincide con los demás datos.")
            if "A" in d and not math.isclose(d["A"], A, abs_tol=1e-3):
                raise ValueError("El ángulo A no coincide con los demás datos.")

            resultado.config(text=(
                "RESULTADOS\n"
                f"Cateto opuesto a = {a:.4g}\n"
                f"Cateto adyacente b = {b:.4g}\n"
                f"Hipotenusa c = {c:.4g}\n"
                f"Ángulo A = {A:.4g}°\n"
                f"Ángulo B = {90 - A:.4g}°\n"
                "Ángulo C = 90°"
            ))
            # A=(0,0), B=(b,0), C=(0,a)
            _dibujar_triangulo(
                marco_grafica,
                {"A": (0, 0), "B": (b, 0), "C": (0, a)},
                {"a": f"a={a:.4g}", "b": f"b={b:.4g}", "c": f"c={c:.4g}"},
                {"A": A, "B": 90-A, "C": 90},
                "Triángulo rectángulo calculado"
            )
        except ValueError as error:
            messagebox.showerror("Datos no válidos", str(error), parent=ventana)

    boton = tk.Button(ventana, text="Calcular", width=20, command=calcular)
    boton.pack(pady=8)
    ventana.bind("<Return>", lambda evento: boton.invoke())


# Abre el formulario de triángulo oblicuángulo (sin ángulo de 90 grados).
def ventana_oblicuangulo():
    ventana = tk.Toplevel()
    ventana.title("Trigonometría - Triángulo oblicuángulo")
    ventana.geometry("680x800")
    ventana.resizable(False, False)
    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except Exception:
        pass

    tk.Label(ventana, text="TRIÁNGULO OBLICUÁNGULO", font=("Arial", 17, "bold")).pack(pady=14)
    tk.Label(
        ventana,
        text="Ingresa los lados a, b, c y/o ángulos A, B, C que conozcas.\n"
             "Cada lado está frente al ángulo con la misma letra.\n"
             "Los ángulos se expresan en grados; deja en blanco lo desconocido.",
        justify="center"
    ).pack(pady=4)

    marco = tk.Frame(ventana)
    marco.pack(pady=12)
    campos = {}
    definiciones = [
        ("Lado a (opuesto a A):", "a"),
        ("Lado b (opuesto a B):", "b"),
        ("Lado c (opuesto a C):", "c"),
        ("Ángulo A (grados):", "A"),
        ("Ángulo B (grados):", "B"),
        ("Ángulo C (grados):", "C"),
    ]
    for fila, (etiqueta, clave) in enumerate(definiciones):
        tk.Label(marco, text=etiqueta, width=24, anchor="e").grid(row=fila, column=0, padx=6, pady=5, sticky="e")
        entrada = tk.Entry(marco, width=18)
        entrada.grid(row=fila, column=1, padx=6, pady=5)
        campos[clave] = entrada

    resultado = tk.Label(ventana, text="", justify="left", font=("Arial", 11), wraplength=640)
    resultado.pack(pady=5)
    marco_grafica = tk.Frame(ventana, height=300)
    marco_grafica.pack(fill="both", expand=True, padx=12, pady=4)

    # Determina los datos faltantes usando Pitágoras y razones trigonométricas.
    def calcular():
        try:
            d = _leer_campos(campos)
            _validar_positivo(d, ["a", "b", "c"])
            for angulo in ("A", "B", "C"):
                if angulo in d and not (0 < d[angulo] < 180):
                    raise ValueError(f"El ángulo {angulo} debe estar entre 0° y 180°.")

            lados = {k: d[k] for k in ("a", "b", "c") if k in d}
            angulos = {k: d[k] for k in ("A", "B", "C") if k in d}

            # Si se conocen dos ángulos, calcular el tercero.
            if len(angulos) >= 2:
                suma = sum(angulos.values())
                if suma >= 180:
                    raise ValueError("La suma de los ángulos conocidos debe ser menor que 180°.")
                faltantes = [k for k in ("A", "B", "C") if k not in angulos]
                if faltantes:
                    angulos[faltantes[0]] = 180 - suma

            # SSS: con tres lados calcular los ángulos por ley de cosenos.
            if len(lados) == 3:
                a, b, c = lados["a"], lados["b"], lados["c"]
                if a + b <= c or a + c <= b or b + c <= a:
                    raise ValueError("Los lados no cumplen la desigualdad triangular.")
                calculados = {
                    "A": math.degrees(math.acos(max(-1, min(1, (b*b + c*c - a*a) / (2*b*c))))),
                    "B": math.degrees(math.acos(max(-1, min(1, (a*a + c*c - b*b) / (2*a*c))))),
                    "C": math.degrees(math.acos(max(-1, min(1, (a*a + b*b - c*c) / (2*a*b))))),
                }
                for k, v in angulos.items():
                    if not math.isclose(v, calculados[k], abs_tol=1e-2):
                        raise ValueError(f"El ángulo {k} no coincide con los tres lados.")
                angulos = calculados

            # Caso SAS: dos lados y el ángulo comprendido.
            if len(lados) >= 2 and len(angulos) >= 1 and len(lados) < 3:
                pares = [("a", "b", "C"), ("a", "c", "B"), ("b", "c", "A")]
                for s1, s2, ang in pares:
                    if s1 in lados and s2 in lados and ang in angulos:
                        v1, v2 = lados[s1], lados[s2]
                        opuesto = {"a": "A", "b": "B", "c": "C"}
                        s3 = next(k for k in ("a", "b", "c") if k not in (s1, s2))
                        lados[s3] = math.sqrt(max(0.0, v1*v1 + v2*v2 - 2*v1*v2*math.cos(math.radians(angulos[ang]))))
                        if lados[s3] <= 0:
                            raise ValueError("Los datos no forman un triángulo válido.")
                        # Recalcular todos los ángulos por SSS
                        a, b, c = lados["a"], lados["b"], lados["c"]
                        angulos = {
                            "A": math.degrees(math.acos(max(-1, min(1, (b*b+c*c-a*a)/(2*b*c))))),
                            "B": math.degrees(math.acos(max(-1, min(1, (a*a+c*c-b*b)/(2*a*c))))),
                            "C": math.degrees(math.acos(max(-1, min(1, (a*a+b*b-c*c)/(2*a*b))))),
                        }
                        break

            # Ley de senos: se requiere al menos un par lado-ángulo opuestos.
            pares_opuestos = [(s, ang) for s, ang in (("a", "A"), ("b", "B"), ("c", "C")) if s in lados and ang in angulos]
            if pares_opuestos:
                s_ref, ang_ref = pares_opuestos[0]
                razon = lados[s_ref] / math.sin(math.radians(angulos[ang_ref]))
                for ang in ("A", "B", "C"):
                    if ang in angulos and angulos[ang] <= 0:
                        raise ValueError("Todos los ángulos deben ser mayores que cero.")
                # Si se conocen todos los ángulos, obtener los lados que falten.
                if len(angulos) == 3:
                    for s, ang in (("a", "A"), ("b", "B"), ("c", "C")):
                        calculado = razon * math.sin(math.radians(angulos[ang]))
                        if s in lados and not math.isclose(lados[s], calculado, rel_tol=1e-5, abs_tol=1e-5):
                            raise ValueError("Los lados y ángulos introducidos son incompatibles.")
                        lados[s] = calculado
                else:
                    for s, ang in (("a", "A"), ("b", "B"), ("c", "C")):
                        if ang in angulos and s not in lados:
                            lados[s] = razon * math.sin(math.radians(angulos[ang]))

            # Caso SSA: intentar obtener ángulos desconocidos por ley de senos.
            changed = True
            while changed:
                changed = False
                pares_opuestos = [(s, ang) for s, ang in (("a", "A"), ("b", "B"), ("c", "C")) if s in lados and ang in angulos]
                if pares_opuestos:
                    s_ref, ang_ref = pares_opuestos[0]
                    razon = lados[s_ref] / math.sin(math.radians(angulos[ang_ref]))
                    for s, ang in (("a", "A"), ("b", "B"), ("c", "C")):
                        if s in lados and ang not in angulos:
                            valor = lados[s] * math.sin(math.radians(ang_ref)) / lados[s_ref]
                            if valor > 1 + 1e-8:
                                raise ValueError("Los datos no pueden formar un triángulo.")
                            valor = max(-1, min(1, valor))
                            candidato = math.degrees(math.asin(valor))
                            otros = [k for k in ("A", "B", "C") if k != ang and k in angulos]
                            if otros and candidato + angulos[otros[0]] >= 180:
                                candidato = 180 - candidato
                            angulos[ang] = candidato
                            changed = True
                            break
                    if changed and len(angulos) == 2:
                        suma = sum(angulos.values())
                        if suma >= 180:
                            raise ValueError("Los ángulos calculados no forman un triángulo válido.")
                        faltante = next(k for k in ("A", "B", "C") if k not in angulos)
                        angulos[faltante] = 180 - suma
                        changed = True

            # Completar lados desde los ángulos y un lado de referencia.
            pares_opuestos = [(s, ang) for s, ang in (("a", "A"), ("b", "B"), ("c", "C")) if s in lados and ang in angulos]
            if len(angulos) == 3 and pares_opuestos:
                s_ref, ang_ref = pares_opuestos[0]
                razon = lados[s_ref] / math.sin(math.radians(angulos[ang_ref]))
                for s, ang in (("a", "A"), ("b", "B"), ("c", "C")):
                    calculado = razon * math.sin(math.radians(angulos[ang]))
                    if s in lados and not math.isclose(lados[s], calculado, rel_tol=1e-5, abs_tol=1e-5):
                        raise ValueError("Los datos introducidos son incompatibles entre sí.")
                    lados[s] = calculado

            if len(lados) != 3 or len(angulos) != 3:
                raise ValueError(
                    "Datos insuficientes o ambiguos. Prueba con tres lados (SSS), "
                    "dos ángulos y un lado, o dos lados y el ángulo comprendido."
                )

            if any(not (0 < angulos[k] < 180) for k in ("A", "B", "C")):
                raise ValueError("Los ángulos calculados no son válidos.")
            if not math.isclose(sum(angulos.values()), 180, abs_tol=1e-2):
                raise ValueError("La suma de los ángulos debe ser 180°; revisa los datos.")
            if lados["a"] + lados["b"] <= lados["c"] or lados["a"] + lados["c"] <= lados["b"] or lados["b"] + lados["c"] <= lados["a"]:
                raise ValueError("Los lados no cumplen la desigualdad triangular.")

            resultado.config(text=(
                "RESULTADOS\n"
                f"Lado a = {lados['a']:.4g}\n"
                f"Lado b = {lados['b']:.4g}\n"
                f"Lado c = {lados['c']:.4g}\n"
                f"Ángulo A = {angulos['A']:.4g}°\n"
                f"Ángulo B = {angulos['B']:.4g}°\n"
                f"Ángulo C = {angulos['C']:.4g}°"
            ))
            # Construcción geométrica con A=(0,0), B=(c,0), AC=b y BC=a.
            a, b, c = lados["a"], lados["b"], lados["c"]
            x_c = (b*b + c*c - a*a) / (2*c)
            y_c = math.sqrt(max(0.0, b*b - x_c*x_c))
            _dibujar_triangulo(
                marco_grafica,
                {"A": (0, 0), "B": (c, 0), "C": (x_c, y_c)},
                {"a": f"a={a:.4g}", "b": f"b={b:.4g}", "c": f"c={c:.4g}"},
                angulos,
                "Triángulo oblicuángulo calculado"
            )
        except ValueError as error:
            messagebox.showerror("Datos no válidos", str(error), parent=ventana)
        except (ZeroDivisionError, OverflowError):
            messagebox.showerror("Error", "Los datos introducidos no permiten calcular un triángulo válido.", parent=ventana)

    boton = tk.Button(ventana, text="Calcular", width=20, command=calcular)
    boton.pack(pady=8)
    ventana.bind("<Return>", lambda evento: boton.invoke())


# Menú inicial que permite elegir qué tipo de triángulo resolver.
def menu_trigonometria():
    ventana = tk.Toplevel()
    ventana.title("Trigonometría")
    ventana.geometry("400x280")
    ventana.resizable(False, False)
    try:
        ventana.iconbitmap("logo_cecyteq.ico")
    except Exception:
        pass

    tk.Label(ventana, text="TRIGONOMETRÍA", font=("Arial", 18, "bold")).pack(pady=28)
    tk.Label(ventana, text="Selecciona el tipo de triángulo:", font=("Arial", 12)).pack(pady=8)
    tk.Button(ventana, text="Triángulo rectángulo", width=25, command=ventana_rectangulo).pack(pady=8)
    tk.Button(ventana, text="Triángulo oblicuángulo", width=25, command=ventana_oblicuangulo).pack(pady=8)
