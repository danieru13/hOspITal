import paho.mqtt.client as mqtt
import time
from tkinter import *


class Gui:
    def __init__(self, master):
        self.master = master
        master.title("Hospital")
        master.geometry('500x200')
        # Le da color al fondo
        master.config(bg="White")
        #boton de salida del programa
        self.salida_programa = Button(False, text="CERRAR", command=master.quit)
        self.salida_programa.grid(row=1, column =1)
        #boton de informacion actual de los sensores
        self.informacion_sensores = Button(False, text="informacion", command=self.informacion)
        self.informacion_sensores.grid(row=0, column =2)
        #definimos la informacion de los sensores

        #definimos si es automatico o manual
        # para automatico
        self.automatico_programa = Button(master, text="automatico", command=self.automatico)
        self.automatico_programa.grid(row=0, column =0)
        #self.automatico_radio = tk.Radiobutton(master,text='automatico', command=self.automatico)
        # para manual
        self.manual_ventilador = Button(master, text="manual", command=self.manual)
        self.manual_ventilador.grid(row=0, column =1)

        #Variables cliente MQTT
        self.ledState = False
        self.fanState = False
        self.windowState = False
        self.broker_IP = "localhost"                # Modificar
        self.topics = ["hospital/room/light", "hospital/room/tmp", "hospital/room/fan", "hospital/room/window", "hospital/room/motion"]
        self.commands = ["ON","OFF", "OPEN", "CLOSE"]

         # cliente mqtt
        CLIENT_ID = "lis01"
        self.mqttc=mqtt.Client(client_id=CLIENT_ID)
        self.mqttc.connect(self.broker_IP, 1883, 60)

        # Iniciando el loop infinito     del cliente mqtt
        self.mqttc.loop_start() 


    #metodos
   
    #metodo funcion manual
    def manual(self):
        window = Tk()
        window.title("hospital")
        window.geometry('500x100')
        window.config(bg="White")
        #texto de ventilador, ventana y luz
        self.ventilador = Label(window, text="VENTILADOR",bg= "White", fg="red")
        self.ventilador.grid(row=0, column =0)
        self.ventana = Label(window, text="VENTANA", bg= "White", fg="blue")
        self.ventana.grid(row=0, column =1)
        self.luz = Label(window, text="LUZ", bg= "White", fg="azure4")
        self.luz.grid(row=0, column =2)
        #botones de ventilador, encendido y apagado
        self.prender_ventilador = Button(window, text="ON", command=self.on_off_fan,bg= "red1", fg="black")
        self.prender_ventilador.grid(row=2, column =0)
        self.apagar_ventilador = Button(window, text="OFF", command=self.on_off_fan,bg= "red2", fg="black")
        self.apagar_ventilador.grid(row=3, column =0)
        #boton para abrir ventana y cerrar ventana
        self.abrir_ventana = Button(window, text="OPEN", command=self.on_off_window, fg="black")
        self.abrir_ventana.grid(row=2, column =1)
        self.cerrar_ventana = Button(window, text="CLOSE", command=self.on_off_window, fg="black")
        self.cerrar_ventana.grid(row=3, column =1)
        #Botones para prender y apagar la luz
        self.on_luz = Button(window, text="ON", command=self.on_off_light, bg= "azure1", fg="black")
        self.on_luz.grid(row=2, column =2)
        self.of_luz = Button(window, text="OFF", command=self.on_off_light, bg= "azure2", fg="black")
        self.of_luz.grid(row=3, column =2)
        
        #metodo funcion automatico
    def automatico(self):
        print("automatico!")
    def informacion(self):
        self.temperatura = Label(False, text="la temperatura es: "+"30",bg= "White")
        self.temperatura.grid(row=2, column =3)
        self.movimiento = Label(False, text="sensor de movimiento: "+"sin",bg= "White")
        self.movimiento.grid(row=3, column =3)
        self.ventilador = Label(False, text="ventilador: "+"prendido",bg= "White")
        self.ventilador.grid(row=4, column =3)
        self.ventana = Label(False, text="ventana: "+"abierta",bg= "White")
        self.ventana.grid(row=5, column =3)

    def on_off_light(self):
        if self.ledState == False:
            #self.ser.write('h'.encode("ascii","ignore")) 
            self.on_luz.config(text = "ON")
            self.luz.config(text = "Lampara apagada")
            self.mqttc.publish(self.topics[0],self.commands[0])  # Uso de publish para 
                                                                 # prender la lampara
            self.ledState = True
        else:
            #self.ser.write('l'.encode("ascii","ignore"))
            self.of_luz.config(text = "OFF")
            self.mqttc.publish(self.topics[0],self.commands[1])  # Uso de publish para 
                                                                 # apagar la lampara
            self.luz.config(text = "Lampara encendida")
            self.ledState = False

    def on_off_fan(self):
        if self.fanState == False:
            #self.ser.write('h'.encode("ascii","ignore")) 
            self.prender_ventilador.config(text = "ON")
            self.ventilador.config(text = "Ventilador apagado")
            self.mqttc.publish(self.topics[2],self.commands[0])  # Uso de publish para 
                                                                 # prender la lampara
            self.fanState = True
        else:
            #self.ser.write('l'.encode("ascii","ignore"))
            self.apagar_ventilador.config(text = "OFF")
            self.mqttc.publish(self.topics[2],self.commands[1])  # Uso de publish para 
                                                                 # apagar la lampara
            self.ventilador.config(text = "Ventilador encendido")
            self.fanState = False

    def on_off_window(self):
        if self.windowState == False:
            #self.ser.write('h'.encode("ascii","ignore")) 
            self.abrir_ventana.config(text = "OPEN")
            self.ventana.config(text = "Ventana cerrada")
            self.mqttc.publish(self.topics[3],self.commands[2])  # Uso de publish para 
                                                                 # prender la lampara
            self.windowState = True
        else:
            #self.ser.write('l'.encode("ascii","ignore"))
            self.cerrar_ventana.config(text = "CLOSE")
            self.mqttc.publish(self.topics[3],self.commands[3])  # Uso de publish para 
                                                                 # apagar la lampara
            self.ventana.config(text = "Ventana abierta")
            self.windowState = False
        
    
root = Tk()
my_gui = Gui(root)
root.mainloop()