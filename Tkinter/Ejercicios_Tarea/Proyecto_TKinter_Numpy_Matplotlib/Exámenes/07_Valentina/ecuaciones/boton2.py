import tkinter as teca 
from tkinter import messagebox
import matplotlib.pyplot as yuka
import numpy

f1 ="#170000"
f2 ="#62162f"
f3 ="#96305a"
f4 ="#9b5973"
f5="#ff9fc5"
blanco="#FAFAFA"
f6="#cfb9a0"


def ventana2():
    ventana2g = teca.Toplevel ()
    ventana2g.geometry ("444x666")
    ventana2g.config (bg= "#330000")
    ventana2g.iconbitmap ("l.ico")

    def enter(event):
        event.widget.tk_focusNext().focus() #evento para q salte de linea 
        return "break"
    def regrezar():
        ventana2g.destroy()
        import interfasg_ecuaciones
        interfasg_ecuaciones.ventana.deiconify()

    datos = teca.Label (ventana2g,text= "Grafica de ecuacion de segundo grado \n Ax*2 + Bx + c = 0 ", 
                        bg = f2,
                        font=("roman" , 18), 
                        fg=blanco
                        )
    datos.pack (pady=20)
    textox = teca.Label (ventana2g,text= "Introduzca valor de A " , 
                         bg= f4,
                         fg=blanco)
    textox.pack()
    AV=teca.IntVar ()
    A= teca.Entry (ventana2g ,bg=f6,
                   textvariable=AV,
                    font= ("roman" , 15))
    A.pack ()
    A.bind ("<Return>",enter)
    textox = teca.Label (ventana2g,text= "Introduzca valor de B ",
                         bg= f4,
                         fg=blanco )
    textox.pack ()
    BV=teca.IntVar ()
    B= teca.Entry (ventana2g , textvariable=BV, 
                    font= ("roman" , 15))
    B.pack ()
    B.bind ("<Return>",enter)
    textox = teca.Label (ventana2g,text= " Introduzca el valor de C ",
                         bg= f4,
                        fg=blanco ) 
    textox.pack ()
    CV=teca.IntVar ()
    C = teca.Entry (ventana2g , textvariable=CV ,
                    font= ("roman" , 15) , 
                    bg= f6)
    C.pack ()
    C.bind ("<Return>",enter)

    def X (): #soluciones de la ecuacion 
            dentro_raiz=(BV.get()**2)-4*AV.get()*CV.get ()
            raiz = dentro_raiz ** (1/2)
            x1 = (-BV.get () + raiz)/ (2*AV.get())
            print ("x1" , x1)
            x2 = (-BV.get() - raiz)/(2*AV.get())
            print ("x2", x2)

    def ecuacion (event=None): #esta funcion hace la ecuacion y grafica  
        if AV.get()==0:
            messagebox.showinfo("ceros" , " AVISO su gragica saldra recta no una parabola   ")
        else: 
            #primero los vertices de x y Y que son basicamente el punto mas bajo de la parabola , aqui empieza tokio 
            vertice_x= -BV.get()/(2*AV.get()) #vertice de x, su formula es -b/2xa , 
            vertice_y= AV.get()*(vertice_x**2)+BV.get()*vertice_x+CV.get() #vertice Y,formula de Y solo q sustituyes por x_vertice 
            xi=vertice_x-5 
            xf=vertice_x+5 #inicio y final parq se vea en todo jeje
            x=numpy.linspace(xi,xf, 100) #inicio,fin y 100 puntos , x son los direnetes puntos que tandra la parabola 
            y=AV.get()*(x**2)+BV.get()*x+CV.get()#calculo de y , Y son los punyos verticales 
            yuka.plot (x, y , color= "yellow" , label=f" formula \n Y= {AV.get()}x^2 + ({BV.get()})x + ({CV.get()})") #plot crea la parabola  
            yuka.plot (vertice_x , vertice_y,
                    label=f"Coordenada del vertice X: ({vertice_x},\nCoordenada del vertice Y {vertice_y})") #este crea un widgetsito q muestra el vertice 
            yuka.legend()
            yuka.show() #chow ps lo mantiene en pantallla , es un mainlopp2.0
            ventana2g.destroy()
            import interfasg_ecuaciones
            interfasg_ecuaciones.ventana.deiconify()
    botoñ = teca.Button (ventana2g,text= "click para graficar jeje" , command=ecuacion ,
                         bg=f2 ,fg=blanco)
    
    botonregreSO= teca.Button(ventana2g,text="regresar al menú " ,command=regrezar,
                                bg= "#330000" , fg= "#fefefe" , font = ("georgia" , 12))
    botonregreSO.place (x=5 , y=70 )

    ventana2g.bind ("<Return>",ecuacion)
    botoñ.pack (pady= 5)
    ventana2g.mainloop ()




#formula general -b+- raiz de b*2 - 4ac / 2a