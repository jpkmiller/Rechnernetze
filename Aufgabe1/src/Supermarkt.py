from Aufgabe1.src.EventList import EventList as EL
from Aufgabe1.src.Logger import Logger as L
from Aufgabe1.src.KundIn import KundIn
from Aufgabe1.src.Station import Station


class Supermarkt:
    bakery = Station('Bäcker', 10)
    butcher = Station('Wursttheke', 30)
    cheese = Station('Cheese', 60)
    checkout = Station('Kasse', 5)

    # passing method references

    @staticmethod
    def get_bakery():
        return Supermarkt.bakery

    @staticmethod
    def get_butcher():
        return Supermarkt.butcher

    @staticmethod
    def get_cheese():
        return Supermarkt.cheese

    @staticmethod
    def get_checkout():
        return Supermarkt.checkout


T1 = KundIn([
    # (Zeit von A nach B, max. Schlange, Anz. Einkäufe)
    (10, 10, 10, Supermarkt.get_bakery),
    (30, 10, 5, Supermarkt.get_butcher),
    (45, 5, 3, Supermarkt.get_cheese),
    (60, 20, 30, Supermarkt.get_checkout),
], 200, 'A')

T2 = KundIn([
    (30, 5, 2, Supermarkt.get_butcher),
    (30, 20, 3, Supermarkt.get_checkout),
    (20, 20, 3, Supermarkt.get_bakery),
], 60, 'B')

if __name__ == "__main__":
    EL.push(EL.Event(0, 2, EL.next(), T1.begin, []))
    EL.push(EL.Event(1, 2, EL.next(), T2.begin, []))
    EL.start()

    # logging
    L.add_station_list([Supermarkt.get_bakery, Supermarkt.get_butcher, Supermarkt.get_cheese, Supermarkt.get_checkout])
    L.log('supermarkt_self.txt')
