print("Ecuación 1:")
coeficiente_X_1 = int(input("Ingresa el coeficiente de X: "))
coeficiente_Y_1 = int(input("Ingresa el coeficiente de Y: "))
resultado_1 = int(input("Ingresa el resultado de la ecuación: "))
print(f"Ecuación 1: {coeficiente_X_1}X + {coeficiente_Y_1}Y = {resultado_1}")

print("\nEcuación 2:")
coeficiente_X_2 = int(input("Ingresa el coeficiente de X: "))
coeficiente_Y_2 = int(input("Ingresa el coeficiente de Y: "))
resultado_2 = int(input("Ingresa el resultado de la ecuación: "))
print(f"Ecuación 2: {coeficiente_X_2}X + {coeficiente_Y_2}Y = {resultado_2}")

def calcular_determinante(a, b, c, d):
    M = (a*d) - (b*c)
    return M

def coseguir_valor_X(Mx, M):
    x = Mx/M
    return x

def conseguir_valor_Y(My, M):
    y = My/M
    return y


#Resultados:
#x:
resultado_X = coseguir_valor_X(calcular_determinante(resultado_1, coeficiente_Y_1, resultado_2, coeficiente_Y_2), 
                        calcular_determinante(coeficiente_X_1, coeficiente_Y_1, coeficiente_X_2, coeficiente_Y_2))

#Y:
resultado_Y = conseguir_valor_Y(calcular_determinante(coeficiente_X_1, resultado_1, coeficiente_X_2, resultado_2),
                        calcular_determinante(coeficiente_X_1, coeficiente_Y_1, coeficiente_X_2, coeficiente_Y_2))

print(f"El valor de X es: {resultado_X}")
print(f"El valor de Y es: {resultado_Y}")

#Comprobación:
ecuacion_1_completa = (coeficiente_X_1*resultado_X) + (coeficiente_Y_1*resultado_Y)
ecuacion_2_completa = (coeficiente_X_2*resultado_X) + (coeficiente_Y_2*resultado_Y)

if round(ecuacion_1_completa, 2) == resultado_1 and round(ecuacion_2_completa, 2) == resultado_2:
    print("Todo correcto!")
else:
    print("hay un error")