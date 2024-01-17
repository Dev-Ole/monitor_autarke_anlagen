

def test():
    lokalvar = "Lokal Variable!"
    lokalvar2 = "Die zweite"
    lokalvar3 = "NUMMER3"
    Werte = [lokalvar, lokalvar2,
    lokalvar3]
    return Werte

RestzeitStunden = (28+0.6) / 0.5
print(RestzeitStunden)
RestzeitTage = int(RestzeitStunden / 24)
print(RestzeitTage)
RestzeitStunden = RestzeitStunden - (RestzeitTage * 24)
print(RestzeitStunden)
