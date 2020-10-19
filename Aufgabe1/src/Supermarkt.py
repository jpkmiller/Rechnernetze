from Aufgabe1.src.EventList import EventList as EL
from Aufgabe1.src.Logger import Logger as L
from Aufgabe1.src.KundIn import KundIn
from Aufgabe1.src.Station import Station

bakery = Station('Bäcker', 10)
butcher = Station('Wursttheke', 30)
cheese = Station('Cheese', 60)
checkout = Station('Kasse', 5)

T1 = KundIn([
    # (Zeit von A nach B, max. Schlange, Anz. Einkäufe)
    (10, 10, 10, bakery),
    (30, 10, 5, butcher),
    (45, 5, 3, cheese),
    (60, 20, 30, checkout),
], 200, '1')

T2 = KundIn([
    (30, 5, 2, butcher),
    (30, 20, 3, checkout),
    (20, 20, 3, bakery),
], 60, '2')

if __name__ == "__main__":
    EL.push(EL.Event(0, 2, EL.next(), T1.begin, []))
    EL.push(EL.Event(1, 2, EL.next(), T2.begin, []))
    EL.start()
    L.log('supermarkt_self.txt')
