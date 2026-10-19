import time

for fila in range(15):
    for columna in range(18):
        if (fila == 0 or fila == 1) and ((columna > 3 and columna < 8) or (columna > 9 and columna < 14)):
            print("*", end=" ")    
        elif (fila == 2 or fila == 3) and ((columna > 1 and columna < 4) or (columna > 7 and columna < 10) or (columna > 13 and columna < 16)):
            print("*", end=" ")
        elif (fila == 4 or fila == 5 or fila == 6) and ((columna < 2) or (columna > 15)):
            print("*", end=" ")
        elif (fila == 7 or fila == 8) and ((columna > 1 and columna < 4) or (columna > 13 and columna < 16)):
            print("*",end=" ")
        elif (fila == 9 or fila == 10) and ((columna > 3 and columna < 6) or (columna > 11 and columna < 14)):
            print("*", end=" ")
        elif (fila == 11 or fila == 12) and ((columna > 5 and columna < 8) or (columna > 9 and columna < 12)):
            print("*", end=" ")
        elif (fila == 13 or fila == 14) and ((columna > 7 and columna < 10)):
            print("*", end=" ")
        else:        
            print(" ", end=" ")
    time.sleep(0.5)
    print()


     
print()
for fila in range(10):
    for columna in range(8):
        if columna < 2:
            print("*", end=" ")
        elif columna != 0 and fila in (0,1, 4,5, 8,9) and columna <7:
            print("*", end=" ")
        else:
            print(" ", end=" ")
    time.sleep(0.5)
    print()        