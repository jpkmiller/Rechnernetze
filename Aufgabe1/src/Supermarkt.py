from collections import namedtuple

from Aufgabe1.src.EreignisListe import EreignisListe
from Aufgabe1.src.KundIn import KundIn
from Aufgabe1.src.Station import Station

entrance = Station('Eingang')
bakery = Station('Bäcker', 10)
butcher = Station('Wursttheke', 30)
cheese = Station('Cheese', 60)
checkout = Station('Kasse', 5)

ereignisListe = []
global ereignisListe

T1 = KundIn([
    # (Zeit von A nach B, max. Schlange, Anz. Einkäufe)
    (10, 10, 10),
    (30, 10, 5),
    (45, 5, 3),
    (60, 20, 30)
])

T2 = KundIn([
    (30, 5, 2),
    (30, 20, 3),
    (20, 20, 3),
])

# Ereigniszeitpunkt, Ereignispriorität, Ereignisnummer, Ereignisfunktion, (optional) Ereignisargumenten
Ereignis = namedtuple('Ereignis', 'Ereigniszeitpunkt, Ereignispriorität, Ereignisnummer, Ereignisfunktion, args')
e1 = Ereignis()
e1.

def begin(kunden):
    ereignisListe.push(kunde)
    ereignisListe.push()

event = namedtuple('e', 'eTime, ePrio, eNum, eFun, eArgs')
initEreignisListe = [
    event(0, 0, 0, lambda kundin, station: kundin.begin(station), [T1, bakery])
    event(0, 0, 0, lambda kundin, station: kundin.begin(station), [T1, bakery])
]

if __name__ == "__main__":
    ereignisListe = EreignisListe(initEreignisListe)
    ereignisListe.start()
