# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overview.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Overview(object):
    def setupUi(self, Overview):
        Overview.setObjectName("Overview")
        Overview.resize(761, 371)
        Overview.setAutoFillBackground(False)
        self.erz_stunde = QtWidgets.QLabel(Overview)
        self.erz_stunde.setGeometry(QtCore.QRect(20, 140, 201, 41))
        self.erz_stunde.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.erz_stunde.setObjectName("erz_stunde")
        self.line_4 = QtWidgets.QFrame(Overview)
        self.line_4.setGeometry(QtCore.QRect(500, 10, 20, 341))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.erz_monat = QtWidgets.QLabel(Overview)
        self.erz_monat.setGeometry(QtCore.QRect(20, 290, 201, 41))
        self.erz_monat.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.erz_monat.setObjectName("erz_monat")
        self.ver_stunde = QtWidgets.QLabel(Overview)
        self.ver_stunde.setGeometry(QtCore.QRect(300, 140, 201, 41))
        self.ver_stunde.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.ver_stunde.setObjectName("ver_stunde")
        self.ver_monat = QtWidgets.QLabel(Overview)
        self.ver_monat.setGeometry(QtCore.QRect(300, 290, 201, 41))
        self.ver_monat.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.ver_monat.setObjectName("ver_monat")
        self.line_5 = QtWidgets.QFrame(Overview)
        self.line_5.setGeometry(QtCore.QRect(240, 10, 20, 341))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.erz_woche = QtWidgets.QLabel(Overview)
        self.erz_woche.setGeometry(QtCore.QRect(20, 240, 201, 41))
        self.erz_woche.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.erz_woche.setObjectName("erz_woche")
        self.b_erzeugung = QtWidgets.QPushButton(Overview)
        self.b_erzeugung.setGeometry(QtCore.QRect(20, 10, 211, 51))
        self.b_erzeugung.setStyleSheet("font: 75 18pt \"Noto Sans\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/system/img/system/if_solar_64682.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_erzeugung.setIcon(icon)
        self.b_erzeugung.setIconSize(QtCore.QSize(30, 30))
        self.b_erzeugung.setObjectName("b_erzeugung")
        self.b_prognose = QtWidgets.QPushButton(Overview)
        self.b_prognose.setGeometry(QtCore.QRect(530, 10, 211, 51))
        self.b_prognose.setStyleSheet("font: 75 18pt \"Noto Sans\";")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/system/img/system/if_gnome-session-reboot_28664.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_prognose.setIcon(icon1)
        self.b_prognose.setIconSize(QtCore.QSize(30, 30))
        self.b_prognose.setObjectName("b_prognose")
        self.b_verbrauch = QtWidgets.QPushButton(Overview)
        self.b_verbrauch.setGeometry(QtCore.QRect(270, 10, 221, 51))
        self.b_verbrauch.setStyleSheet("font: 75 18pt \"Noto Sans\";")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/system/img/system/if_Light_bulb_653262.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_verbrauch.setIcon(icon2)
        self.b_verbrauch.setIconSize(QtCore.QSize(30, 30))
        self.b_verbrauch.setObjectName("b_verbrauch")
        self.ver_tag = QtWidgets.QLabel(Overview)
        self.ver_tag.setGeometry(QtCore.QRect(300, 190, 201, 41))
        self.ver_tag.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.ver_tag.setObjectName("ver_tag")
        self.ver_woche = QtWidgets.QLabel(Overview)
        self.ver_woche.setGeometry(QtCore.QRect(300, 240, 201, 41))
        self.ver_woche.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.ver_woche.setObjectName("ver_woche")
        self.erz_tag = QtWidgets.QLabel(Overview)
        self.erz_tag.setGeometry(QtCore.QRect(20, 190, 201, 41))
        self.erz_tag.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.erz_tag.setObjectName("erz_tag")
        self.prognose = QtWidgets.QLabel(Overview)
        self.prognose.setGeometry(QtCore.QRect(540, 90, 201, 41))
        self.prognose.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.prognose.setObjectName("prognose")
        self.erz_jetzt = QtWidgets.QLabel(Overview)
        self.erz_jetzt.setGeometry(QtCore.QRect(20, 90, 201, 41))
        self.erz_jetzt.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.erz_jetzt.setObjectName("erz_jetzt")
        self.ver_jetzt = QtWidgets.QLabel(Overview)
        self.ver_jetzt.setGeometry(QtCore.QRect(300, 90, 201, 41))
        self.ver_jetzt.setStyleSheet("font: 75 16pt \"Noto Sans\";")
        self.ver_jetzt.setObjectName("ver_jetzt")

        self.retranslateUi(Overview)
        QtCore.QMetaObject.connectSlotsByName(Overview)

    def retranslateUi(self, Overview):
        _translate = QtCore.QCoreApplication.translate
        Overview.setWindowTitle(_translate("Overview", "Form"))
        self.erz_stunde.setText(_translate("Overview", "000 W / Stunde"))
        self.erz_monat.setText(_translate("Overview", "000 kW / Monat"))
        self.ver_stunde.setText(_translate("Overview", "000 W / Stunde"))
        self.ver_monat.setText(_translate("Overview", "000 kW / Monat"))
        self.erz_woche.setText(_translate("Overview", "000 kW / Woche"))
        self.b_erzeugung.setText(_translate("Overview", "Erzeugung"))
        self.b_prognose.setText(_translate("Overview", "Prognose"))
        self.b_verbrauch.setText(_translate("Overview", "Verbrauch"))
        self.ver_tag.setText(_translate("Overview", "000 kW / Tag"))
        self.ver_woche.setText(_translate("Overview", "000 kW / Woche"))
        self.erz_tag.setText(_translate("Overview", "000 kW / Tag"))
        self.prognose.setText(_translate("Overview", "1 Tag 8 Stunden"))
        self.erz_jetzt.setText(_translate("Overview", "000 W / Aktuell"))
        self.ver_jetzt.setText(_translate("Overview", "000 W / Aktuell"))

import resources_rc
