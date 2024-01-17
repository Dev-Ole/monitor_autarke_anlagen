import spidev
import time
import os
import MySQLdb

global R1
global R2
#------------Settings------------#
R1 = 22000
R2 = 4700
VoltMax = 13.1  #Max Akkuspannung
VoltMin = 11.8  #Min Zul. Akkuspannung
channel1 = 0    #PV_Spannung
channel2 = 1    #PV_Ampere
channel3 = 2    #Verb_Spannung
channel4 = 3    #Verb_Ampere
channel5 = 4    #Akku_Spannung
#--------------------------------#

"""SPI Bus initialisieren"""
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def ReadChannel(channel):
    """Werte der Analog Channels auslesen"""
    adc = spi.xfer2([1, (8+channel)<<4, 0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def ConvertVolt(channel, places):
    """Analogwerte in Spannungs umwandeln"""
    SUMvolt = 0
    SUMdata = 0
    for i in range(0, 100):
        data = ReadChannel(channel)
        voltOffset =  0.028
        volt = (data * 3.3) / float(1023)+voltOffset
        volt = (volt * (R1+R2)) / R2
        SUMvolt = SUMvolt + volt
        SUMdata = SUMdata + data
    volt = SUMvolt / 100
    data = SUMdata / 100
    volt = round(volt, places)
    return (data, volt)

def ConvertAmpere(channel, places):
    """Analogwerte in Ampere umwandeln"""
    SUMamp = 0
    SUMdata = 0
    for i in range(0, 100):
        data = ReadChannel(channel)
        ampOffset = 0.016 #Offset abweichung
        mVproAmp = 0.064  #Ermittelte Volt pro Ampere
        ampere = (data * 3.3) / float(1023)+ampOffset
        #ampere = (ampere-1.65) / mVproAmp
        SUMamp = SUMamp + ampere
        SUMdata = SUMdata + data
    ampere = SUMamp / 100
    data = SUMdata / 100
    #ampere = round(ampere, places)
    return (data, ampere)

def UpdateSensors():
    """Aktuellen Sensorwerte abrufen"""
    voltData, PV_Volt = ConvertVolt(channel1, 2)
    ampereData1, PV_Ampere = ConvertAmpere(channel2, 3)
    voltData2, Verb_Volt = ConvertVolt(channel3, 2)
    ampereData2, Verb_Ampere = ConvertAmpere(channel4, 3)
    voltData3, AkkuVolt = ConvertVolt(channel5, 2)

    Erz_Leistung = PV_Volt * PV_Ampere
    Verb_Leistung = Verb_Volt * Verb_Ampere

    """Spannung der Batterie in Prozent umwandeln"""
    deltaVolt = (VoltMax - VoltMin)
    AkkuProzent = ((AkkuVolt - VoltMin) / deltaVolt) * 100
    AkkuProzent = round(AkkuProzent, 2)
    if (AkkuVolt <= VoltMin):
        AkkuProzent = 0
    if (AkkuVolt >= VoltMax):
        AkkuProzent = 100

    print("--------------------------------------------")
    print("PV Spannung: {} ({}V)".format(voltData, PV_Volt))
    print("PV Strom: {} ({}A)".format(ampereData1, PV_Ampere))
    print("Verb Spannung: {} ({}V)".format(voltData2, Verb_Volt))
    print("Verb Strom: {} ({}A)".format(ampereData2, Verb_Ampere))
    print("Akku Spannung: {} ({}V)".format(voltData3, AkkuVolt))
    print("Akku: {}%".format(AkkuProzent))

    SensorData = [PV_Volt, PV_Ampere, Verb_Volt, Verb_Ampere, AkkuVolt,
    AkkuProzent, Erz_Leistung, Verb_Leistung]
    return SensorData


# ADW (mcp3008) auslesen mit RPi
# https://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008

if __name__ == '__main__':
    UpdateSensors()
