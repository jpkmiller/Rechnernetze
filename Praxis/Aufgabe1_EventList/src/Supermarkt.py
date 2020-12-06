from Praxis.Aufgabe1_EventList.src.EventList import EventList as EL
from Praxis.Aufgabe1_EventList.src.Logger import Logger as L, Logger
from Praxis.Aufgabe1_EventList.src.KundIn import KundIn
from Praxis.Aufgabe1_EventList.src.Station import Station

bakery = Station('Bäcker', 10)
butcher = Station('Metzger', 30)
cheese = Station('Käse', 60)
checkout = Station('Kasse', 5)


T1 = KundIn([
    # (Zeit von A nach B, max. Schlange, Anz. Einkäufe)
    # passing method references
    # "references" are passed as values!!
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
    open("supermarkt.txt", "w").write("")
    open("supermarkt_customer.txt", "w").write("")

    EL.push(EL.Event(0, 2, EL.next(), T1.begin, []))
    EL.push(EL.Event(1, 2, EL.next(), T2.begin, []))
    EL.start(lambda: Logger.simulation_time < 3076)

    # logging
    # passing references here too
    L.add_station_list([bakery, butcher, cheese, checkout])
    L.log('supermarkt.txt')
