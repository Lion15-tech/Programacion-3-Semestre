import tkinter as teca 
import numpy as snumpy 
import boton1
import boton2
import boton3 
import boton4
 
ventana=teca.Tk ()
ventana.geometry ("800x400")
ventana.config (background= "#170000")
ventana.iconbitmap ("l.ico")
bienvenida = teca.Label (ventana,text= "Bienvendido \n ¿Qué tipo de ecuación desea hacer? " ,
                            bg = "#cb7169" ,
                            fg = "#FDFDFD" ,
                            font= ("roman" , 21))
bienvenida.pack (pady = 20)
def seleccion_1 (): 
        ventana.withdraw()
        boton1.ventana_ec1 ()
def seleccion_2 ():
        ventana.withdraw()
        boton2.ventana2()
def seleccion_3 (): 
        ventana.withdraw()
        boton3.ventana3()
def seleccion_4():
        ventana.withdraw()
        boton4.VentAna4()
    

op1 = teca.Button (ventana,text= "grafica de \n ecuacion lineal \n (1er grado) " ,
                        command=seleccion_1 ,
                        bg= "#56070c",
                        font = ("italic" , 16),
                        fg = "#FDFDFD"
                        ) 
op1.place (x= 10 , y=140 )

op2 = teca.Button (ventana,text= "grafica de \n ecuacion cuadratica \n  (2do grado) ",
                        command= seleccion_2 , 
                        bg= "#56070c",
                        fg = "#FDFDFD",
                        font = ("italic" , 16))
op2.place ( x = 200 , y= 140)

op3=teca.Button(ventana,text=" sistema de \n ecuaciones \nlineales ",
                    command=seleccion_3 , 
                    bg= "#56070c",
                    fg = "#FDFDFD" , 
                        font = ("italic" , 16))
op3.place ( x= 440 , y = 140)

op4=teca.Button(text="trigonometria ",
                    command=seleccion_4,
                    bg= "#56070c",
                    fg = "#FDFDFD" , 
                    font = ("italic" , 16))
op4.place(x=600, y=140)




ventana.mainloop ()