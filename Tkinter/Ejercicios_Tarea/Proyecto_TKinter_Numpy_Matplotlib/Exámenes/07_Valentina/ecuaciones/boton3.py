import tkinter as teca 
import numpy as nn
import matplotlib.pyplot as mate
from tkinter import messagebox
f1 ="#170000"
f2 ="#62162f"
f3 ="#96305a"
f4 ="#9b5973"
f5="#ff9fc5"
blanco="#FAFAFA"
f6="#cfb9a0"
def ventana3(): 
    ventana3g = teca.Toplevel() #ventana secundaria en vez de tk q es la principal 
    ventana3g.geometry ("666x706")
    ventana3g.iconbitmap ("l.ico")
    ventana3g.config (bg= "#330000")
    opciones = ["2x2", "3x3"]
    textox = teca.Label (ventana3g,text= ". ݁ ˖๋ ࣭ ⭑¿Qué tipo de ecucion lineal desea hacer ? (2x2 o 3x3). ݁ ˖๋ ࣭ ⭑" , 
                        bg = "#cb7169" ,
                        fg = "#FDFDFD" ,
                        font= ("georgia" , 15) , 
                        pady=5)
    textox.pack ()
    def enter(event):
        event.widget.tk_focusNext().focus() #evento para q salte de linea 
        return "break"
    def regrezar():
        ventana3g.destroy()
        import interfasg_ecuaciones
        interfasg_ecuaciones.ventana.deiconify()
    def dospordos ():
        boton3x3.config(state=teca.DISABLED)
        textox= teca.Label(ventana3g,text= "Ecuación de 2x2 Introduzca los valores necesarios" ,
                            bg = f2,
                            font=("roman" , 18), 
                            fg=blanco)
        textox.place(x=90 , y=100)
        ajeje=teca.Label(ventana3g,text="Valor de A:" ,  
                         bg= f4,
                        fg=blanco)
        ajeje.place(x=160,y=180)
        Aec1=teca.Entry (ventana3g,width=7)
        Aec1.place (x=240, y=180)
        Aec1.bind ("<Return>",enter)

        bjeje=teca.Label(ventana3g,text="Valor de B:",
                         bg= f4,
                        fg=blanco)
        bjeje.place(x=320,y=180)
        Bec1=teca.Entry(ventana3g,width=7)
        Bec1.place(x=400 , y= 180)
        Bec1.bind("<Return>",enter)

        cjeje=teca.Label(ventana3g,text="Valor de C:" ,
                         bg= f4,
                        fg=blanco)
        cjeje.place(x=480,y=180)
        Cec1=teca.Entry(ventana3g, width=7)
        Cec1.place (x=560, y=180)
        Cec1.bind ("<Return>",enter)

        testo= teca.Label(ventana3g,text= "valores de la segunda ecuacion " ,
                        bg = f2,
                        font=("georgia" , 15), 
                        fg=blanco)
        testo.place (x=270 , y= 240)
        Ajeje=teca.Label(ventana3g,text="Valor de A:" ,
                         bg= f4,
                        fg=blanco)
        Ajeje.place(x=160,y=300)
        Aec2=teca.Entry (ventana3g,width=5)
        Aec2.place (x=240 , y=300)
        Aec2.bind ("<Return>",enter)

        Bjeje=teca.Label(ventana3g,text="Valore de B:",
                         bg= f4,
                        fg=blanco)
        Bjeje.place(x=320 ,y=300)
        Bec2=teca.Entry(ventana3g,width=5)
        Bec2.place(x=400 , y= 300)
        Bec2.bind("<Return>",enter)

        Cjeje=teca.Label(ventana3g,text="Valor de C:" ,
                         bg= f4,
                        fg=blanco)
        Cjeje.place(x=480,y=300)
        Cec2=teca.Entry(ventana3g,width=5)
        Cec2.place (x=560, y=300)
        Cec2.bind ("<Return>",enter)


        lizzz= [textox,testo , Ajeje ,ajeje,Bjeje,bjeje,Cjeje,
        cjeje,Aec1,Aec2,Bec1,Bec2,Cec1,Cec2 ,]
        def valorrrr(entry): 
            try:
                entrada=entry.get()
                if entrada =="":  
                    return 0
                else:  
                    return float (entrada)
            except: 
                messagebox.showwarning("letras" , "favor de no introduci letras  ")
        def resolverjeje (event=None): 
            boton3x3.config(state=teca.NORMAL)
            A1= valorrrr(Aec1)
            B1 =valorrrr(Bec1)
            C1= valorrrr(Cec1)
            A2= valorrrr(Aec2)
            B2= valorrrr(Bec2)
            C2= valorrrr(Cec2)
                
            A=nn.array([
                        [A1,B1],
                        [A2,B2]
                        ])
            
            B=nn.array([C1,C2])

            solucioñ = nn.linalg.solve(A, B) #esto resuelve toda esa ecuacion 
            print ("valor de X: " , solucioñ[0])
            print ("Valoe de Y: " , solucioñ[1])
                    #creamoszz la graficaaaa
            xini= solucioñ[0]-5
            xfin=solucioñ[0]+5

            Y = nn.linspace(xini,xfin, 100)
            # Despejamos y: y = (c - a*x)/b
            y1 = (C1 - A1*Y)/B1
            y2 = (C2 - A2*Y)/B2
            mate.plot(Y, y1 , label= f"Ecuación 1\n A y B {A}            C {B}" ,
                      color="#892494")
            mate.plot(Y, y2,label=f"Ecuación 2" , color="#86B95F" )
            mate.xlabel("lado X")
            mate.ylabel("Lado Y")
            mate.grid()
            mate.scatter(solucioñ[0] , solucioñ[1] ,
                         label=f"punto de interseccion\n {solucioñ} " ,
                         color= "#A40707")
            mate.legend()
            mate.show()
            for widget in lizzz  :
                widget.destroy()
            

        botongraf = teca.Button(ventana3g,text="graficar" , command=resolverjeje ,
                                bg= f6,
                                font = ("georgia" , 12))
        ventana3g.bind("<Return>",resolverjeje)
        botongraf.place(x= 350 , y= 370)
    def tresxtres(): 
        boton2x2.config(state=teca.DISABLED)
        testo3=teca.Label(ventana3g,text="Ecuación de 3x3 \nfavor de introducir todos los valores necesarios " ,
        bg = f2,
        font=("roman" , 18), 
        fg=blanco )
        testo3.place(x=100 ,y=100)
        # 2x + y - z = 2
        # x -2y + z = 3
        # 3x + y +2z =11
        tt= teca.Label(ventana3g,text="x1: " , 
                        bg= f4,
                        fg=blanco)
        tt.place (x=140 , y=170)
        valorx1= teca.Entry (ventana3g,width=9 , 
                            bg= f6)
        valorx1.place (x=180 , y= 170)
        valorx1.bind ("<Return>",enter)

        qua=teca.Label(ventana3g,text="Y1: ",
                        bg= f4,
                        fg=blanco)
        qua.place (x=260 , y=170)
        valory1=teca.Entry (ventana3g,width=9 , bg= f6)
        valory1.place (x=300 , y= 170)
        valory1.bind ("<Return>",enter)


        www= teca.Label(ventana3g,text="Z1: " ,
                        bg= f4,
                        fg=blanco)
        www.place (x=380 , y=170)
        valorz1=teca.Entry (ventana3g,width=9 , bg= f6)
        valorz1.place (x=420 , y= 170)
        valorz1.bind ("<Return>",enter)


        ci= teca.Label(ventana3g,text="b1: " , 
                        bg= f4,
                        fg=blanco)
        ci.place (x=500 , y=170)
        valora1=teca.Entry (ventana3g,width=9 , bg= f6)
        valora1.place (x=540 , y= 170)
        valora1.bind ("<Return>",enter)

        #.place (x=0 , y=0)

        s=teca.Label (ventana3g,text="X2: " , 
                        bg= f4,
                         fg=blanco)
        s.place (x=140 , y=200)
        valorx2=teca.Entry(ventana3g,width=9)
        valorx2.place (x=180 , y=200)
        valorx2.bind ("<Return>",enter)


        ka=teca.Label (ventana3g,text="Y2: " , 
                        bg= f4,
                        fg=blanco)
        ka.place (x=260 , y=200)
        valory2=teca.Entry(ventana3g,width=9)
        valory2.place (x=300 , y=200)
        valory2.bind ("<Return>",enter)


        se=teca.Label(ventana3g,text="Z2: " , 
                        bg= f4,
                         fg=blanco)
        se.place (x=380 , y=200)
        valorz2=teca.Entry(ventana3g,width=9)
        valorz2.place (x=420 , y=200)
        valorz2.bind ("<Return>",enter)


        ta= teca.Label(ventana3g,text=" B2: " , 
                        bg= f4,
                        fg=blanco)
        ta.place (x=500 , y= 200)
        valora2=teca.Entry(ventana3g,width=9)
        valora2.place (x=540 , y=200)
        valora2.bind ("<Return>",enter)

        #fkkkkk 


        say=teca.Label (ventana3g,text="X3: " , 
                        bg= f4,
                         fg=blanco)
        say.place (x=140 , y=230)
        valorx3=teca.Entry(ventana3g,width=9 , bg= f6)
        valorx3.place (x=180 , y=230)
        valorx3.bind ("<Return>",enter)


        you=teca.Label (ventana3g,text="Y3: " , 
                        bg= f4,
                        fg=blanco)
        you.place (x=260 , y=230)
        valory3=teca.Entry(ventana3g,width=9, bg= f6)
        valory3.place (x=300 , y=230)
        valory3.bind ("<Return>",enter)


        bo=teca.Label(ventana3g,text="Z3: " , 
                        bg= f4,
                        fg=blanco)
        bo.place (x=380 , y=230)
        valorz3=teca.Entry(ventana3g,width=9, bg= f6)
        valorz3.place (x=420 , y=230)
        valorz3.bind ("<Return>",enter)


        dy= teca.Label(ventana3g,text=" B3: " ,
                        bg= f4,
                        fg=blanco)
        dy.place (x=500 ,y= 230)
        valora3=teca.Entry(ventana3g,
                           width=9, bg= f6)
        valora3.place (x=540 , y=230)
        valora3.bind ("<Return>",enter)
        lista_w= [valora1,valora2,valora3,valorx1,valorx2,valorx3,
        valory1,valory2,valory3,valorz1,valorz2,valorz3 ,
        tt , www,ci,testo3 ,s,ka,se,ta,se,you,bo,dy ,bo,qua , say]

        def valores (entry): 
            try:
                entrada=entry.get()
                if entrada =="":  
                    return 0
                else:  
                    return float (entrada)
            except: 
                messagebox.showwarning("letras" , "favor de no introduci letras  ")
        try:        
            def calculo (): 
                boton2x2.config(state=teca.NORMAL)
                x1=valores(valorx1)
                y1= valores(valory1)
                z1=valores(valorz1)
                a1=valores(valora1)
                x2=valores(valorx2)
                y2=valores(valory2)
                z2=valores(valorz2)
                a2=valores(valora2)
                x3=valores(valorx3)
                y3=valores(valory3)
                z3=valores(valorz3)
                a3=valores(valora3)
                print (x1,y1,z1,a1,x2,y2,z2,a2,x3,y3,z3,a3,)

                matrizA= nn.array ([[x1,y1,z1],
                                    [x2,y2,z2],
                                    [x3,y3,z3]])
                
                matrizB = nn.array ([a1,a2,a3])
                print (matrizA)
                print (matrizB)

                solufin= nn.linalg.solve(matrizA, matrizB)
                print (f"resultado de x:{solufin [0]}")
                print (f"resultado de Y: {solufin[1]}")
                print (f"resultado de Z: {solufin[2]}")

                for widget in lista_w : 
                    widget.destroy()

                figurin= mate.figure()
                tresD = figurin.add_subplot(projection='3d')
                
                iniciox= solufin[0]-5
                finx=solufin[1]+5
                inicioy= solufin[0]-1
                finy=solufin[1]+1
                x=nn.linspace(iniciox , finx , 20)
                y=nn.linspace(inicioy,finy,20)

                X,Y= nn.meshgrid (x,y)
                ZZZ= solufin[2]-X-Y
                tresD.plot_surface (x,y,ZZZ)
                mate.show()
        
            # X ancho ,f
            # Y  porfundidad
            # Z altura 

            okey = teca.Button (ventana3g,text="graficar" , command= calculo ,
                                bg=f2 ,fg=blanco,
                                padx=10 , pady=2 ,
                                font= ("Georgia" , 9))
            
            ventana3g.bind("<Return>",calculo)
            okey.place(x= 350 , y= 370)
        except: 
            messagebox.showwarning ("campos" , "porfavor complete todos los ") 

    boton2x2 = teca.Button (ventana3g,text= "ecuacion de 2x2" , command=dospordos , 
                            bg= f6,
                            font = ("georgia" , 12))
    boton2x2.place (x= 200 , y= 50) 

    boton3x3 = teca.Button (ventana3g,text=" ecuacion de 3x3" , command=tresxtres , 
                            bg= f6,
                            font = ("georgia" , 12))

    boton3x3.place (x= 400 , y= 50)

    botonreg= teca.Button (ventana3g , text="regresar al menú" ,command=regrezar ,
                           bg= "#330000",
                           fg="#FAFAFA",
                            font = ("georgia" , 12))
    botonreg.place (x= 5 , y= 50)

    ventana3g.mainloop ()







