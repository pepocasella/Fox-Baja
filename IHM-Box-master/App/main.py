from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore, QtWidgets
from MainWindow import Ui_MainWindow

import serial.tools.list_ports
from datetime import datetime
import csv
import webbrowser

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Variáveis do programa
        self.deviceName = None
        self.devicePort = 9600
        self.recordReport = False
        self.receiveDataFlag = True
        self.speedMax = 0
        self.speedAcc = 0
        self.rpmMax = 0
        self.rpmAcc = 0
        self.distanceAcc = 0
        self.dataCounter = 0
        self.lastData = None
        self.filename = None
        self.corruptedData = 0

        self.showSerialDevices()
        self.listHelpOptions()
        self.show()

        self.actionStart.triggered.connect(self.startReport)
        self.actionStop.triggered.connect(self.stopReport)
        self.actionDisconnect.triggered.connect(self.disconnectDevice)
        self.actionStop.triggered.connect(self.stopReport)

    def listHelpOptions(self):
        how_works = QAction("Como funciona", self)
        how_works.triggered.connect(self.openHelp)
        self.menuHelp.addAction(how_works)

    def openHelp(self):
        url = "https://github.com/FoxBaja/IHM-Box/blob/master/README.md"
        webbrowser.open_new_tab(url)

    def consolePrint(self, text):
        item = QtWidgets.QListWidgetItem()
        item.setText(text)
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.console.addItem(item)

    def cleanConsole(self):
        self.console.clear()

    def resetGlobalVars(self):
        self.lastData = [0, 0, 0, 0, datetime.now()]
        self.speedMax = 0
        self.speedAcc = 0
        self.rpmMax = 0
        self.rpmAcc = 0
        self.distanceAcc = 0
        self.dataCounter = 0

    def showSerialDevices(self):
        for element in serial.tools.list_ports.comports():
            device_button = QAction('{}'.format(element.device), self)
            device_button.triggered.connect(lambda checked, device=element.device: self.connectDevice(device))
            self.menuConnect.addAction(device_button)

    def setState(self, state):
        if state == "Disconnected":
            self.menuConnect.setEnabled(True)
            self.actionStart.setEnabled(False)
            self.actionStop.setEnabled(False)
            self.actionDisconnect.setEnabled(False)
        if state == "Connected":
            self.menuConnect.setEnabled(False)
            self.actionStart.setEnabled(True)
            self.actionStop.setEnabled(False)
            self.actionDisconnect.setEnabled(True)
        if state == "Running":
            self.menuConnect.setEnabled(False)
            self.actionStart.setEnabled(False)
            self.actionStop.setEnabled(True)
            self.actionDisconnect.setEnabled(True)

    def connectDevice(self, device):
        self.deviceName = device
        self.setState("Connected")
        self.consolePrint("Dispositivo na porta {} selecionado".format(device))
        self.consolePrint(" ")
        self.consolePrint("Recebendo dados...")
        self.consolePrint("Para salvá-los, inicie um relatório em Arquivo > Iniciar")
        self.consolePrint(" ")
        self.receiveData()

    def disconnectDevice(self):
        self.receiveDataFlag = False
        self.deviceName = None
        self.resetGlobalVars()
        self.cleanDisplayData()
        self.consolePrint("Dispositivo desconectado, selecione outro dispositivo")
        self.setState("Disconnected")
    
    def calculateDistance(self, newData):
        deltaTime = (newData[4] - self.lastData[4]).seconds/3600
        deltaSpeed = (newData[0] + self.lastData[0])/2
        distance = deltaSpeed * deltaTime
        self.distanceAcc += distance

    def displayData(self, data):
        speed, battery, rpm, gasoline, timestamp = data

        self.dataCounter += 1
        self.rpmAcc += rpm
        self.speedAcc += speed
        rpm_mean = self.rpmAcc/self.dataCounter
        speed_mean = self.speedAcc/self.dataCounter

        if speed > self.speedMax:
            self.lcd_speed_max.setProperty("value", speed)
            self.speedMax = speed

        if rpm > self.rpmMax:
            self.lcd_rpm_max.setProperty("value", rpm)
            self.rpmMax = rpm

        self.calculateDistance(data)

        self.lcd_rpm_value.setProperty("value", rpm)
        self.lcd_speed_value.setProperty("value", speed)
        self.lcd_rpm_mean.setProperty("value", rpm_mean)
        self.lcd_speed_mean.setProperty("value", speed_mean)
        self.progress_battery.setProperty("value", battery)
        self.progress_gasoline.setProperty("value", gasoline)
        self.lcd_distance.setProperty("value", self.distanceAcc)

        self.lastData = data

    def cleanDisplayData(self):
        self.lcd_rpm_value.setProperty("value", 0)
        self.lcd_speed_value.setProperty("value", 0)
        self.lcd_rpm_mean.setProperty("value", 0)
        self.lcd_speed_mean.setProperty("value", 0)
        self.progress_battery.setProperty("value", 0)
        self.lcd_speed_max.setProperty("value", 0)
        self.lcd_rpm_max.setProperty("value", 0)
        self.progress_gasoline.setProperty("value", 0)
        self.lcd_distance.setProperty("value", 0)

    def receiveData(self):
        self.resetGlobalVars()
        inBuffer = serial.Serial(self.deviceName, self.devicePort)
        while self.receiveDataFlag:
            QtCore.QCoreApplication.processEvents()
            if inBuffer.in_waiting != 0:
                data = inBuffer.readline().decode('utf-8').strip('\r\n').split(';')
                if len(data) == 6 and data[0] == "Fox":
                    formated_data = [int(float(i)) for i in data[1:5]]
                    formated_data.append(datetime.now())
                    if self.recordReport:
                        date = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
                        self.writeReport(formated_data, date)
                    else:
                        pass
                    self.displayData(formated_data)
                else:
                    self.corruptedData += 1

    def startReport(self):
        self.setState("Running")
        self.resetGlobalVars()
        self.cleanDisplayData()
        self.filename = QFileDialog.getSaveFileName(self, 'Save File')
        if self.filename[0] == '':
            self.consolePrint("Operação cancelada, tente novamente")
            pass
        else:
            self.consolePrint("Arquivo criado com sucesso")
            self.consolePrint("Gravando dados...")
            with open(self.filename[0]+'.csv', mode='w') as csvfile:
                vehicle_data = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                vehicle_data.writerow(['Speed', 'Battery', 'RPM', 'Gasoline', 'Distance', 'Date(DD/MM/YY - HH:MM:SS)'])
                self.recordReport = True

    def writeReport(self, data, date):
        with open(self.filename[0]+'.csv', mode='a') as csvfile:
            vehicle_data = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            vehicle_data.writerow([data[0], data[1], data[2], data[3], round(self.distanceAcc,3), date])

    def stopReport(self):
        self.setState("Connected")
        self.recordReport = False
        self.consolePrint(" ")
        self.consolePrint("Relatório terminado")
        self.consolePrint("Relatório salvo em: {}.csv".format(self.filename[0]))
        self.consolePrint("Pacotes recebidos corrompidos: {}".format(self.corruptedData))

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("IHM - Fox Baja")
    window = MainWindow()
    app.exec_()