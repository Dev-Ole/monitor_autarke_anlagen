"""@package docstring
Hauptprogramm
"""
import sys #System lib
import os #Shell Lib
import PyQt5 #PyQt Lib
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

#Eigene Module
import mainwindow
import overview
import weather
from weather import QtGui
import settings
import owm
import sensors
import mysql
import qdialog
import Akkuwerte


#--------------Relais-Initialisieren----------------
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)    #RPI Layout setzten
GPIO.setup(38, GPIO.OUT)    #Relais 1
GPIO.setup(40, GPIO.OUT)    #Relais 2
#---------------------------------------------------

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    # FENSTERNAME(QMainWindow, dateiname.Objektname):
    """Class zum Erzeugung des Hauptfensters"""

    def __init__(self):
        """Constructor"""

        super(self.__class__, self).__init__()
        """Fenster und Widgets initialisieren"""
        self.MainLayout(self)

        self.overview_widget = QWidget()
        self.overview_manager = overview.Ui_Overview()
        self.overview_manager.setupUi(self.overview_widget)

        self.weather_widget = QWidget()
        self.weather_manager = weather.Ui_Weather()
        self.weather_manager.setupUi(self.weather_widget)

        self.settings_widget = QWidget()
        self.settings_manager = settings.Ui_Settings()
        self.settings_manager.setupUi(self.settings_widget)

        self.content.setLayout(QStackedLayout())
        self.content.layout().addWidget(self.overview_widget)
        self.content.layout().addWidget(self.weather_widget)
        self.content.layout().addWidget(self.settings_widget)
        self.setContent(self.overview_widget)

        """Menübutton aktionen"""
        self.m_overview.clicked.connect(lambda: self.setContent(self.overview_widget))
        self.m_overview.clicked.connect(lambda: self.title_bg.setText("Übersicht"))
        self.m_weather.clicked.connect(lambda: self.setContent(self.weather_widget))
        self.m_weather.clicked.connect(lambda: self.title_bg.setText("Wetter"))
        self.m_settings.clicked.connect(lambda: self.setContent(self.settings_widget))
        self.m_settings.clicked.connect(lambda: self.title_bg.setText("Einstellung"))

        """Button aktionen festlegen"""
        self.settings_manager.b_displayoff.clicked.connect(lambda: os.system("xset dpms force off"))
        self.settings_manager.b_shutdown.clicked.connect(lambda: os.system("shutdown -h now"))
        self.settings_manager.b_reboot.clicked.connect(lambda: os.system("shutdown -r now"))

        """QTimer Funktion um Daten konstant zu aktualisieren (Multithreads)"""
        CountMinute = 60*1000
        CountStunde = 60*60*1000
        DialogBatteryLow = 0
        DialogBatteryEmpty = 0

        #Akkuanzeige
        Dialog1 = 0 #LowBattery gesehen?
        Dialog2 = 0 #EmptyBattery gesehen?
        self.BatterieMonitor(Dialog1, Dialog2)
        overviewTimer1 = QTimer(self)
        overviewTimer1.timeout.connect(lambda: self.BatterieMonitor(Dialog1, Dialog2))
        overviewTimer1.start(3000)

        #Overview anzeige
        self.UpdateOverview()
        overviewTimer2 = QTimer(self)
        overviewTimer2.timeout.connect(lambda: self.UpdateOverview())
        overviewTimer2.start(CountStunde)

        #Overview anzeige
        self.UpdateCurrentSensors()
        overviewTimer3 = QTimer(self)
        overviewTimer3.timeout.connect(lambda: self.UpdateCurrentSensors())
        overviewTimer3.start(500)

        #Wetter
        self.UpdateWeather()
        WeatherTimer = QTimer(self)
        WeatherTimer.timeout.connect(lambda: self.UpdateWeather())
        WeatherTimer.start(CountStunde)

        #Settings
        self.UpdateSettings()
        SettingsTimer = QTimer(self)
        SettingsTimer.timeout.connect(lambda: self.UpdateSettings())
        SettingsTimer.start(100)

        #MYSQL
        MYSQLcounter = 0
        MYSQLperiode = 10
        self.UpdateMYSQL(MYSQLperiode, MYSQLcounter)
        MYSQLtimer = QTimer(self)
        MYSQLtimer.timeout.connect(lambda: self.UpdateMYSQL(MYSQLperiode, MYSQLcounter))
        MYSQLtimer.start(CountMinute)

    def setContent(self, widget):
        """Content Widget ändern bei Buttonklick"""
        self.content.layout().setCurrentWidget(widget)

    def BatterieMonitor(self, LowAngezeigt, EmptyAngezeigt):
        """Batterieüberwachung
        Prozentanzeige und Warnmeldungen
        sowie Relaissteuerung bei kritischem Zustand"""
        SensorData = sensors.UpdateSensors()
        self.capacity.setProperty("value", SensorData[5])
        print("LowAnzeige for if: {}".format(LowAngezeigt))
        if(SensorData[5] <= 5):
            GPIO.output(38, GPIO.HIGH) #Licht
            GPIO.output(40, GPIO.HIGH) #Allgemein
            print("System abgeschaltet")
            #qdialog.BatteryEmpty()
            EmptyAngezeigt = 1
        elif(SensorData[5] <= 15):
            GPIO.output(38, GPIO.LOW) #Licht
            energysafer = self.settings_manager.b_energysafer
            if energysafer.isChecked():
                GPIO.output(40, GPIO.LOW) #Allgemein
                LowAngezeigt = 1
                print("kleiner 15 GPIO LOW")
            else:
                #qdialog.BatteryLow()
                GPIO.output(40, GPIO.HIGH)
                LowAngezeigt = 0
                print("kleiner 15 GPIO HIGH")
        elif(SensorData[5] > 15):
            GPIO.output(38, GPIO.LOW) #Licht
            GPIO.output(40, GPIO.LOW) #Allgemein
            LowAngezeigt = 0
            EmptyAngezeigt = 0

    def UpdateOverview(self):
        mysql.askMYSQL()
        """Erzeugung darstellen"""
        self.overview_manager.erz_stunde.setText("%.2f W / Stunde" % mysql.e_leistung_stunde)
        self.overview_manager.erz_tag.setText("%.2f kW / Tag" % mysql.e_leistung_tag)
        self.overview_manager.erz_woche.setText("%.2f kW / Woche" % mysql.e_leistung_woche)
        self.overview_manager.erz_monat.setText("%.2f kW / Monat" % mysql.e_leistung_monat)

        """Verbrauch darstellen"""
        self.overview_manager.ver_stunde.setText("%.2f W / Stunde" % mysql.v_leistung_stunde)
        self.overview_manager.ver_tag.setText("%.2f kW / Tag" % mysql.v_leistung_tag)
        self.overview_manager.ver_woche.setText("%.2f kW / Woche" % mysql.v_leistung_woche)
        self.overview_manager.ver_monat.setText("%.2f kW / Monat" % mysql.v_leistung_monat)


    def UpdateCurrentSensors(self):
        """Aktuelle Erzeugung und Vebrauch anzeigen"""
        SensorData = sensors.UpdateSensors()
        #Sensor DICT [PV_Volt, PV_Ampere, Verb_Volt, Verb_Ampere, AkkuVolt,
        #AkkuProzent, Erz_Leistung, Verb_Leistung]
        self.overview_manager.ver_jetzt.setText("%.3f W / Akutell" % SensorData[7])
        self.overview_manager.erz_jetzt.setText("%.3f W / Akutell" % SensorData[6])
        """Berechnung Akkukapazität"""
        AkkuAmpere = "na"
        while(AkkuAmpere == "na"):
            for position, item in enumerate(Akkuwerte.AkkuVoltlist):
                if item == SensorData[4]:
                    AkkuAmpere = 7 - (Akkuwerte.AkkuZeitlist[position] / 60) * 0.5
                    AkkuAmpere = round(AkkuAmpere,3)
            if AkkuAmpere == "na":
                SensorData[4] = SensorData[4] + 0.01
                SensorData[4] = round(SensorData[4], 2)
        #------------------(Akkuampere + Aktuelle Erz) / Aktuellen Verbrauch
        RestzeitStunden = (AkkuAmpere + SensorData[1]) / SensorData[3]
        RestzeitTage = int(RestzeitStunden / 24)
        RestzeitStunden = RestzeitStunden - (RestzeitTage * 24)
        self.overview_manager.prognose.setText("{:2.0f} Tage {:2.0f} Stunden".format(RestzeitTage, RestzeitStunden))


    def UpdateWeather(self):
        """Neue Wetterdaten einbinden"""
        try:
            owm.data_organizer(owm.data_fetch(owm.url_builder()))
            self.weather_manager.b_refresh_status.setText("Stand: {} Uhr".format(owm.daytime))
            self.weather_manager.b_location.setText(owm.city)
            self.weather_manager.temp.setText("{:2.0f}°C".format(owm.temp[0]))
            self.weather_manager.temp_2.setText("{:2.0f}°C".format(owm.temp[1]))
            self.weather_manager.temp_3.setText("{:2.0f}°C".format(owm.temp[2]))
            self.weather_manager.temp_minmax.setText("({0:2.0f}°-{1:2.0f}°)".format(owm.temp_min[0], owm.temp_max[0]))
            self.weather_manager.temp_minmax_2.setText("({0:2.0f}°-{1:2.0f}°)".format(owm.temp_min[1], owm.temp_max[1]))
            self.weather_manager.temp_minmax_3.setText("({0:2.0f}°-{1:2.0f}°)".format(owm.temp_min[2], owm.temp_max[2]))
            self.weather_manager.wind.setText("{:2.0f} km/h".format(owm.wind[0]))
            self.weather_manager.wind_2.setText("{:2.0f} km/h".format(owm.wind[1]))
            self.weather_manager.wind_3.setText("{:2.0f} km/h".format(owm.wind[2]))
            self.weather_manager.humidity.setText(" {:2.0f} %".format(owm.humidity[0]))
            self.weather_manager.humidity_2.setText(" {:2.0f} %".format(owm.humidity[1]))
            self.weather_manager.humidity_3.setText(" {:2.0f} %".format(owm.humidity[2]))
            self.weather_manager.sunrise.setText("{} Uhr".format(owm.sunrise))
            self.weather_manager.sunset.setText("{} Uhr".format(owm.sunset))

            """Wolken darstellung & Prognose berechnen"""
            #------------Prognose Einstellung--------------""""""
            ProgPanels = []
            ProgWind = []
            ProgErz = []
            sonnenstunden = 9 #Prognose nicht fertig
            windstunden = 20 #Prognose nicht fertig
            panels = float(self.settings_manager.panels.text())
            wind = float(self.settings_manager.wind.text())
            PanelErzTag = panels * sonnenstunden
            WindErzTag = wind * windstunden
            #----------------------------------------------
            clouds = [self.weather_manager.clouds, self.weather_manager.clouds_2, self.weather_manager.clouds_3]
            for i in range(0, 3):
                if((owm.condition[i] >= 200) and (owm.condition[i] < 300)): #Gewitter
                    clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/0.png"))
                    ProgPanels.append(PanelErzTag - (PanelErzTag * 0.9))
                elif((owm.condition[i] <= 300) and (owm.condition[i] < 600)): #Regen
                    clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/11.png"))
                    ProgPanels.append(PanelErzTag - (PanelErzTag * 0.85))
                elif((owm.condition[i] <= 600) and (owm.condition[i] < 700)): #Schnee
                    clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/14.png"))
                    ProgPanels.append(PanelErzTag - (PanelErzTag * 0.6))
                elif((owm.condition[i] <= 700) and (owm.condition[i] < 800)): #Nebel, Rauch, Tornado
                    clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/20.png"))
                    ProgPanels.append(PanelErzTag - (PanelErzTag * 0.92))
                elif(owm.condition[i] >= 800): #Wolken
                    if(owm.condition[i] == 800): #clear
                        clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/32.png"))
                        ProgPanels.append(PanelErzTag - (PanelErzTag * 0.1))
                    elif(owm.condition[i] == 801): #wenig
                        clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/34.png"))
                        ProgPanels.append(PanelErzTag - (PanelErzTag * 0.3))
                    elif(owm.condition[i] == 802): #leicht
                        clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/30.png"))
                        ProgPanels.append(PanelErzTag - (PanelErzTag * 0.5))
                    elif(owm.condition[i] == 803): #mittel
                        clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/28.png"))
                        ProgPanels.append(PanelErzTag - (PanelErzTag * 0.6))
                    elif(owm.condition[i] == 801): #stark
                        clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/26.png"))
                        ProgPanels.append(PanelErzTag - (PanelErzTag * 0.9))
                    else: #Nicht Verfügbar
                        clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/na.png"))
                        ProgPanels.append(0)
                else: #Nicht Verfügbar
                    clouds[i].setPixmap(QtGui.QPixmap(":/weather/img/weather/na.png"))
                    ProgPanels.append(0)

            ProgErz1 = ProgPanels[0] / 24# + ProgWind[0]
            ProgErz2 = ProgPanels[1] / 24# + ProgWind[1]
            ProgErz3 = ProgPanels[2] / 24# + ProgWind[2]
            self.weather_manager.prog_erz.setText("~{:1.0f} KW/h".format(ProgErz1))
            self.weather_manager.prog_erz_2.setText("~{:1.0f} KW/h".format(ProgErz2))
            self.weather_manager.prog_erz_3.setText("~{:1.0f} KW/h".format(ProgErz3))

        except IOError:
            print("Kein internet [WETTER]")
            qdialog.NoInternet()

    def UpdateSettings(self):
        """Energiesparmodus verwalten"""
        energysafer = self.settings_manager.b_energysafer
        if energysafer.isChecked():
            energysafer.setStyleSheet("color: rgb(0, 121, 16);") #Text Grün
            energysafer.setText("Aktivieren")
        elif not energysafer.isChecked():
            energysafer.setStyleSheet("color: rgb(199, 0, 0);") #Text Rot
            energysafer.setText("Deaktivieren")

    def UpdateMYSQL(self, periode, counter):
        SensorData = sensors.UpdateSensors()
        #Sensor DICT [PV_Volt, PV_Ampere, Verb_Volt, Verb_Ampere, AkkuVolt,
        #AkkuProzent, Erz_Leistung, Verb_Leistung]
        if counter < periode:
            SUMvolt = SUMvolt + SensorData[0]
            SUMamp = SUMamp + SensorData[1]
            counter = counter + 1
            print("MYSQL Counter: {}".format(counter))
        elif counter >= periode:
            mysql.SensorEntry(periode, SUMvolt, SUMamp)
            SUMvolt = 0
            SUMamp = 0
            counter = 0

def main():
    """App Instanz erzeugen"""
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    """MainProgramm abruf"""
    main()
