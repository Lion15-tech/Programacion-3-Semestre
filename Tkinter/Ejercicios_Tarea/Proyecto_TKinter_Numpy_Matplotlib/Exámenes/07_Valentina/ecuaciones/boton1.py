import tkinter as teca  
import matplotlib.pyplot as yuka
import numpy as np
f1 ="#170000"
f2 ="#62162f"
f3 ="#96305a"
f4 ="#9b5973"
f5="#ff9fc5"
blanco="#FAFAFA"
f6="#cfb9a0"

def ventana_ec1 (): 
    ventana1g = teca.Toplevel()
    ventana1g.geometry ("444x666")
    ventana1g.config (bg= "#330000")
    ventana1g.iconbitmap ("l.ico")
    

    def enter(event):
        event.widget.tk_focusNext().focus() #evento para q salte con enter 
        return "break"
    def regrezar():
            ventana1g.destroy()
            import interfasg_ecuaciones
            interfasg_ecuaciones.ventana.deiconify()
        

    bienvenida= teca.Label (ventana1g,text= " ☆⋆｡°‧★ִ ࣪.˖ ࣪ wꫀᥣᥴ᥆ꩇꫀ ! ᰔ ִ ׄ ☆.｡°‧★ \n intruduzca 2 pares odenados para graficar su ecuacion: " , 
                            bg = f2,
                            fg = blanco,
                            font= ("Georgia" , 13))
    bienvenida.pack(pady=5) 
    texto1= teca.Label (ventana1g,text="par ordenado 1 " , 
                        bg= f4,
                        fg=blanco)
    texto1.pack()
    Xpar1=teca.Entry (ventana1g,
                      bg=f6)
    Xpar1.pack()
    Xpar1.bind ("<Return>",enter)
    Ypar1=teca.Entry(ventana1g,)
    Ypar1.pack()
    Ypar1.bind ("<Return>",enter)

    texto2= teca.Label(ventana1g,text="par ordenado 2 " , 
                        bg= f4,
                        fg=blanco)
    texto2.pack()
    Xpar2=teca.Entry (ventana1g,
                      bg=f6)
    Xpar2.pack()
    Xpar2.bind ("<Return>",enter)
    Ypar2=teca.Entry(ventana1g,)
    Ypar2.pack()
    Ypar2.bind ("<Return>",enter)
    def valores_numericosjeje (event=None): 
        xp1= int(Xpar1.get())
        xp2= int(Xpar2.get())
        yp1= int(Ypar1.get())
        yp2= int(Ypar2.get())
    
        pendiente=yp2 - yp1 / xp2-xp1
        print (pendiente)
            #y=mx+b 
            #ejemplo jeje 4x-2 = 8  
            #4 es x y 2 es Y ,  ax+by = c ,  Y =mx + b , m=y2-y1/x2-x1
        A = np.array([xp1,xp2]) #vector    
        B = np.array([yp1,yp2]) #matriz 
        yuka.plot (A,B,marker="*" ,
        label= f"pendiente de la recta {pendiente} \n par 1: {xp1,yp1} par 2: {xp2,yp2}" ,
                    color="#952B2B") #crea la grafica ,
        yuka.legend ()
        yuka.grid ()
        yuka.show ()
        ventana1g.destroy()
        import interfasg_ecuaciones
        interfasg_ecuaciones.ventana.deiconify()
        
       
    botonmandar= teca.Button (ventana1g,text= "graficar" ,
                               command=valores_numericosjeje ,
                               bg=f2 ,fg=blanco)
    botonregreso=teca.Button(ventana1g,text="regresar al menú" ,
                              command=regrezar)
    botonregreso.place (x=5 , y=50 )
    ventana1g.bind ("<Return>",valores_numericosjeje)
    botonmandar.pack()
    ventana1g.mainloop()

