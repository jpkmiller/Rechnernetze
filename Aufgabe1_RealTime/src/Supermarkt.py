from Aufgabe1_EventList.src.EventList import EventList as EL
from Aufgabe1_RealTime.src.KundIn import KundIn
from Aufgabe1_RealTime.src.Station import Station

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
], 200, 'A')

T2 = KundIn([
    (30, 5, 2, butcher),
    (30, 20, 3, checkout),
    (20, 20, 3, bakery),
], 60, 'B')

if __name__ == "__main__":
    # FIXME: station threads are started at the beginning of the simulation
    # bakery.start()
    # butcher.start()
    # cheese.start()
    # checkout.start()

    EL.push(EL.Event(0, 2, EL.next(), T1.begin, []))
    EL.push(EL.Event(1, 2, EL.next(), T2.begin, []))
    EL.start()
