from Aufgabe1.src.EventList import EventList
from Aufgabe1.src.KundIn import KundIn
from Aufgabe1.src.Station import Station

entrance = Station('Eingang')
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
], 200)

T2 = KundIn([
    (30, 5, 2, butcher),
    (30, 20, 3, checkout),
    (20, 20, 3, bakery),
], 60)

if __name__ == "__main__":
    EventList.push(EventList.event(0, 2, EventList.next(), T1.begin, []))
    EventList.push(EventList.event(1, 2, EventList.next(), T2.begin, []))
    EventList.start()
