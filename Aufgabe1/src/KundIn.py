import Aufgabe1.src.Supermarkt as sm
from Aufgabe1.src import Supermarkt
from Aufgabe1.src.EreignisListe import EreignisListe
from Aufgabe1.src.Station import Station


class KundIn:
    def __init__(self, stationList: list, timeBetweenCustomers):
        self.stationList: list = list(stationList)
        self.timeBetweenCustomers = timeBetweenCustomers

    def begin(self, args):
        next_customer = KundIn(self.stationList, self.timeBetweenCustomers)
        begin_event = Supermarkt.event(eTime=EreignisListe.simulationTime + self.timeBetweenCustomers, ePrio=2,
                                       eNum=++Supermarkt.counter,
                                       eFun=next_customer.begin,
                                       eArgs=[next_customer])
        station = self.stationList[0]
        arrive_event = Supermarkt.event(eTime=EreignisListe.simulationTime + station[0], ePrio=1,
                                        eNum=++Supermarkt.counter, eFun=self.arrive,
                                        eArgs=[])
        Supermarkt.event_list.push(begin_event)
        Supermarkt.event_list.push(arrive_event)
        return

    def arrive(self, at: Station):
        if at.customer_queue.__sizeof__() > 0:
            at.queue(self)
        else:
            at.serve(self.stationList[0][2])
        station = self.stationList[0]
        leave_event = Supermarkt.event(eTime=EreignisListe.simulationTime + station[1], ePrio=3,
                                       eNum=++Supermarkt.counter, eFun=self.leave, eArgs=[])
        Supermarkt.event_list.push(leave_event)
        return

    def leave(self):

        return

# •	Beginn des Einkaufs
# o	Ereignis Ankunft an der ersten Station erzeugen
# o	nächstes Ereignis Beginn des Einkaufs für den gleichen KundInnen-Typ erzeugen
# •	Ankunft an einer Station
# o	anhand der Warteschlangenlänge überprüfen, ob an der Station eingekauft wird
# o	wenn eingekauft wird, entweder Einreihen in die Warteschlange (Systemzustand ändern) oder im Falle einer direkten Bedienung das Ereignis Verlassen der Station erzeugen
# o	wenn nicht eingekauft wird, direkt das Ereignis Ankunft an der nächsten Station erzeugen
# •	Verlassen einer Station
# o	Ereignis Ankunft an der nächsten Station erzeugen
# o	wenn sich weitere KundInnnen in der Warteschlange befinden, erste KundIn aus der Warteschlange nehmen und Ereignis Verlassen der Station für die nächste KundIn erzeugen
