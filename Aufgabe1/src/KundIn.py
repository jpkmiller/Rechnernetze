from Aufgabe1.src.EventList import EventList
from Aufgabe1.src.Station import Station


class KundIn:
    def __init__(self, station_list: list, time_between_customers):
        self.stationList: list = list(station_list)
        self.timeBetweenCustomers = time_between_customers

    def begin(self, args):
        # instantiate next Customer
        next_customer = KundIn(self.stationList, self.timeBetweenCustomers)
        # create begin event for next customer
        begin_event = EventList.event(eTime=EventList.simulationTime + self.timeBetweenCustomers,
                                      ePrio=2,
                                      eNum=EventList.next(),
                                      eFun=next_customer.begin,
                                      eArgs=[])
        # start current customers purchase
        time_to_station = self.stationList[0][0]
        arrive_event = EventList.event(eTime=EventList.simulationTime + time_to_station, ePrio=3,
                                       eNum=EventList.next(), eFun=self.arrive,
                                       eArgs=[])
        EventList.push(begin_event)
        EventList.push(arrive_event)
        return

    def arrive(self, args):
        station = self.stationList[0]
        if len(station[3].customer_queue) < station[1]:
            station[3].queue(self)
        else:
            self.stationList.pop(0)
            arrive_event = EventList.event(eTime=EventList.simulationTime + station[0], ePrio=3,
                                           eNum=EventList.next(), eFun=self.arrive, eArgs=[])
            EventList.push(arrive_event)
        return

    def leave(self, args):
        last_station: Station = self.stationList.pop(0)[3]
        if len(last_station.customer_queue) > 0:
            last_station.customer_queue.pop(0)
        last_station.serve()

        if len(self.stationList) <= 0:
            return
        arrive_event = EventList.event(eTime=EventList.simulationTime + self.stationList[0][0], ePrio=3,
                                       eNum=EventList.next(), eFun=self.arrive, eArgs=[])
        EventList.push(arrive_event)
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
