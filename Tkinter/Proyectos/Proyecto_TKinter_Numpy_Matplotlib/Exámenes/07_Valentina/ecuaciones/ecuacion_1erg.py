
#import numpy as alexksyntek 
import tkinter as teca  
import matplotlib.pyplot as yuka
import numpy as np

def bad(): 
    ventana1g = teca.Toplevel ()
    ventana1g.geometry ("444x666")
    ventana1g.config (bg= "#330000")
    ventana1g.iconbitmap ("l.ico")
    a = []
    b = []
    c =[]

    datos =teca.Label (ventana1g,
                    text= "Grafica de ecuacion de primer grado \n ax + b = 0" , 
                    bg = "#62162f" , 
                    fg = "#FAF7F7" 
                    )
    datos.pack () 
    #ejemplo jeje 4x-2 = 8  
    #4 es x y 2 es Y       ax+by = c       Y =mx + b 
    textox = teca.Label (ventana1g,
                        text= "Introduzca primer valor (a) " ,
                        bg = "#62162f" , 
                        fg = "#FAF7F7"  , 
                        )
    textox.pack ()
    ints=teca.IntVar ()
    v1 = teca.Entry (ventana1g ,bg= "#CE9DA5" , textvariable=ints)
    v1.pack ()


    textox = teca.Label (ventana1g,
                        text= "Introduzca segundo valor (b)" , 
                        bg = "#62162f" , 
                        fg = "#FAF7F7" ,)
    textox.pack ()
    para2=teca.IntVar ()
    v2= teca.Entry (ventana1g ,bg= "#CE9DA5" , textvariable=para2)
    v2.pack ()


    textox = teca.Label (ventana1g,
                        text= " Introduzca el resultado " , 
                        bg = "#62162f" , 
                        fg = "#FAF7F7" ,)
    textox.pack ()
    para3=teca.IntVar ()
    resultado = teca.Entry (ventana1g , bg= "#CE9DA5" ,textvariable=para3)
    resultado.pack ()
    # solucion y graficazzz 
    def ecuacion (): 
        a=ints.get ()
        b=para2.get ()
        c=para3.get ()
        despeje=c-(b)
        print ("depejeje" , despeje)
        encontrarx =despeje/a
        print ("resultado de X: ", encontrarx)
        

        # Matriz de coeficientes (A)
        A = np.array([0,encontrarx]) #vector 

        # Vector de términos independientes (B)
        B = np.array([0,b]) #matriz 
        yuka.plot (A,B , marker="*" ,label=f"coordenada X {encontrarx} \n coordenada Y {b}") #crea la grafica ,
        yuka.legend ()
        yuka.show () #muestra el resultado 
    botont= teca.Button (ventana1g,text= "mandar" , command=ecuacion)
    botont.pack ()
    ventana1g.mainloop()

'''
A= alexksyntek.array ([
    [v1.get () , v2.get ()],
])
B = alexksyntek.array ([resultado.get ()])

solucion = alexksyntek.linalg.solve (A,B)
print (solucion)
ventana1g.mainloop ()'''