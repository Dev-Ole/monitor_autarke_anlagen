import MySQLdb

def askMYSQL():
    """Mit Datenbank verbinden"""
    db = MySQLdb.connect("localhost", "USERNAME", "PASSOWRD!", "project")
    # Mysqldb.connect("HOST, USER, PW, DATABASE")
    curs = db.cursor()

    """Datenbankabfrage der Mittelwerte"""
    #---------------------ERZEUGUNG-----------------------#
    curs.execute("SELECT AVG(leistung) FROM erzeugung WHERE date >= CURRENT_TIMESTAMP - INTERVAL 1 HOUR")
    for leistung in curs.fetchone():
        global e_leistung_stunde
        e_leistung_stunde = leistung
        if e_leistung_stunde == None:
            e_leistung_stunde = 0

    curs.execute("SELECT AVG(leistung) FROM erzeugung WHERE date >= CURRENT_TIMESTAMP - INTERVAL 24 HOUR")
    for leistung in curs.fetchone():
        global e_leistung_tag
        e_leistung_tag = leistung
        if e_leistung_tag == None:
            e_leistung_tag = 0
        elif e_leistung_tag > 0:
            e_leistung_tag = e_leistung_tag/1000

    curs.execute ("SELECT AVG(leistung) FROM erzeugung WHERE date >= CURRENT_TIMESTAMP - INTERVAL 7 DAY")
    for leistung in curs.fetchone():
        global e_leistung_woche
        e_leistung_woche = leistung
        if e_leistung_woche == None:
            e_leistung_woche = 0
        elif e_leistung_woche > 0:
            e_leistung_woche = e_leistung_woche/1000

    curs.execute ("SELECT AVG(leistung) FROM erzeugung WHERE date >= CURRENT_TIMESTAMP - INTERVAL 30 DAY")
    for leistung in curs.fetchone():
        global e_leistung_monat
        e_leistung_monat = leistung
        if e_leistung_monat == None:
            e_leistung_monat = 0
        elif e_leistung_monat > 0:
            e_leistung_monat = e_leistung_monat/1000

    #---------------------VERBRAUCH-----------------------#
    curs.execute("SELECT AVG(leistung) FROM verbrauch WHERE date >= CURRENT_TIMESTAMP - INTERVAL 1 HOUR")
    for leistung in curs.fetchone():
        global v_leistung_stunde
        v_leistung_stunde = leistung
        if v_leistung_stunde == None:
            v_leistung_stunde = 0

    curs.execute("SELECT AVG(leistung) FROM verbrauch WHERE date >= CURRENT_TIMESTAMP - INTERVAL 24 HOUR")
    for leistung in curs.fetchone():
        global v_leistung_tag
        v_leistung_tag = leistung
        if v_leistung_tag == None:
            v_leistung_tag = 0
        elif v_leistung_tag > 0:
            v_leistung_tag = v_leistung_tag/1000

    curs.execute ("SELECT AVG(leistung) FROM verbrauch WHERE date >= CURRENT_TIMESTAMP - INTERVAL 7 DAY")
    for leistung in curs.fetchone():
        global v_leistung_woche
        v_leistung_woche = leistung
        if v_leistung_woche == None:
            v_leistung_woche = 0
        elif v_leistung_woche > 0:
            v_leistung_woche = v_leistung_woche/1000

    curs.execute ("SELECT AVG(leistung) FROM verbrauch WHERE date >= CURRENT_TIMESTAMP - INTERVAL 30 DAY")
    for leistung in curs.fetchone():
        global v_leistung_monat
        v_leistung_monat = leistung
        if v_leistung_monat == None:
            v_leistung_monat = 0
        elif v_leistung_monat > 0:
            v_leistung_monat = v_leistung_monat/1000

    #-----Ampere/Tag------#
    curs.execute("SELECT AVG(leistung) FROM verbrauch WHERE date >= CURRENT_TIMESTAMP - INTERVAL 24 HOUR")
    for strom in curs.fetchone():
        global v_ampere_tag
        v_ampere_tag = strom
        if v_ampere_tag == None:
            v_ampere_tag = 0

def SensorEntry(periode, SUMvolt, SUMamp):
    """Addieren der Sensorwerte im Minutentakt ausgelöst durch QTimer->UpdateMYSQL im Main.py
    Stündlicher Eintrag in die MYSQL Datenbank"""
    try:
            volt = SUMvolt / periode
            amp = SUMamp / periode
            leistung = volt * amp
            db = MySQLdb.connect("localhost", "Ole", "IchmagBrot!", "project")
            # Mysqldb.connect("HOST, USER, PW, DATABASE")
            curs = db.cursor()
            curs.execute("INSERT INTO erzeugung (date, volt, ampere, leistung) VALUES (CURRENT_TIMESTAMP, %.2f, %.2f, %.2f);" % (spannung, strom, leistung))
            db.commit()
            print("Eintrag erstellt! [Erzeugung MYSQL]\n")
    except:
            print("Error. Rolling back.\n!")
            db.rollback()

# #----------------------Beispiel Eintrag erstellen---------------------#
# try:
#     spannung = 12
#     strom = 9
#     leistung = (spannung * strom)
#     curs.execute("INSERT INTO erzeugung (date, volt, ampere, leistung) VALUES (CURRENT_TIMESTAMP, %.2f, %.2f, %.2f);" % (spannung, strom, leistung))
#     db.commit()
#     print("Eintrag erstellt [MYSQL.py]!\n")
# except:
#     print("Error. Rolling back.\n!")
#     db.rollback()

#z.B SELECT spalte1, spalte2 FROM tabelle ORDER BY vornamen
# #---------------------------------------------------------------------#

# ---------------------------ABFRAGE BEISPIEL---------------------------#
# curs.execute("SELECT * FROM erzeugung")
# for spalte in curs.fetchall():
# print("Ergebnisse am {0} um {1}Uhr war {2}Volt".format(spalte[1], spalte[2], spalte[3]))
