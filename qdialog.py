import sys
#import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def Sample():
    """Beispiel eines Dialogfensters"""
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    # Warning, Critical, Question, Information
    msg.setText("This is a message box")
    msg.setInformativeText("This is additional information")
    msg.setDetailedText("Detials in message bereich:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setWindowFlags(Qt.FramelessWindowHint) #Titlebar verbergen
    retval = msg.exec_() #Pflicht für Ausführung

def BatteryLow():
    """Warnmeldung bei niedrigen Batteriezustand"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Batterie kapazität ist gering!")
    msg.setInformativeText("Energiesparmodus wurde aktiviert.")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowFlags(Qt.FramelessWindowHint) #Titlebar verbergen
    retval = msg.exec_() #Pflicht für Ausführung

def BatteryEmpty():
    """Warnmeldung bei leerem Batteriezustand"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Die Batterie Leer!")
    msg.setInformativeText("Die Relais wurden abgeschaltet.")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowFlags(Qt.FramelessWindowHint) #Titlebar verbergen
    retval = msg.exec_() #Pflicht für Ausführung

def NoInternet():
    """Warnmeldung wenn kein Internet vorhanden"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Wetterdaten konnten nicht abgerufen werden.")
    msg.setInformativeText("Bitte Internetverbindung überprüfen!")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowFlags(Qt.FramelessWindowHint) #Titlebar verbergen
    retval = msg.exec_() #Pflicht für Ausführung

if __name__ == '__main__':
   Sample()
