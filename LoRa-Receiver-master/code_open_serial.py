# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:19:26 2018

@author: Pedro Casella
"""

import serial

lista_velocidade = []
lista_bateria = []
lista_rpm = []
lista_gasolina_sensor_1 = []
lista_gasolina_sensor_2 = []

lista_dados = []

arduinoData = serial.Serial("COM7", 9600)

while True:
    while (arduinoData.inWaiting()==0):
        
        pass
    
    arduinoString = arduinoData.readline().decode().strip('\r\n')
    
    lista_dados.append(arduinoString)
    lista_dados = arduinoString.split(';')
    del lista_dados[0]
    
    print("nova info:")
    print(arduinoString)
    print(lista_dados)
    print("fim")
    
    
    
    
    

  

    
    
    