import tkinter as teca 
from tkinter import messagebox
import math

def VentAna4 (): 
    ventana4=teca.Tk()
    ventana4.geometry("666x706")
    ventana4.iconbitmap ("l.ico")
    ventana4.config (bg= "#330000")

    tezzzto=teca.Label (ventana4,
        text="función de trigonometria puede elegir entre",
                        bg = "#A55048" ,
                        fg = "#FDFDFD" ,
                        font= ("roman" , 18),
                        pady=5)
    tezzzto.pack()
    def regrezar():
        ventana4.destroy()
        import interfasg_ecuaciones
        interfasg_ecuaciones.ventana.deiconify()

    def rec(): 
        #2 angulos y 3 lados ,la suma del angulo que tenemos y el otro debe dar 90 g
        def enter(event):
            event.widget.tk_focusNext().focus() #evento para q salte de linea 
            return "break"
        
        txt= teca.Label(ventana4,text="introduza los datos que usted conoce de su triangulo ")
        txt.place(x= 10 , y=130)
        htext= teca.Label(ventana4,text="Hipotenusa : ")
        htext.place(x=90 , y=160)
        hipotenusa=teca.Entry (ventana4,width=10)
        hipotenusa.place (x=200 , y=160)
        hipotenusa.bind ("<Return>",enter)

        co= teca.Label(ventana4,text="Cateto opuesto: ")
        co.place (x=90 , y=190)
        catetoop=teca.Entry (ventana4,width=10)
        catetoop.place (x=200 , y=190)
        catetoop.bind ("<Return>",enter)

        catetext = teca.Label(ventana4,text="Cateto adyacante: ")
        catetext.place (x=90 , y=220)
        catetoad=teca.Entry(ventana4,width=10)
        catetoad.place(x=200 , y=220)
        catetoad.bind ("<Return>",enter)

        ang1text= teca.Label (ventana4,text= "Angulo 1: ")
        ang1text.place (x=90 , y=250 )
        angulo1=teca.Entry(ventana4,width=10)
        angulo1.place (x=200 , y=250 )
        angulo1.bind ("<Return>",enter)

        ang2text = teca.Label (ventana4,text="angulo 2: ")
        ang2text.place (x=90 , y= 280)
        angulo2=teca.Entry(ventana4,width=10)
        angulo2.place(x= 200 , y= 280 )
        angulo2.bind ("<Return>",enter)

        mostrar= teca.Text (ventana4,width=40, height=10)
        mostrar.place(x=0 , y=400 )

        def cerote (entry):
            try:
                entrada=entry.get()
                if entrada =="": 
                    return 0
                else:  
                    return float (entrada)
            except: 
                messagebox.showwarning("letras" , "favor de no introduci letras  ")

        def trigonometriajeje ():
            mostrar.delete ("1.0" , teca.END)
            hip=cerote(hipotenusa)
            co=cerote(catetoop)
            ca=cerote(catetoad)
            ang1=cerote(angulo1)
            ang2=cerote(angulo2)
            valores= [hip,co,ca,ang1,ang2]
            # seno = op / hipo 
            #coseno = andaycente/hipo 
            #tangente = opuesto / adya 
            def Operacionezzz ():
                    if hip !=0:  #si tenemos hipotenusa nada mas 
                        if co==0: # si no hay cop ni angulos (solo ca)
                            if ang1==0 and ang2==0: 
                                catetop=(hip**2-ca**2)**(1/2) # 
                                mostrar.insert(teca.END , f"Cateto opuesto: {catetop}\n"  )
                                valorrr= ca/hip
                                radiant=math.radians (valorrr)
                                ang_1ns= math.asin(radiant)
                                mostrar.insert(teca.END , f"angulo: {ang_1ns}\n")
                                B= 90-ang_1ns
                                mostrar.insert(teca.END , f"otro angulo: {B}\n")

                            elif ang1+ang2==90: 
                                    ang=ang1
                                    seno_rad = math.radians(ang) #converti a radientes pa pythonbodrio no puede con grados 
                                    valor_seno = math.sin(seno_rad)  
                                    valor_miki= math.cos(seno_rad)                         
                                    seno=hip*valor_seno
                                    mostrar.insert(teca.END , f"cateto opuesto:{seno}\n")
                                    b=hip*valor_miki
                                    mostrar.insert(teca.END , f"cateto adyacente{b}")
                            elif ang1+ang2>= 90:
                                messagebox.showerror ("angulos" , "la suma de mabos angulos debe ser mayor a 90g ") 
                            else: 
                                ang=ang1 if ang2==0 else ang2
                                seno_radd = math.radians(ang) #converti a radientes pa pythonbodrio no puede con grados 
                                valor_se = math.sin(seno_radd)                           
                                seno=hip*valor_se
                                valo_cos=math.cos(seno_radd)
                                hanya= hip*valo_cos 
                                mostrar.insert(teca.END, f"cateto adyacente: {hanya}")
                                mostrar.insert(teca.END , f"cateto opuesto:{seno}\n")
                                mostrar.insert(teca.END , f"angulo faltante:{90-ang}\n")
                        elif ca == 0:
                            if ang1==0 or ang2==0: 
                                catetoad=(hip**2-co**2)**(1/2)
                                mostrar.insert(teca.END , f"Cateto adyacente: {catetoad}\n")
                                valorrr= co/hip
                                radiant=math.radians (valorrr)
                                ang_1ns= math.asin(radiant)
                                mostrar.insert(teca.END , f"angulo 1: {ang_1ns}\n" )
                                B= 90-ang_1ns
                                mostrar.insert(teca.END , f"otro angulo:{B} \n") #CAH coseno = adyacente / hipo
                            else: 
                                coseno_ang=ang1 if ang2==0 else ang2
                                coseno_rad = math.radians(coseno_ang) #converti a radientes pa pythobodrio no puede con grados 
                                valor_seno = math.cos(coseno_rad)
                                coseno=hip*valor_seno
                                an= 90-ang
                                mostrar.insert(teca.END , f"cateto adyacente: {coseno}\n")
                                mostrar.insert(teca.END , f"angulo faltente :{an}\n" )
                        elif ca==0 and co==0 : 
                            ang=ang1 if ang2==0 else ang2
                            otroang= 90-ang 
                            mostrar.insert(teca.END , f"otro angulo: {otroang}\n")
                            radianteb= math.radians(ang)
                            cop= math.sin(radianteb)
                            capo= hip*cop 
                            mostrar.insert(teca.END, f"cateto opuesto: {capo}\n")
                            valor_coco= math.cos(radianteb)
                            print (valor_coco)
                            cadya= hip*valor_coco
                            mostrar.insert(teca.END , f"cateto adyacente: {cadya}\n")
                     
                    #hipo es cateto/ co o seno grado
                    else:
                        if hip==0:  
                            hipopo=(ca**2+co**2)**(1/2)
                            mostrar.insert(teca.END , f"hipotenusa: {hipopo}\n"   )
                            valor = co/ca 
                            radiante=math.radians (valor )
                            anguloA= math.atan (radiante)
                            mostrar.insert(teca.END , f"Valor del 1er angulo: {anguloA}\n")
                            anguloB =90-anguloA
                            mostrar.insert(teca.END , f"Valor del 2do angulo: {anguloB}\n" )



                        elif co==0 and hip==0:#solo tenemos adyacente y un angulo  asi q usamos coseno 
                            if ang1+ang2==90:
                                angq= ang1
                                raid=math.radians (angq)
                                valor_tan= math.tan(raid)
                                senn= math.sin(raid )
                                caopp= ca/valor_tan
                                señ= ca/ senn
                                mostrar.insert(teca.END , f"cateto opuesto{caopp}")
                                mostrar.insert(teca.END , f" hipotenusa:{señ}")
                            elif ang1+ang2>= 90: 
                                messagebox.showerror ("angulos", "los angulos no deben ser mayores a 90 grados ")
                            else: 
                                angr=ang1 if ang2==0 else ang2
                                radiante = math.radians(angr) #converti a radientes pa pythobodrio no puede con grados 
                                valor_coseno = math.cos(radiante)
                                tangente = math.tan(radiante) 
                                ca_op =ca*tangente                      
                                hipot=ca/valor_coseno
                                triple = 90-ang 
                                mostrar.insert(teca.END , f"cateto opuesto: {ca_op}\n" )
                                mostrar.insert(teca.END, f"hipotenusa  : {hipot}\n")
                                mostrar.insert(teca.END, f"angulo 2 :{triple}\n")
                        elif ca==0 and hip==0: 
                            angm=ang1 if ang2==0 else ang2 
                            radiantezz= math.radians(angm)
                            valor_seno= math.sin(radiantezz)
                            t=math.tan(radiantezz)
                            h=co//valor_seno 
                            ca_ad= co/t
                            mostrar.insert(teca.END, f"hipotenusa: {h}\n")
                            mostrar.insert(teca.END, f"cateto adyacente: {ca_ad}\n")
                         
            Operacionezzz()
                    

        
        
        ns=teca.Button(ventana4,text="mandar" , command=trigonometriajeje) 
        ns.place(x=140 ,y=350)
        
    def obli(): 
        def enter(event):
            event.widget.tk_focusNext().focus() #evento para q salte de linea 
            return "break"
        def caso1 (): 
            tezto=teca.Label (ventana4,text="Caso anguo-angulo y lado \n angulo-lado-angulo ")
            tezto.place(x=450 , y=230)
            té=teca.Label (ventana4,text="Angulo A: ")
            té.place(x=450 , y= 310)
            angulo1= teca.Entry (ventana4,width=8)
            angulo1.place (x= 550 ,  y= 310)
            angulo1.bind ("<Return>",enter)
            t=teca.Label (ventana4,text="Angulo B: ")
            t.place (x=450 , y=340 )
            angulo2=teca.Entry(ventana4,width=8)
            angulo2.place (x=550 , y=340 )
            angulo2.bind ("<Return>",enter)
            roy =teca.Label(ventana4,text="Lado a: ")
            roy.place(x=450 , y=370)
            lado=teca.Entry(ventana4,width=8)
            lado.place(x=550 , y=370)
            lado.bind ("<Return>",enter)
            mostrar=teca.Text (ventana4,width=40, height=10)
            mostrar.place (x=400 , y=430)
            
            
            def valores(entry):
                try:
                    entrada=entry.get()
                    if entrada =="":  
                        return 0
                    else:  
                        return float (entrada)
                except: 
                    messagebox.showwarning("letras" , "favor de no introduci letras  ")
            def trigo_obli(): 
                A=valores(angulo1)
                B=valores(angulo2)
                a=valores(lado)
                print (A,B,a)
                C=180-A-B 
                mostrar.insert(teca.END, f"angulo C: {C}\n")
                radinateA=math.radians(A)
                radianteB=math.radians(B)
                radianteC=math.radians(C)
                senoA= math.sin(radinateA)
                senoB=math.sin(radianteB)
                senoC=math.sin(radianteC)            
                ladob= a*senoB//senoA
                mostrar.insert(teca.END , f"Lado b:{ladob}\n")
                ladoc= a*senoC/senoA
                mostrar.insert(teca.END, f"lado c: {ladoc} \n")
            limon = teca.Button(ventana4,text="mandar" , command=trigo_obli)
            limon.place(x=550 , y=400)

        def caso2(): 
            tezto= teca.Label(ventana4,text="Caso lado-angulo-lado")
            tezto.place(x=450 , y=230)
            té=teca.Label (ventana4,text="Lado a: ")
            té.place(x=450 , y= 310)
            lado1= teca.Entry (ventana4,width=8)
            lado1.place (x= 550 ,  y= 310)
            lado1.bind ("<Return>",enter)
            t= teca.Label (ventana4,text="Lado b: ")
            t.place (x=450 , y=340 )
            lado2=teca.Entry(ventana4,width=8)
            lado2.place (x=550 , y=340 )
            lado2.bind ("<Return>",enter)
            roy =teca.Label(ventana4,text="Angulo C : ")
            roy.place(x=450 , y=370)
            angulo=teca.Entry (ventana4,width=8)
            angulo.place (x=550 , y=370)
            angulo.bind ("<Return>",enter)
            mostrar=teca.Text (ventana4,width=40, height=10)
            mostrar.place (x=400 , y=430)
            def valores(entry):
                try:
                    entrada=entry.get()
                    if entrada =="":  
                        return 0
                    else:  
                        return float (entrada)
                except: 
                        messagebox.showwarning("letras" , "favor de no introduci letras  ") 
            def trigo_obli():
                mostrar.delete ("1.0" , teca.END)
                a=valores(lado1)
                b=valores(lado2)
                C=valores(angulo)
                radianteC=math.radians(C)
                cosenoC=math.cos(radianteC) 
                ladoc=a**2+b**2-2*a*b*cosenoC
                c=ladoc**(1/2)
                mostrar.insert("1.0" , "lado c: {c}" )

                ang_2=(b**2+c**2-a**2)/(2*b*c)
                mostrar.insert(teca.END, f"Lado faltante : {ang_2}")
                radianteA=math.asin(ang_2)
                arcos=math.degrees(radianteA)
                mostrar.insert(teca.END, f"angulo A: {arcos}" )

                B=180-arcos-C
                mostrar.insert(teca.END, f"angulo faltante: {B}" )

            limon = teca.Button(ventana4,text="mandar" , command=trigo_obli)
            limon.place(x=550 , y=400)

        def caso3(): 
            tezto=teca.Label(ventana4,text="Lado-Lado-Lado")
            tezto.place (x=450 , y= 230)
            té=teca.Label (ventana4,text="Lado a: ")
            té.place(x=450 , y= 310)
            lado1= teca.Entry (ventana4,)
            lado1.bind ("<Return>",enter)
            lado1.place (x= 550 ,  y= 310)
            t= teca.Label (ventana4,text="Lado b: ")
            t.place (x=450 , y=340 )
            lado2=teca.Entry(ventana4,)
            lado2.bind ("<Return>",enter)
            lado2.place (x=550 , y=340 )
            roy =teca.Label(ventana4,text="Lado c: ")
            roy.place(x=450 , y=370)
            lado3=teca.Entry (ventana4,)
            lado3.bind ("<Return>",enter)
            lado3.place (x=550 , y=370)
            mostrar=teca.Text (ventana4,width=40, height=10)
            mostrar.place (x=400 , y=430)

            def valores(entry):
                try:
                    entrada=entry.get()
                    if entrada =="":  
                        return 0
                    else:  
                        return float (entrada)
                except: 
                    messagebox.showwarning("letras" , "favor de no introduci letras  ")
            def trigo_obli(): 
                
                a=valores(lado1)
                b=valores(lado2)
                c=valores(lado3)
                valor= (b**2+c**2-a**2)/(2*b*c)
                radiantes=math.acos(valor)
                A=math.degrees(radiantes)
                mostrar.insert(teca.END , f"angulo A: {A}")
                valorB=(a**2+c**2-b**2)/ (2*a*c)
                radiante=math.asin(valorB)
                B= math.degrees(radiante)
                mostrar.insert(teca.END, f"angulo B: {B}" )

                C=180-A-B
                mostrar.insert(teca.END, f"angulo C: {C}" )
            limon = teca.Button(ventana4,text="mandar" , command=trigo_obli)
            limon.place(x=550, y=400)

        def caso4(): 
            tezto= teca.Label (ventana4,text="Lado-angulo opuesto ")
            tezto.place (x=450 , y=230 )
            té=teca.Label (ventana4,text="Lado a: ")
            té.place(x=450 , y= 310)
            lado1= teca.Entry (ventana4,)
            lado1.place (x= 550 ,  y= 310)
            lado1.bind ("<Return>",enter)
            t= teca.Label (ventana4,text="Lado b: ")
            t.place (x=450 , y=340 )
            lado2=teca.Entry(ventana4,)
            lado2.place (x=550 , y=340 )
            lado2.bind ("<Return>",enter)
            roy =teca.Label(ventana4,text="Angulo A: ")
            roy.place(x=450 , y=370)
            angulo=teca.Entry (ventana4,)
            angulo.place (x=550 , y=370)
            angulo.bind ("<Return>",enter)
            mostrar=teca.Text (ventana4,width=40, height=10)
            mostrar.place (x=550 , y=430)

            def valores(entry):
                try:
                    entrada=entry.get()
                    if entrada =="":  
                        return 0
                    else:  
                        return float (entrada)
                except: 
                        messagebox.showwarning("letras" , "favor de no introduci letras  ")
                
            def trigo_obli(): 
                mostrar.delete ("1.0" , teca.END)
                a=valores(lado1)
                b=valores(lado2)
                A=valores(angulo)
                print (a,b,A)
                radiante=math.radians(a)
                seno=math.sin(radiante)
                h=b*seno
                print (h)

                if a <=h : 
                    print ("no")
                elif a==h: 
                    print ("su triangulo es un triangulo rectangulo ")

                else: 
                    radiantes=math.radians(A)
                    senoA=math.sin(radiantes)
                    valorA=(b*senoA)/a
                    radiante=math.asin(valorA)
                    B= math.degrees(radiante)
                    mostrar.insert(teca.END, f"angulo b: {B}" )
                    C=180-A-B
                    radi=math.radians(C)
                    senoC= math.sin(radi)
                    mostrar.insert(teca.END,f"Angulo C: {C}")
                    c = a*senoC / senoA
                    mostrar.insert(teca.END, f"Lado c: {c}")
               

             
            limon = teca.Button(ventana4,text="mandar" , command=trigo_obli)
            limon.place(x=200 , y=300)

        def caso5():
            messagebox.showerror ("aviso" ," No es posibble resolver este triangulo , hay infinitos tamaños " ) 
       



        c1=teca.Button (ventana4,text= "Caso AAL o ALA" , command=caso1)
        c1.place(x=450 , y= 130)
        c2=teca.Button (ventana4,text= "Caso LAL" , command=caso2)
        c2.place(x=550 , y=130)
        c3=teca.Button(ventana4,text="Caso LLL",command=caso3)
        c3.place(x=450 , y=160)
        c4=teca.Button(ventana4,text=" Caso LLA" , command=caso4)
        c4.place(x=550 , y=160)
        c5=teca.Button (ventana4,text=" Caso AAA" , command=caso5)
        c5.place(x=450 , y=190)
        
        pass 

    botonrectangulo = teca.Button(ventana4,text= "trinagulo rectangulo " ,command=rec )
    botonoblicuangulo = teca.Button(ventana4,text="trinagulo oblicuángulo" ,command=obli)
    botonregrezzzo= teca.Button(ventana4,text="regresar al menú" , command=regrezar , 
                                bg="#330000" , fg="#F5F5F5")
    botonregrezzzo.place (x=5 , y= 50)
    botonrectangulo.place(x= 100 , y=90)
    botonoblicuangulo.place (x=450 , y=90)
    ventana4.mainloop()

VentAna4()




