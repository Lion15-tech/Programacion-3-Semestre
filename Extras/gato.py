tablero = [
#     0    1    2
    [" ", " ", " "], # 0
    [" ", " ", " "], # 1
    [" ", " ", " "]  # 2
]
#Se usaría tablero[1][1] para acceder al centro por ejemplo

jugador_1 = "X"
jugador_2 = "O"

#Hacemos que el primero en jugar sea el jugador 1
turno_actual = jugador_1

def mostrar_tablero(tablero):
    for y, fila in enumerate(tablero):
        for x, casilla in enumerate(fila):
                print(f"[{casilla}]", end="")
        print()


def comprobar_victoria():
    pass

def juego():
    global turno_actual
    mostrar_tablero(tablero)
    print("Decide donde tirar:")
    while True:
        try:
            fila = int(input("Fila: "))
            columna = int(input("Columna: "))
            if tablero[fila-1][columna-1] ==  " ":
                if turno_actual == jugador_1:
                    tablero[fila-1][columna-1] = f"{jugador_1}"
                    mostrar_tablero(tablero)
                    turno_actual = jugador_2
                else:
                    tablero[fila-1][columna-1] = f"{jugador_2}"
                    mostrar_tablero(tablero)
                    turno_actual = jugador_1
            else:
                print("No puedes tirar en esa casilla")
        except IndexError:
            print("[ERROR] Debe ser una tirada del 1 al 3 ")
juego()