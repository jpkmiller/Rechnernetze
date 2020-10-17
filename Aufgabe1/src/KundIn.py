from Aufgabe1.src.EventList import EventList
from Aufgabe1.src.Station import Station


class KundIn:
    def __init__(self, station_list: list, time_between_customers):
        self.stationList: list = list(station_list)
        self.timeBetweenCustomers = time_between_customers

    def begin(self, args):
        # instantiate next Customer (copy of current customer)
        next_customer = KundIn(self.stationList, self.timeBetweenCustomers)
        # create begin event for next customer (next customer of same type gets announced)
        begin_event = EventList.event(eTime=EventList.simulationTime + self.timeBetweenCustomers,
                                      ePrio=2,
                                      eNum=EventList.next(),
                                      eFun=next_customer.begin,
                                      eArgs=[])
        # create event for arriving at first station of current customer
        time_to_station = self.stationList[0][0]
        arrive_event = EventList.event(eTime=EventList.simulationTime + time_to_station, ePrio=3,
                                       eNum=EventList.next(), eFun=self.arrive,
                                       eArgs=[])
        # push created events on heap
        EventList.push(begin_event)
        EventList.push(arrive_event)
        return

    def arrive(self, args):
        # get station, customer should arrive to
        station = self.stationList[0]
        # check if queue of station is too long
        if len(station[3].customer_queue) < station[1]:
            # queue up to make the purchase at the current station
            # everything else decides the station the customer is queued in
            station[3].queue(self)
        # skip purchase if queue was too long
        else:
            # delete station to mark it as done
            self.stationList.pop(0)
            # create event for arriving at next station
            arrive_event = EventList.event(eTime=EventList.simulationTime + station[0], ePrio=3,
                                           eNum=EventList.next(), eFun=self.arrive, eArgs=[])
            # push event on heap
            EventList.push(arrive_event)
        return

    def leave(self, args):
        # get and delete station to mark it as done
        last_station: Station = self.stationList.pop(0)[3]
        # if statement should always be true!
        if len(last_station.customer_queue) > 0:
            # delete customer out of stations queue
            last_station.customer_queue.pop(0)
        # start serving next customer
        last_station.serve()
        # todo: maybe its better to make a wrapper method inside Station to queue out and start serving next customer?

        # setup next station:
        # return if all stations are done -> customer has finished
        if len(self.stationList) <= 0:
            return
        # create event for arriving at next station
        arrive_event = EventList.event(eTime=EventList.simulationTime + self.stationList[0][0], ePrio=3,
                                       eNum=EventList.next(), eFun=self.arrive, eArgs=[])
        # push event on heap
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
