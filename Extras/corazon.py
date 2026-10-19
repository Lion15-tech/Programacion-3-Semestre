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
    #time.sleep(0.5)
    print()


     
print()
for fila in range(10):
    for columna in range(100):
        if columna < 2:
            print("*", end=" ")
        elif columna != 0 and fila in (0,1, 4,5, 8,9) and columna <7:
            print("*", end=" ")
        elif columna in (11,12, 13,14, 15,16) and fila in (0,1):
            print("*", end=" ")
        elif columna in (9, 10) and fila in (2,3):
            print("*", end=" ")
        elif columna in (11,12, 13,14, 15,16) and fila in (4,5):
            print("*", end=" ")
        elif columna in (17,18) and fila in (6,7):
            print("*", end=" ")
        elif columna in (11,12, 13,14, 15,16) and fila in (8,9):
            print("*", end=" ")
        elif columna in (21,22, 23,24, 25,26, 27,28, 29,30) and fila in (0,1):
            print("*", end=" ")
        elif columna in (25, 26):
            print("*", end=" ")
        elif columna in (33,34):
            print("*", end=" ")
        elif columna in (35,36, 37,38) and fila in (4,5):
            print("*", end=" ")
        elif columna in (39, 40):
            print("*", end=" ")
        elif columna in (43, 44):
            print("*", end=" ")
        elif columna != (43,44) and fila in (0,1, 4,5, 8,9) and columna in (45,46, 47,48, 49):
            print("*", end=" ")
        elif columna in (52,53):
            print("*", end=" ")
        elif columna in (54,55, 56,57) and fila in (0,1):
            print("*", end=" ")
        elif columna in (58,59) and fila in (2,3):
            print("*", end=" ")
        elif columna in (54,55, 56,57) and fila in (4,5):
            print("*", end=" ")
        elif columna in (58,59) and fila > 5:
            print("*", end=" ")         


        else:
            print(" ", end=" ")
    #time.sleep(0.5)
    print()        